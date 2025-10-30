from fastapi import FastAPI, Depends, Header, HTTPException
from pydantic import BaseModel, Field
import httpx
from services.cache import cache_get, cache_set
from services.db import get_session, AsyncSession
from services.auth import require_auth, extract_bearer_token
from jinja2 import Environment, FileSystemLoader, select_autoescape
from typing import Dict
from fastapi.responses import HTMLResponse

app = FastAPI(title="python-uv-demo")

templates = Environment(
    loader=FileSystemLoader("templates"),
    autoescape=select_autoescape(["html", "xml"]),
)


class Item(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    qty: int = Field(ge=1, le=1000)


# simple in-memory store
_items: Dict[int, Item] = {}
_next_id: int = 1


@app.middleware("http")
async def auth_probe_middleware(request, call_next):
    # Light probe: record whether an Authorization header was sent
    auth_header = request.headers.get("authorization")
    request.state.has_auth = bool(extract_bearer_token(auth_header))
    response = await call_next(request)
    # Expose for tests/tools (not secure for prod)
    response.headers["X-Has-Auth"] = "1" if request.state.has_auth else "0"
    return response


# Intentionally unsafe: directly interpolates user input into HTML without sanitization
# This exists only for SCA/XSS demonstration purposes.
def render_unsafe_html(user_input: str) -> str:
    return (
        "<html><body>"
        f"<h1>Welcome {user_input}</h1>"
        f"<div id='msg'>{user_input}</div>"
        # Dangerous: reflecting raw user input into inline script context
        f"<script>var msg = '{user_input}';</script>"
        "</body></html>"
    )


@app.get("/")
async def root():
    tpl = templates.get_template("index.html")
    html = tpl.render(title="python-uv-demo", status="ok")
    return {"ok": True, "html": html}


@app.get("/unsafe")
async def unsafe_reflection(q: str = ""):
    html = render_unsafe_html(q)
    return HTMLResponse(content=html, media_type="text/html")


@app.post("/items")
async def create_item(item: Item, session: AsyncSession = Depends(get_session)):
    global _next_id
    item_id = _next_id
    _next_id += 1
    _items[item_id] = item
    return {"ok": True, "id": item_id, "item": item.model_dump()}


@app.get("/items/{item_id}")
async def read_item(item_id: int, token: str = Depends(require_auth)):
    if item_id not in _items:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"id": item_id, "item": _items[item_id].model_dump()}


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item, token: str = Depends(require_auth)):
    if item_id not in _items:
        raise HTTPException(status_code=404, detail="Item not found")
    _items[item_id] = item
    return {"ok": True, "id": item_id, "item": item.model_dump()}


@app.delete("/items/{item_id}")
async def delete_item(item_id: int, token: str = Depends(require_auth)):
    if item_id not in _items:
        raise HTTPException(status_code=404, detail="Item not found")
    del _items[item_id]
    return {"ok": True}


@app.get("/cache")
async def cache(key: str = "k", value: str | None = None):
    if value is not None:
        cache_set(key, value, ttl=60)
    return {"value": cache_get(key)}


@app.get("/httpbin")
async def httpbin():
    async with httpx.AsyncClient(timeout=5) as client:
        r = await client.get("https://httpbin.org/get")
        r.raise_for_status()
        return {"httpbin": r.json()}
