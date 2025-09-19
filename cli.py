import typer
from loguru import logger
from dotenv import load_dotenv

app = typer.Typer(help="python-uv demo CLI")


@app.command()
def hello(name: str = "world"):
    """Say hello from the CLI."""
    load_dotenv()
    logger.info("Saying hello")
    typer.echo(f"Hello, {name}!")


if __name__ == "__main__":
    app()
