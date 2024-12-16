import typer
from rich.console import Console
from rich.panel import Panel
from rich import box
from rich.prompt import Prompt
from utils import clipboard

console=Console()

def configure_vlans():
    console.print("\n[bold magenta]Configuring VLANs[/bold magenta]")
    vlans = []

    while True:
        vlan_id = typer.prompt("Enter VLAN ID (or type 'done' to finish)")
        if vlan_id.lower() == "done":
            break

        vlan_name = typer.prompt(f"Enter name for VLAN {vlan_id}", default=f"VLAN_{vlan_id}")
        vlans.append(f"vlan {vlan_id}\n name {vlan_name}")

    return "\n".join(vlans)

def configure_interfaces():
    console.print("\n[bold blue]Configuring Interface Mode[/bold blue]")
    interfaces_config = []

    while True:
        interface = typer.prompt("Enter interface name (e.g., 'GigabitEthernet0/1') or type 'done' to finish")
        if interface.lower() == "done":
            break

        mode = typer.prompt("Select mode:\n1. Access\n2. Trunk", type=int, default=1)
        if mode == 1:
            vlan = typer.prompt(f"Enter VLAN ID for access mode on {interface}")
            config = f"""
interface {interface}
 switchport mode access
 switchport access vlan {vlan}
"""
        elif mode == 2:
            allowed_vlans = typer.prompt(f"Enter allowed VLANs for trunk mode on {interface} (leave blank for default)", default="")
            config = f"""
interface {interface}
 switchport mode trunk
"""
            if allowed_vlans:
                config += f" switchport trunk allowed vlan {allowed_vlans}\n"
        else:
            typer.echo("[Error] Invalid mode selected. Skipping this interface.")
            continue

        interfaces_config.append(config.strip())

    return "\n".join(interfaces_config)

def configure_dtp():
    console.print("\n[bold magenta]Configuring DTP[/bold magenta]")
    dtp_config = []

    while True:
        # Prompt for interface or global configuration
        config_type = typer.prompt(
            "\nSelect configuration type:\n1. Interface DTP Configuration\n2. Show Commands\n3. Exit",
            type=int,
            default=1
        )

        if config_type == 1:  # Interface DTP Configuration
            interface = typer.prompt("Enter interface name (e.g., GigabitEthernet0/1) or type 'done' to finish")
            if interface.lower() == "done":
                break

            dtp_mode = typer.prompt(
                "Select DTP mode:\n1. Dynamic Desirable\n2. Dynamic Auto\n3. Nonegotiate\n4. Disable DTP on Interface",
                type=int,
                default=1
            )

            modes = {
                1: "switchport mode dynamic desirable",
                2: "switchport mode dynamic auto",
                3: "switchport nonegotiate",
            }

            if dtp_mode == 4:  # Disable DTP
                mode_choice = typer.prompt("Disable DTP with:\n1. Access Mode\n2. Trunk Mode", type=int, default=1)
                if mode_choice == 1:
                    config = f"""
interface {interface}
 switchport mode access
"""
                elif mode_choice == 2:
                    config = f"""
interface {interface}
 switchport mode trunk
"""
                else:
                    console.print("[bold red]Invalid selection. Skipping interface configuration.[/bold red]")
                    continue
            else:
                config = f"""
interface {interface}
 {modes.get(dtp_mode, "[Error] Invalid mode selected.")}
"""

            dtp_config.append(config.strip())

        elif config_type == 2:  # Show Commands
            interface = typer.prompt("Enter the interface name for show commands (e.g., GigabitEthernet0/1)")
            config = f"""
! Use the following commands to verify DTP status for {interface}:
show dtp interface {interface}            ! Check DTP status for the specified interface
show running-config interface {interface} ! Verify interface DTP configuration
show interfaces trunk                     ! Display trunk information for all interfaces
"""
            dtp_config.append(config.strip())

        elif config_type == 3:  # Exit
            typer.echo("\nExiting DTP configuration.")
            break

        else:
            typer.echo("[bold red]Invalid selection. Please try again.[/bold red]")

    return "\n".join(dtp_config)

