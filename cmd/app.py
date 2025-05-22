import typer
from cmd.process import app as process_app

app = typer.Typer()
app.add_typer(process_app)
