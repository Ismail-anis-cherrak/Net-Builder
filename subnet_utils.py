import ipaddress

def cidr_to_netmask(cidr: int) -> str:
    """
    Convert CIDR to subnet mask.
    
    Args:
        cidr (int): The CIDR prefix (e.g., 24).
        
    Returns:
        str: Subnet mask (e.g., 255.255.255.0).
    """
    try:
        net = ipaddress.IPv4Network(f"0.0.0.0/{cidr}", strict=False)
        return str(net.netmask)
    except ValueError:
        raise ValueError("Invalid CIDR value. Must be between 0 and 32.")

def cidr_to_wildcard(cidr: int) -> str:
    """
    Convert CIDR to wildcard mask.
    
    Args:
        cidr (int): The CIDR prefix (e.g., 24).
        
    Returns:
        str: Wildcard mask (e.g., 0.0.0.255).
    """
    try:
        net = ipaddress.IPv4Network(f"0.0.0.0/{cidr}", strict=False)
        wildcard = ipaddress.IPv4Address(int(net.hostmask))
        return str(wildcard)
    except ValueError:
        raise ValueError("Invalid CIDR value. Must be between 0 and 32.")