def configure_vtp():
    console.print("\n[bold magenta]Configuring VTP (VLAN Trunking Protocol)[/bold magenta]")
    vtp_config = []

    # Select VTP Mode
    vtp_mode = typer.prompt(
        "Select VTP mode:\n1. Server\n2. Client\n3. Transparent\n4. Off",
        type=int,
        default=1
    )

    modes = {
        1: "vtp mode server",
        2: "vtp mode client",
        3: "vtp mode transparent",
        4: "vtp mode off",
    }
    selected_mode = modes.get(vtp_mode)
    if not selected_mode:
        console.print("[bold red]Invalid mode selected. Exiting VTP configuration.[/bold red]")
        return

    vtp_config.append(selected_mode)

    # Optional: Set VTP Domain Name
    domain_name = typer.prompt("Enter VTP domain name (leave blank to skip)", default="")
    if domain_name:
        vtp_config.append(f"vtp domain {domain_name}")

    # Optional: Set VTP Version
    version = typer.prompt(
        "Select VTP version:\n1. Version 1\n2. Version 2\n3. Version 3",
        type=int,
        default=1
    )
    if version in [1, 2, 3]:
        vtp_config.append(f"vtp version {version}")
    else:
        console.print("[bold red]Invalid version selected. Skipping version configuration.[/bold red]")

    # Optional: Set VTP Password
    password = typer.prompt("Enter VTP password (leave blank to skip)", default="")
    if password:
        vtp_config.append(f"vtp password {password}")

    # Optional: Enable/Disable VTP Pruning
    pruning = typer.prompt("Enable VTP pruning? (yes/no)", default="no")
    if pruning.lower() == "yes" and vtp_mode in [1, 2]:  # Pruning is valid for Server and Client modes only
        vtp_config.append("vtp pruning")
    elif pruning.lower() == "yes":
        console.print("[bold red]Pruning is only available in Server or Client mode. Skipping pruning configuration.[/bold red]")

    # Optional: Additional Configuration for VTP Version 3
    if version == 3:
        sync_database = typer.prompt("Synchronize VLAN database? (yes/no)", default="no")
        if sync_database.lower() == "yes":
            vtp_config.append("vtp database synchronize")

    # Show Commands
    show_commands = typer.prompt("Do you want to include VTP show commands? (yes/no)", default="yes")
    if show_commands.lower() == "yes":
        vtp_config.append("""
! Use the following commands to verify VTP configuration:
show vtp status
show vtp counters
""")

    return "\n".join(vtp_config)



def configure_cdp_lldp():
    """
    Combined configuration for CDP and LLDP, including:
    - Global enable/disable
    - Interface-level enable/disable
    - Verification commands
    """
    console.print("\n[bold cyan]Configuring CDP and LLDP[/bold cyan]\n")

    config = ""

    # Global CDP Configuration
    if Prompt.ask("Enable CDP globally? (yes/no)", choices=["yes", "no"], default="yes") == "yes":
        config += "cdp run\n"
    else:
        config += "no cdp run\n"

    # Global LLDP Configuration
    if Prompt.ask("Enable LLDP globally? (yes/no)", choices=["yes", "no"], default="yes") == "yes":
        config += "lldp run\n"
    else:
        config += "no lldp run\n"

    # Interface-Level Configuration
    while Prompt.ask("Do you want to configure CDP or LLDP for specific interfaces? (yes/no)", choices=["yes", "no"], default="no") == "yes":
        interface = Prompt.ask("Enter the interface name (e.g., GigabitEthernet0/1)")

        console.print(f"\n[bold]Configuring interface {interface}:[/bold]")
        config += f"interface {interface}\n"

        # CDP on interface
        cdp_choice = Prompt.ask("Enable, disable, or skip CDP? (enable/disable/skip)", choices=["enable", "disable", "skip"], default="skip")
        if cdp_choice == "enable":
            config += " cdp enable\n"
        elif cdp_choice == "disable":
            config += " no cdp enable\n"

        # LLDP on interface
        lldp_choice = Prompt.ask("Enable, disable, or skip LLDP? (enable/disable/skip)", choices=["enable", "disable", "skip"], default="skip")
        if lldp_choice == "enable":
            config += " lldp transmit\n lldp receive\n"
        elif lldp_choice == "disable":
            config += " no lldp transmit\n no lldp receive\n"

    # Verification Commands
    if Prompt.ask("Include CDP verification commands? (yes/no)", choices=["yes", "no"], default="yes") == "yes":
        config += "\n! CDP Verification Commands\n"
        config += "show cdp\nshow cdp neighbors\nshow cdp neighbors detail\nshow cdp interface\n"

    if Prompt.ask("Include LLDP verification commands? (yes/no)", choices=["yes", "no"], default="yes") == "yes":
        config += "\n! LLDP Verification Commands\n"
        config += "show lldp\nshow lldp neighbors\nshow lldp neighbors detail\nshow lldp interface\n"

    return config 
   
