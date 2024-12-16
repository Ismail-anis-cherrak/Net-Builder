import typer

def configure():
    typer.echo("Configuring VLAN")
    vlan_id = typer.prompt("Enter VLAN ID")
    vlan_name = typer.prompt("Enter VLAN name")
    
    config = f"""
vlan {vlan_id}
 name {vlan_name}
"""
    return config

