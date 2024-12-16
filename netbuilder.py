import typer
from art import text2art  # Library to generate ASCII art
from rich.console import Console
from rich.panel import Panel
from rich import box
from rich.prompt import Prompt
from routers.router_config import configure_router
from switches.switch_config import configure_switch
from access_points.ap_config import configure_access_point

app = typer.Typer()
console = Console()

@app.command()
def main():
    # Generate a dynamic ASCII welcome banner using text2art
    welcome_art = text2art("NetBuilder")
    console.print(Panel(welcome_art, title="[bold magenta]Welcome to[/bold magenta]", subtitle="[bold cyan]NetBuilder[/bold cyan]", box=box.HEAVY))

    device_type = Prompt.ask(
        "[bold cyan]Select a device type:[/bold cyan]\n1. [green]Router[/green]\n2. [blue]Switch[/blue]\n",
        choices=["1", "2"],
        default="1"
    )

    if device_type == "1":
        configure_router()
    elif device_type == "2":
        configure_switch()
    # elif device_type == "3":
    #     configure_access_point()
    else:
        console.print("[bold red]Invalid selection. Exiting.[/bold red]")

if __name__ == "__main__":
    app()
