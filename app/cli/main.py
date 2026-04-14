import typer
from pathlib import Path
from app.core.storage import load_json, save_json
from app.core.monitor import run_monitor
from app.core.fetcher import fetch
from app.core.parser import parse

BASE_DIR = Path(__file__).resolve().parents[2]
CONFIG_FILE = BASE_DIR / "data" / "sites.json"


app = typer.Typer()

@app.command()
def run():
    run_monitor()

# =========================
# list
# =========================
@app.command()
def list(detail: bool = typer.Option(False, "--detail", "-d")):
    """サイト一覧"""

    sites = load_json(CONFIG_FILE)

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
# remove
# =========================
@app.command()
def remove(name: str):
    """サイト削除"""

    sites = load_json(CONFIG_FILE)

    new_sites = [s for s in sites if s["name"] != name]

    if len(new_sites) == len(sites):
        typer.echo("Failed")
        return

    save_json(CONFIG_FILE, new_sites)
    typer.echo(f"{name} is deleted.")


# =========================
# add
# =========================
@app.command()
def add():
    """サイト追加"""

    sites = load_json(CONFIG_FILE)

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

if __name__ == "__main__":
    app()