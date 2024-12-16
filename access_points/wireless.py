import typer

def configure():
    typer.echo("Configuring wireless settings")
    ssid = typer.prompt("Enter SSID")
    password = typer.prompt("Enter password", hide_input=True)
    
    config = f"""
ssid {ssid}
 authentication open
 authentication key-management wpa version 2
 wpa-psk ascii 0 {password}
"""
    return config

