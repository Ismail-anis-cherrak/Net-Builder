import typer
from subnet_utils import cidr_to_netmask

def configure():
    typer.echo("Configuring router interfaces")
    configs = []

    while True:
        interface = typer.prompt("Enter interface name")
        ip_type = typer.prompt("Enter IP type (ipv4/ipv6)", default="ipv4").lower()

        if ip_type == "ipv4":
            ip_address = typer.prompt("Enter IPv4 address")
            cidr = typer.prompt("Enter CIDR prefix (e.g., 24)", type=int,default=24)
            subnet_mask = cidr_to_netmask(cidr)
            config = f"""
interface {interface}
 ip address {ip_address} {subnet_mask}
 no shutdown
"""
        elif ip_type == "ipv6":
            ipv6_address = typer.prompt("Enter IPv6 address (With the mask /64)")
            config = f"""
interface {interface}
 ipv6 address {ipv6_address}
 no shutdown
"""
        else:
            typer.echo("Invalid IP type. Skipping configuration for this interface.")
            continue

        configs.append(config)

        another = typer.confirm("Do you want to configure another interface?", default=True)
        if not another:
            break

    return "\n".join(configs)
