import typer
from rich.console import Console
from subnet_utils import cidr_to_netmask, cidr_to_wildcard

console = Console()

def configure():
    console.print("Configuring routing protocols")
    configs = []

    protocol = typer.prompt(
        "Select a routing protocol:\n1. OSPF\n2. EIGRP\n3. BGP\n4. Static Routes\n5. RIP\n6. IS-IS",
        type=int
    )

    if protocol == 1:
        configs.append(configure_ospf())
    elif protocol == 2:
        configs.append(configure_eigrp())
    elif protocol == 3:
        configs.append(configure_bgp())
    elif protocol == 4:
        configs.append(configure_static_routes())
    elif protocol == 5:
        configs.append(configure_rip())
    elif protocol == 6:
        configs.append(configure_isis())
    else:
        console.print("[bold red]Invalid selection.[/bold red]")

    return "\n".join(configs)


def configure_ospf():
    console.print("\n[bold magenta]OSPF Configuration[/bold magenta]")

    # Ask if the user wants to configure OSPF for IPv4 or IPv6
    ip_version = typer.prompt("Do you want to configure OSPF for IPv4 or IPv6? (v4/v6)", default="v4").lower()

    process_id = typer.prompt("Enter OSPF process ID", default="1")
    router_id = typer.prompt("Enter OSPF router ID (or leave blank for default)", default="")
    if not router_id:
        router_id = None  # No router ID provided

    networks = []

    if ip_version == "v4":
        # For IPv4 (OSPFv2), use CIDR and wildcard masks
        while True:
            network = typer.prompt("Enter a network (e.g., 192.168.1.0/24) or 'done' to finish")
            if network.lower() == "done":
                break
            try:
                network_address, cidr = network.split('/')  # Split network and CIDR
                cidr = int(cidr)  # Ensure CIDR is an integer
                wildcard_mask = cidr_to_wildcard(cidr)  # Convert CIDR to wildcard mask
                area = typer.prompt(f"Enter OSPF area for {network}", default="0")
                networks.append(f"network {network_address} {wildcard_mask} area {area}")
            except ValueError:
                console.print("[bold red]Invalid network format. Please use the format 192.168.1.0/24[/bold red]")

        ospf_config = f"router ospf {process_id}\n"
        if router_id:
            ospf_config += f"router-id {router_id}\n"
        ospf_config += "\n".join(networks)

    elif ip_version == "v6":
        # For IPv6 (OSPFv3), configure interfaces with areas
        while True:
            interface = typer.prompt("Enter an interface (e.g., GigabitEthernet0/1) or 'done' to finish")
            if interface.lower() == "done":
                break
            area = typer.prompt(f"Enter OSPF area for interface {interface}", default="0")
            networks.append(f"interface {interface}\n ipv6 ospf {process_id} area {area}")

        ospf_config = f"router ospf {process_id}\n"
        if router_id:
            ospf_config += f"router-id {router_id}\n"
        ospf_config += "\n".join(networks)

    else:
        console.print("[bold red]Invalid IP version selected. Please choose 'v4' or 'v6'.[/bold red]")
        return

    return ospf_config

def configure_eigrp():
    console.print("\n[bold magenta]EIGRP Configuration[/bold magenta]")

    # Choose EIGRP address family (IPv4 or IPv6)
    address_family_choice = typer.prompt(
        "Select address family for EIGRP configuration:\n1. IPv4\n2. IPv6\nEnter your choice",
        type=int,
        default=1
    )

    if address_family_choice not in [1, 2]:
        console.print("[bold red]Invalid selection. Please choose 1 for IPv4 or 2 for IPv6.[/bold red]")
        return

    address_family_str = "IPv4" if address_family_choice == 1 else "IPv6"
    address_family_cmd = "ipv6" if address_family_choice == 2 else ""

    # Autonomous System Number
    as_number = typer.prompt("Enter EIGRP Autonomous System number", default="1")

    # Auto-summary configuration
    auto_summary = typer.prompt("Disable auto-summary? (yes/no)", default="yes")

    networks = []
    interfaces = []
    
    if address_family_choice == 1:  # IPv4
        while True:
            network = typer.prompt(f"Enter {address_family_str} network (e.g., 192.168.1.0/24) or 'done' to finish")
            if network.lower() == "done":
                break

            try:
                network_ip, cidr = network.split("/")  # Split network and CIDR
                cidr = int(cidr)
                wildcard_mask = cidr_to_wildcard(cidr)  # Convert CIDR to wildcard mask
                networks.append(f"network {network_ip} {wildcard_mask}")
            except (ValueError, IndexError):
                console.print("[bold red]Invalid network format. Please use the format 192.168.1.0/24[/bold red]")
                continue

    elif address_family_choice == 2:  # IPv6
        while True:
            interface = typer.prompt(f"Enter {address_family_str} interface (e.g., GigabitEthernet0/1) or 'done' to finish")
            if interface.lower() == "done":
                break
            interfaces.append(f"interface {interface}\n ipv6 eigrp {as_number}")

    # Construct EIGRP config
    eigrp_config = f"router eigrp {as_number}\n"
    if auto_summary.lower() == "yes":
        eigrp_config += "no auto-summary\n"

    if address_family_choice == 1:  # IPv4
        eigrp_config += "\n".join(networks)

    elif address_family_choice == 2:  # IPv6
        eigrp_config += f"address-family ipv6\n"
        eigrp_config += "\n".join(interfaces)

    return eigrp_config


