import typer
from rich import print

from app.core.config import get_settings

cli = typer.Typer(name="Newton Basins API", add_completion=False)


@cli.command()
def settings():
    settings = get_settings()
    print(settings.dict())


@cli.command()
def shell():  # pragma: no cover
    """Opens an interactive shell with objects auto imported"""
    settings = get_settings()
    _vars = {"settings": settings}
    print(f"Auto imports: {list(_vars.keys())}")
    try:
        from IPython import start_ipython

        start_ipython(argv=[], user_ns=_vars)
    except ImportError:
        import code

        code.InteractiveConsole(_vars).interact()


cli()
