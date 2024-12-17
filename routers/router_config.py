# from rich.console import Console
# from rich.panel import Panel
# from rich.prompt import Prompt
# from rich import box
# from routers import interfaces, routing
# from utils import clipboard

# console = Console()

# def configure_router():
#     console.print("\n[bold green]Router Configuration[/bold green]\n")
#     config_type = Prompt.ask(
#         "[bold cyan]Select configuration type:[/bold cyan]\n1. [yellow]Interface[/yellow]\n2. [magenta]Routing[/magenta]",
#         choices=["1", "2"],
#         default="1"
#     )

#     if config_type == "1":
#         config = interfaces.configure()
#     elif config_type == "2":
#         console.print("\n[bold cyan]Select Routing Protocol[/bold cyan]")
#         config = routing.configure()
#     else:
#         console.print("[bold red]Invalid selection. Exiting.[/bold red]\n")
#         return

#     console.print("\n[bold blue]Generated Configuration:[/bold blue]\n")
#     console.print(Panel(config, title="[bold green]Configuration[/bold green]", box=box.DOUBLE_EDGE))

#     if Prompt.ask("[bold cyan]Copy to clipboard?[/bold cyan]", choices=["yes", "no"], default="yes") == "yes":
#         clipboard.copy(config)
#         console.print("[bold green]Configuration copied to clipboard![/bold green]\n")


from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich import box
from routers import interfaces, routing
from utils import clipboard

console = Console()

def configure_router():
    console.print("\n[bold green]Router Configuration[/bold green]\n")
    
    while True:
        # Show all configuration options directly
        config_type = Prompt.ask(
            "[bold cyan]Select a configuration option:[/bold cyan]\n"
            "1. [yellow]Interfaces[/yellow]\n"
            "2. [magenta]RIP[/magenta]\n"
            "3. [magenta]OSPF[/magenta]\n"
            "4. [magenta]EIGRP[/magenta]\n"
            "5. [magenta]IS-IS[/magenta]\n"
            "6. [magenta]BGP[/magenta]\n"
            "7. [magenta]Static Routes[/magenta]\n"
            "8. [red]Back to Main Menu[/red]",
            choices=["1", "2", "3", "4", "5", "6", "7", "8"],
            default="8"
        )

        if config_type == "1":
            config = interfaces.configure()
        elif config_type == "2":
            config = routing.configure_rip()
        elif config_type == "3":
            config = routing.configure_ospf()
        elif config_type == "4":
            config = routing.configure_eigrp()
        elif config_type == "5":
            config = routing.configure_isis()
        elif config_type == "6":
            config = routing.configure_bgp()
        elif config_type == "7":
            config = routing.configure_static_routes()
        elif config_type == "8":
            console.print("[bold yellow]Returning to Main Menu...[/bold yellow]\n")
            break
        else:
            console.print("[bold red]Invalid selection. Try again.[/bold red]\n")
            continue

        # Show generated configuration
        console.print("\n[bold blue]Generated Configuration:[/bold blue]\n")
        console.print(Panel(config, title="[bold green]Configuration[/bold green]", box=box.DOUBLE_EDGE))

        # Copy to clipboard option
        if Prompt.ask("[bold cyan]Copy to clipboard?[/bold cyan]", choices=["yes", "no"], default="yes") == "yes":
            clipboard.copy(config)
            console.print("[bold green]Configuration copied to clipboard![/bold green]\n")