def configure_bgp():
    console.print("\n[bold magenta]BGP Configuration[/bold magenta]")
    
    # Choose BGP address family (IPv4 or IPv6)
    address_family_choice = typer.prompt(
        "Select address family for BGP configuration:\n1. IPv4\n2. IPv6\nEnter your choice",
        type=int,
        default=1
    )

    if address_family_choice not in [1, 2]:
        console.print("[bold red]Invalid selection. Please choose 1 for IPv4 or 2 for IPv6.[/bold red]")
        return

    address_family_str = "IPv4" if address_family_choice == 1 else "IPv6"
    address_family_cmd = "ipv4" if address_family_choice == 1 else "ipv6"

    # Autonomous System Number
    as_number = typer.prompt("Enter your Autonomous System number", default="65001")
    
    neighbors = []
    
    # Loop to add neighbors
    while True:
        neighbor_ip = typer.prompt(f"Enter {address_family_str} neighbor IP address or 'done' to finish")
        if neighbor_ip.lower() == "done":
            break
        
        remote_as = typer.prompt(f"Enter remote AS for neighbor {neighbor_ip}", default="65002")
        if address_family_choice == 1:
            # IPv4 neighbor configuration
            neighbors.append(f"neighbor {neighbor_ip} remote-as {remote_as}")
        else:
            # IPv6 neighbor configuration
            neighbors.append(f"neighbor {neighbor_ip} remote-as {remote_as}\n{address_family_cmd} unicast")
    
    # Construct BGP config
    bgp_config = f"router bgp {as_number}\n" + "\n".join(neighbors)

    return bgp_config


def configure_static_routes():
    console.print("\n[bold magenta]Static Routes Configuration[/bold magenta]")
    routes = []
    
    # Choose route type at the beginning (IPv4 or IPv6)
    route_type_choice = typer.prompt(
        "Select default route type:\n1. IPv4\n2. IPv6\nEnter your choice",
        type=int,
        default=1
    )

    if route_type_choice not in [1, 2]:
        console.print("[bold red]Invalid selection. Please choose 1 for IPv4 or 2 for IPv6.[/bold red]")
        return

    # Set route type string for later use
    route_type_str = "IPv4" if route_type_choice == 1 else "IPv6"
    route_prefix = "ip" if route_type_choice == 1 else "ipv6"

    while True:
        console.print(f"\n[bold cyan]Adding {route_type_str} Route[/bold cyan]")
        
        # Prompt for destination network (CIDR format)
        destination = typer.prompt(
            f"Enter destination network ({'e.g., 192.168.1.0/24' if route_type_choice == 1 else 'e.g., 2001:db8::/64'}) or 'done' to finish"
        )
        if destination.lower() == "done":
            break
        
        if route_type_choice == 1:  # IPv4 configuration
            try:
                # Extract network and CIDR
                network, cidr = destination.split("/")
                cidr = int(cidr)
                subnet_mask = cidr_to_netmask(cidr)  # Convert CIDR to subnet mask
            except (ValueError, IndexError):
                console.print("[bold red]Invalid network format. Please use the format 192.168.1.0/24[/bold red]")
                continue

            # Prompt for next-hop or exit interface
            next_hop = typer.prompt(f"Enter next-hop IP address for {destination} (leave blank if not applicable)", default="")
            exit_int = typer.prompt(f"Enter exit-interface for {destination} (leave blank if not applicable)", default="")

            # Construct IPv4 route
            if next_hop and exit_int:
                routes.append(f"{route_prefix} route {network} {subnet_mask} {next_hop} {exit_int}")
            elif next_hop:
                routes.append(f"{route_prefix} route {network} {subnet_mask} {next_hop}")
            elif exit_int:
                routes.append(f"{route_prefix} route {network} {subnet_mask} {exit_int}")
            else:
                console.print("[bold red]Error: Either next-hop or exit-interface must be specified![/bold red]")
                continue

        elif route_type_choice == 2:  # IPv6 configuration
            try:
                # Validate IPv6 address
                from ipaddress import IPv6Network
                IPv6Network(destination)  # Validate format
            except ValueError:
                console.print("[bold red]Invalid IPv6 network format. Please use the format 2001:db8::/64.[/bold red]")
                continue

            # Prompt for next-hop or exit interface
            next_hop = typer.prompt(f"Enter next-hop IPv6 address for {destination} (leave blank if not applicable)", default="")
            exit_int = typer.prompt(f"Enter exit-interface for {destination} (leave blank if not applicable)", default="")

            # Construct IPv6 route
            if next_hop and exit_int:
                routes.append(f"{route_prefix} route {destination} {next_hop} {exit_int}")
            elif next_hop:
                routes.append(f"{route_prefix} route {destination} {next_hop}")
            elif exit_int:
                routes.append(f"{route_prefix} route {destination} {exit_int}")
            else:
                console.print("[bold red]Error: Either next-hop or exit-interface must be specified![/bold red]")
                continue

    return "\n".join(routes)

