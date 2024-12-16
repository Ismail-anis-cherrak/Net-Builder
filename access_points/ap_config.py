from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich import box
from access_points import wireless
from utils import clipboard

console = Console()

def configure_access_point():
    console.print("\n[bold magenta]Access Point Configuration[/bold magenta]\n")
    config = wireless.configure()
    console.print("\n[bold blue]Generated Configuration:[/bold blue]\n")
    console.print(Panel(config, title="[bold green]Configuration[/bold green]", box=box.DOUBLE_EDGE))

    if Prompt.ask("[bold cyan]Copy to clipboard?[/bold cyan]", choices=["yes", "no"], default="yes") == "yes":
        clipboard.copy(config)
        console.print("\n[bold green]Configuration copied to clipboard![/bold green]\n")
