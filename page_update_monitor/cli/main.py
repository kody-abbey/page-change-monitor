import typer
from page_update_monitor import __version__
from page_update_monitor.config import CONFIG_FILE
from page_update_monitor.core.storage import load_json, save_json
from page_update_monitor.core.monitor import run_monitor
from page_update_monitor.core.fetcher import fetch
from page_update_monitor.core.parser import parse



app = typer.Typer()

# =========================
# check
# =========================
@app.command()
def check():
    """Run programs to check if websites change"""
    run_monitor()

# =========================
# version
# =========================
@app.command()
def version():
    """Show this software's version"""
    typer.echo(__version__)

def version_callback(value: bool):
    if value:
        typer.echo(__version__)
        raise typer.Exit()

# =========================
# list
# =========================
@app.command()
def list(detail: bool = typer.Option(False, "--detail", "-d")):
    """See a list user added websites"""

    sites = load_json(CONFIG_FILE, [])

    if not sites:
        typer.echo("No sites")
        return

    for s in sites:
        if not detail:
            typer.echo(f"{s['name']} | {s['url']}")
        else:
            line = f"{s['name']} | {s['url']} | {s['mode']}"
            if s["mode"] == "selector":
                line += f" | {s.get('selector', '')}"
            typer.echo(line)

# =========================
# remove or rm
# =========================
@app.command()
def remove(name: str):
    """Remove a website from a list"""

    sites = load_json(CONFIG_FILE, [])

    new_sites = [s for s in sites if s["name"] != name]

    if len(new_sites) == len(sites):
        typer.echo("Failed")
        return

    save_json(CONFIG_FILE, new_sites)
    typer.echo(f"{name} is deleted.")
app.command(name="rm")(remove)

# =========================
# add
# =========================
@app.command()
def add():
    """Add a website to a list"""

    sites = load_json(CONFIG_FILE, [])

    # name
    name = typer.prompt("Enter site name")
    if not name.strip():
        typer.echo("Name cannot be empty")
        return

    # 重複チェック
    if any(s["name"] == name for s in sites):
        typer.echo("Already exists")
        return

    # url
    url = typer.prompt("Enter URL")
    if not url.startswith("http"):
        typer.echo("Invalid URL")
        return
    html = fetch(url)
    if html is None:
        typer.echo("Failed to fetch URL")
        return

    # mode
    mode_input = typer.prompt(
        "Select mode (default is full, if you want to use HTML selector, type slct)",
        default=""
    )

    if mode_input == "slct":
        mode = "selector"

        while True:
            selector = typer.prompt("Type HTML selector").strip()

            if not selector:
                typer.echo("Selector cannot be empty")
                continue

            if not selector.startswith("#") and not selector.startswith("."):
                selector = "#" + selector

            test_site = {
                "mode": "selector",
                "selector": selector
            }

            content = parse(test_site, html)

            if not content:
                typer.echo("Selector not found. Try again.")
                continue

            typer.echo(f"[OK] {selector} -> {content[:50]}...")
            break
        site = {
            "name": name,
            "url": url,
            "mode": "selector",
            "selector": selector
        }

    else:
        mode = "full"

        site = {
            "name": name,
            "url": url,
            "mode": mode
        }

    sites.append(site)
    save_json(CONFIG_FILE, sites)

    typer.echo("Added")

@app.callback()
def main(
    version: bool = typer.Option(
        None,
        "--version",
        "-v",
        help="Show version",
        callback=version_callback,
        is_eager=True,
    )
):
    pass

if __name__ == "__main__":
    app()