from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich import box
from switches import vlan
from utils import clipboard

console = Console()

def configure_switch():
    console.print("\n[bold blue]Switch Configuration[/bold blue]\n")

    while True:
        config_type = Prompt.ask(
            "[bold cyan]Select configuration type:[/bold cyan]\n"
            "1. [green]VLAN[/green]\n"
            "2. [yellow]Interface Mode (Access/Trunk)[/yellow]\n"
            "3. [blue]DTP[/blue]\n"
            "4. [magenta]VTP[/magenta]\n"
            "5. [cyan]CDP/LLDP[/cyan]\n"
            "6. [red]EtherChannel[/red]\n"
            "7. [bold red]STP[/bold red]\n"
            "8. [white]Exit[/white]",
            choices=["1", "2", "3", "4", "5", "6", "7", "8"],
            default="1"
        )

        if config_type == "1":
            config = vlan.configure_vlans()
        elif config_type == "2":
            config = vlan.configure_interfaces()
        elif config_type == "3":
            config = vlan.configure_dtp()
        elif config_type == "4":
            config = vlan.configure_vtp()
        elif config_type == "5":
            config = vlan.configure_cdp_lldp()
        elif config_type == "6":
            config = vlan.configure_etherchannel()
        elif config_type == "7":
            config = vlan.configure_stp()
        elif config_type == "8":
            console.print("\n[bold yellow]Exiting Switch Configuration.[/bold yellow]")
            break
        else:
            console.print("[bold red]Invalid selection. Try again.[/bold red]")
            continue

        console.print("\n[bold yellow]Generated Configuration:[/bold yellow]\n")
        console.print(Panel(config, title="[bold green]Configuration[/bold green]", box=box.DOUBLE_EDGE))

        if Prompt.ask("[bold cyan]Copy to clipboard?[/bold cyan]", choices=["yes", "no"], default="yes") == "yes":
            clipboard.copy(config)
            console.print("\n[bold green]Configuration copied to clipboard![/bold green]\n")