def configure_rip():
    console.print("\n[bold magenta]RIP Configuration[/bold magenta]")

    # Select address family (IPv4 or IPv6)
    address_family = typer.prompt(
        "Select address family:\n1. IPv4\n2. IPv6",
        type=int,
        default=1
    )
    address_family_type = "IPv4" if address_family == 1 else "IPv6"

    # Validate RIP version input
    while True:
        try:
            if address_family == 1:  # IPv4 supports versions 1 and 2
                version = int(typer.prompt("Enter RIP version (1/2)", default="2"))
                if version not in [1, 2]:
                    raise ValueError
            else:  # IPv6 supports only RIPng
                version = 6
            break
        except ValueError:
            console.print("[bold red]Invalid RIP version. Please enter 1 or 2 for IPv4.[/bold red]")

    # Auto-summary prompt only applies to IPv4
    if address_family == 1:
        auto_summary = typer.prompt("Disable auto-summary? (yes/no)", default="yes")

    networks = []
    while True:
        network = typer.prompt(
            f"Enter a network ({'e.g., 192.168.1.0' if address_family == 1 else 'e.g., 2001:db8::/64'}) or 'done' to finish"
        )
        if network.lower() == "done":
            break
        networks.append(network)

    # Build RIP configuration
    if address_family == 1:  # IPv4 configuration
        rip_config = f"router rip\nversion {version}\n"
        if auto_summary.lower() == "yes":
            rip_config += "no auto-summary\n"
        for network in networks:
            rip_config += f"network {network}\n"
    else:  # IPv6 configuration (RIPng)
        rip_config = "ipv6 router rip RIPng\n"
        for network in networks:
            rip_config += f"interface {network}\n ipv6 rip RIPng enable\n"

    return rip_config

def configure_isis():
    console.print("\n[bold magenta]IS-IS Configuration[/bold magenta]")
    process_tag = typer.prompt("Enter IS-IS process tag", default="1")

    # IPv4 or IPv6 selection
    address_family = typer.prompt(
        "Select address family:\n1. IPv4\n2. IPv6",
        type=int,
        default=1
    )
    address_family_type = "IPv4" if address_family == 1 else "IPv6"

    # Set IS-IS level
    isis_level = typer.prompt(
        "Select IS-IS level:\n1. Level-1\n2. Level-2\n3. Level-1-2",
        type=int,
        default=3
    )
    levels = {1: "level-1", 2: "level-2", 3: "level-1-2"}
    selected_level = levels.get(isis_level, "level-1-2")

    # Collect interfaces to enable IS-IS
    interfaces = []
    while True:
        interface = typer.prompt(f"Enter an interface to enable IS-IS for {address_family_type} (e.g., GigabitEthernet0/0) or 'done' to finish")
        if interface.lower() == "done":
            break
        if address_family == 1:  # IPv4
            ip_cidr = typer.prompt(f"Enter IPv4 address with CIDR for {interface} (e.g., 192.168.1.1/24)")
            ip, cidr = ip_cidr.split("/")
            subnet_mask = cidr_to_netmask(int(cidr))  # Convert CIDR to subnet mask
            interfaces.append((interface, ip, subnet_mask))
        elif address_family == 2:  # IPv6
            ipv6_address = typer.prompt(f"Enter IPv6 address with CIDR for {interface} (e.g., 2001:db8::1/64)")
            interfaces.append((interface, ipv6_address))

    # Build IS-IS configuration
    isis_config = f"router isis {process_tag}\n"
    isis_config += f" is-type {selected_level}\n"
    if address_family == 2:  # IPv6-specific configuration
        isis_config += " address-family ipv6\n"

    # Enable IS-IS on interfaces
    for interface in interfaces:
        if address_family == 1:  # IPv4
            int_name, ip, subnet_mask = interface
            isis_config += f"interface {int_name}\n"
            isis_config += f" ip address {ip} {subnet_mask}\n"
            isis_config += f" ip router isis {process_tag}\n"
        elif address_family == 2:  # IPv6
            int_name, ipv6_address = interface
            isis_config += f"interface {int_name}\n"
            isis_config += f" ipv6 address {ipv6_address}\n"
            isis_config += f" ipv6 router isis {process_tag}\n"

    return isis_config