def configure_etherchannel():
    """
    Configures EtherChannel with LACP or PAgP modes, including trunking settings,
    load balancing, optional show commands, and verification commands.
    """
    # Prompt for EtherChannel details
    channel_group = input("\nEnter channel-group number: ")
    
    # Choose between LACP and PAgP
    etherchannel_protocol = input("Select EtherChannel protocol:\n1. LACP\n2. PAgP\nEnter choice (1/2): ")

    if etherchannel_protocol == "1":
        # LACP Modes (Active/Passive)
        mode = int(input("Select LACP mode:\n1. Active\n2. Passive\nEnter choice (1/2): "))
        modes = {
            1: f"channel-group {channel_group} mode active",  # LACP Active
            2: f"channel-group {channel_group} mode passive"  # LACP Passive
        }
        etherchannel_config = modes.get(mode, '[Error] Invalid mode selected.')
        
        # LACP Show Commands
        show_commands = input("Do you want to include LACP show commands? (yes/no): ").lower()
        if show_commands == "yes":
            lacp_show_commands = """
! LACP Show Commands
show lacp neighbor
show lacp interface
show etherchannel summary
show etherchannel load-balance
"""
        else:
            lacp_show_commands = ""

    elif etherchannel_protocol == "2":
        # PAgP Modes (Auto/Desirable)
        mode = int(input("Select PAgP mode:\n1. Auto\n2. Desirable\nEnter choice (1/2): "))
        modes = {
            1: f"channel-group {channel_group} mode auto",      # PAgP Auto
            2: f"channel-group {channel_group} mode desirable"  # PAgP Desirable
        }
        etherchannel_config = modes.get(mode, '[Error] Invalid mode selected.')
        
        # PAgP Show Commands
        show_commands = input("Do you want to include PAgP show commands? (yes/no): ").lower()
        if show_commands == "yes":
            pagp_show_commands = """
! PAgP Show Commands
show pagp brief
show pagp neighbor
show etherchannel summary
show etherchannel load-balance
"""
        else:
            pagp_show_commands = ""

    else:
        etherchannel_config = '[Error] Invalid protocol selected.'
        lacp_show_commands = ""
        pagp_show_commands = ""

    # Collect interface details
    interface_range = input("Enter interface range (e.g., GigabitEthernet1/0/1 - 2): ")

    # Define trunk settings
    allowed_vlans = input("Enter allowed VLANs for trunking (e.g., 10,20,30): ")
    portfast = input("Enable spanning-tree portfast for faster trunk convergence? (yes/no): ").lower() == 'yes'

    # Define the load-balancing method
    load_balance_method = input("Enter load-balancing method (e.g., src-dst-mac, src-dst-ip): ")

    # EtherChannel configuration string
    config = f"""
! Global EtherChannel Configuration
feature port-channel

! Configuring the physical interfaces for EtherChannel
interface range {interface_range}
 description Link to Server
 switchport mode trunk
 switchport trunk allowed vlan {allowed_vlans}
 {etherchannel_config}
 no shutdown

! Configuring the Port-Channel interface
interface Port-channel{channel_group}
 description EtherChannel to Server
 switchport mode trunk
 switchport trunk allowed vlan {allowed_vlans}
 spanning-tree portfast trunk
"""

    # Load Balancing Configuration
    config += f"\n! Load Balancing Configuration\nport-channel load-balance {load_balance_method}\n"

    # Optional LACP/PAgP configuration (only if LACP or PAgP is used)
    if etherchannel_protocol == "1" or etherchannel_protocol == "2":
        priority = input("Enter EtherChannel port priority (e.g., 128, 256): ")
        system_priority = input("Enter EtherChannel system priority (e.g., 32768): ")
        config += f"""
! Optional EtherChannel Protocol Configuration
etherchannel system-priority {system_priority}
etherchannel port-priority {priority}
"""

    # Add show commands if requested
    if etherchannel_protocol == "1" and lacp_show_commands:
        config += lacp_show_commands
    elif etherchannel_protocol == "2" and pagp_show_commands:
        config += pagp_show_commands

    # Return the final configuration
    return config

