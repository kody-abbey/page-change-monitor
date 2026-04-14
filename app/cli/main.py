import typer
from app.core.monitor import run_monitor

app = typer.Typer()

@app.command()
def run():
    run_monitor()

if __name__ == "__main__":
    app()