from fastapi import FastAPI, Depends
from pydantic import BaseModel, Field
import httpx
from services.cache import cache_get, cache_set
from services.db import get_session, AsyncSession
from jinja2 import Environment, FileSystemLoader, select_autoescape

app = FastAPI(title="python-uv-demo")

templates = Environment(
    loader=FileSystemLoader("templates"),
    autoescape=select_autoescape(["html", "xml"]),
)


class Item(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    qty: int = Field(ge=1, le=1000)


@app.get("/")
async def root():
    tpl = templates.get_template("index.html")
    html = tpl.render(title="python-uv-demo", status="ok")
    return {"ok": True, "html": html}


@app.post("/items")
async def create_item(item: Item, session: AsyncSession = Depends(get_session)):
    # No real DB ops; ensure dependency wire works for SCA context
    return {"ok": True, "item": item.model_dump()}


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