def configure_stp():
    """
    Configures Spanning Tree Protocol (STP) with PVST, Rapid-PVST, or MST,
    including optional show commands for each STP mode at the end.
    This version also allows the configuration of multiple interfaces in a loop.
    """
    typer.echo("\n[bold green]Configuring STP[/bold green]")

    # Prompt for STP mode selection
    stp_mode = typer.prompt("Select STP mode:\n1. PVST\n2. Rapid-PVST\n3. MST", type=int, default=1)

    modes = {
        1: "spanning-tree mode pvst",
        2: "spanning-tree mode rapid-pvst",
        3: "spanning-tree mode mst"
    }

    config = modes.get(stp_mode, "[Error] Invalid mode selected.")

    # Additional MST configuration
    if stp_mode == 3:
        instance = typer.prompt("Enter MST instance number", default="1")
        vlan_map = typer.prompt("Enter VLAN-to-instance mapping (e.g., '10-20,30-40')", default="")
        config += f"\nspanning-tree mst configuration\n instance {instance} vlan {vlan_map}"

    # Loop for configuring multiple interfaces
    while True:
        interface = typer.prompt("Enter interface (e.g., GigabitEthernet0/1), or type 'done' to finish")
        if interface.lower() == "done":
            break

        config += f"\ninterface {interface}\n"
        config += f"spanning-tree portfast\n"  # Add other port-related configurations as needed

        # Option to configure additional STP settings for this interface
        stp_enabled = input(f"Do you want to enable STP on interface {interface}? (yes/no): ").lower()
        if stp_enabled == "yes":
            config += "spanning-tree bpduguard enable\n"
            config += "spanning-tree bpdufilter enable\n"

        # Loop for additional interface configurations
        additional_configs = input(f"Do you want to add more STP configurations for {interface}? (yes/no): ").lower()
        if additional_configs == "yes":
            # Allow user to specify if they want to configure any STP options like portfast, guard, etc.
            portfast_enabled = input(f"Enable portfast on {interface}? (yes/no): ").lower()
            if portfast_enabled == "yes":
                config += f"spanning-tree portfast\n"

            bpdu_guard = input(f"Enable BPDU Guard on {interface}? (yes/no): ").lower()
            if bpdu_guard == "yes":
                config += f"spanning-tree bpduguard enable\n"

            bpdu_filter = input(f"Enable BPDU Filter on {interface}? (yes/no): ").lower()
            if bpdu_filter == "yes":
                config += f"spanning-tree bpdufilter enable\n"

    # Ask the user whether to include show commands after interface configurations
    stp_show_commands = input("Do you want to include show commands for the selected STP mode? (yes/no): ").lower()

    if stp_show_commands == "yes":
        if stp_mode == 1:
            config += """
! PVST Show Commands
show spanning-tree
show spanning-tree vlan
show spanning-tree detail
show spanning-tree interface
"""
        elif stp_mode == 2:
            config += """
! Rapid-PVST Show Commands
show spanning-tree rapid-pvst
show spanning-tree rapid-pvst vlan
show spanning-tree rapid-pvst detail
show spanning-tree interface
"""
        elif stp_mode == 3:
            config += """
! MST Show Commands
show spanning-tree mst
show spanning-tree mst configuration
show spanning-tree mst instance
show spanning-tree mst instance detail
"""

    return config
