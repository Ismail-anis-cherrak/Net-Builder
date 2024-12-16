import typer
from art import text2art  # Library to generate ASCII art
from rich.console import Console
from rich.panel import Panel
from rich import box
from rich.prompt import Prompt
from routers import interfaces, routing
from switches import vlan
from access_points import wireless
from utils import clipboard

app = typer.Typer()
console = Console()

@app.command()
def main():
    # Generate a dynamic ASCII welcome banner using text2art
    welcome_art = text2art("NetBuilder")
    console.print(Panel(welcome_art, title="[bold magenta]Welcome to[/bold magenta]", subtitle="[bold cyan]NetBuilder[/bold cyan]", box=box.HEAVY))

    device_type = Prompt.ask(
        "[bold cyan]Select a device type:[/bold cyan]\n1. [green]Router[/green]\n2. [blue]Switch[/blue]\n3. [magenta]Access Point[/magenta]",
        choices=["1", "2", "3"],
        default="1"
    )

    if device_type == "1":
        configure_router()
    elif device_type == "2":
        configure_switch()
    elif device_type == "3":
        configure_access_point()
    else:
        console.print("[bold red]Invalid selection. Exiting.[/bold red]")

def configure_router():
    console.print("\n[bold green]Router Configuration[/bold green]\n")
    config_type = Prompt.ask(
        "[bold cyan]Select configuration type:[/bold cyan]\n1. [yellow]Interface[/yellow]\n2. [magenta]Routing[/magenta]",
        choices=["1", "2"],
        default="1"
    )

    if config_type == "1":
        config = interfaces.configure()
    elif config_type == "2":
        console.print("\n[bold cyan]Select Routing Protocol[/bold cyan]")
        config = routing.configure()
    else:
        console.print("[bold red]Invalid selection. Exiting.[/bold red]\n")
        return

    console.print("\n[bold blue]Generated Configuration:[/bold blue]\n")
    console.print(Panel(config, title="[bold green]Configuration[/bold green]", box=box.DOUBLE_EDGE))

    if Prompt.ask("[bold cyan]Copy to clipboard?[/bold cyan]", choices=["yes", "no"], default="yes") == "yes":
        clipboard.copy(config)
        console.print("[bold green]Configuration copied to clipboard![/bold green]\n")

def configure_switch():
    console.print("\n[bold blue]Switch Configuration[/bold blue]\n")
    config = vlan.configure()
    console.print("\n[bold yellow]Generated Configuration:[/bold yellow]\n")
    console.print(Panel(config, title="[bold green]Configuration[/bold green]", box=box.DOUBLE_EDGE))

    if Prompt.ask("[bold cyan]Copy to clipboard?[/bold cyan]", choices=["yes", "no"], default="yes") == "yes":
        clipboard.copy(config)
        console.print("\n[bold green]Configuration copied to clipboard![/bold green]\n")

def configure_access_point():
    console.print("\n[bold magenta]Access Point Configuration[/bold magenta]\n")
    config = wireless.configure()
    console.print("\n[bold blue]Generated Configuration:[/bold blue]\n")
    console.print(Panel(config, title="[bold green]Configuration[/bold green]", box=box.DOUBLE_EDGE))

    if Prompt.ask("[bold cyan]Copy to clipboard?[/bold cyan]", choices=["yes", "no"], default="yes") == "yes":
        clipboard.copy(config)
        console.print("\n[bold green]Configuration copied to clipboard![/bold green]\n")

if __name__ == "__main__":
    app()
