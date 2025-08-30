import subprocess

from rich.console import Console
from rich.table import Table
import typer
from tinydb import TinyDB, Query
from link2v2ray import link2v2ray

app = typer.Typer()
console = Console()
db = TinyDB("servers.json")
qr = Query()

TUN = False

@app.command()
def add(id:str):
#check if its valid
    url = console.input("url:\n")
    console.print(url)
    db.insert({'url': url, 'id': id})
    

@app.command()
def delete(id:str):
    pass
@app.command()
def show():
    table = Table(title="servers")
    table.add_column("ID", justify="right", style="cyan")
    table.add_column("url", justify="right", style="green")
    table.add_column("selected", justify="right")
    servers = db.all()
    for server in servers:
        table.add_row(server["id"], server["url"])
    console.print(table)
    console.print(f"[yellow]TUN[/yellow] mode {"[green]ON[/green]" if TUN else "[red]OFF[/red]"}")
v2ray_process = subprocess.Popen(
    ["v2ray", "run", " -config", "config.json"]
)
@app.command()
def run(id=None):
    current_config = db.search(qr.id == "id")if id else db.all()[-1]["url"]
    current_config = link2v2ray(current_config)

    with open("config.json", "w") as f:
        f.write(current_config)
    def v2ray_init():
        if v2ray_process.poll() is None:
            v2ray_process.kill()
            v2ray_process = subprocess.Popen(["v2ray", "run", " -config", "config.json"])
        else:
            v2ray_process = subprocess.Popen(["v2ray", "run", " -config", "config.json"])

@app.command()
def stop():
    if v2ray_process.poll() is None:
        v2ray_process.kill()



if __name__ == "__main__":
    app()

