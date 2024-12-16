from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich import box
from routers import interfaces, routing
from utils import clipboard

console = Console()

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
