
# **NetBuilder**

NetBuilder is a Python-based command-line application designed to automate network configurations for devices like routers and switches. It simplifies repetitive configuration tasks, allowing network engineers to focus on design and troubleshooting.

The tool generates configuration scripts for various network features, which can be copied directly to the clipboard for deployment.

---

## **Features**

- Configure router interfaces with IP addressing and subnetting.
- Automate routing protocol setups (e.g., OSPF, EIGRP, BGP, RIP, IS-IS, and static routes).
- Create and manage VLANs on switches.
- Utility functions for subnet calculations (e.g., CIDR to subnet mask).

---

## **Usage Scenarios**

### **1. Router Configuration: Basic Routing**
You need to configure a router with OSPF routing for the following networks:
- **Network 1**: 192.168.1.0/24
- **Network 2**: 10.0.0.0/8

#### Example Session:
```plaintext
Welcome to NetBuilder!
Select a device to configure:
1. Router
2. Switch
Enter your choice: 1

Select a configuration task:
1. Interface Configuration
2. Routing Protocols
Enter your choice: 2

Select a routing protocol:
1. OSPF
2. EIGRP
3. BGP
4. RIP
5. IS-IS
6. Static Routes
Enter your choice: 1

Enter OSPF Process ID: 1
Enter the number of networks to configure: 2

Enter network 1 (e.g., 192.168.1.0/24): 192.168.1.0/24
Enter network 2 (e.g., 10.0.0.0/8): 10.0.0.0/8

Generated Configuration:
router ospf 1
 network 192.168.1.0 0.0.0.255 area 0
 network 10.0.0.0 0.255.255.255 area 0
The configuration has been copied to the clipboard!
```

---

### **2. Switch Configuration: VLANs**
You need to configure a switch with the following VLANs:
- **HR**: VLAN ID 10, Name: HR_VLAN
- **IT**: VLAN ID 20, Name: IT_VLAN

#### Example Session:
```plaintext
Welcome to NetBuilder!
Select a device to configure:
1. Router
2. Switch
Enter your choice: 2

Select a configuration task:
1. VLAN Configuration
2. Other Features (coming soon)
Enter your choice: 1

Enter the number of VLANs to configure: 2

Enter VLAN ID for VLAN 1: 10
Enter VLAN Name for VLAN 1: HR_VLAN

Enter VLAN ID for VLAN 2: 20
Enter VLAN Name for VLAN 2: IT_VLAN

Generated Configuration:
vlan 10
 name HR_VLAN
vlan 20
 name IT_VLAN
The configuration has been copied to the clipboard!
```

---

## **Future Enhancements**
- Wireless access point configuration (e.g., SSID, WPA2 settings).
- Support for IPv6 routing protocols.
- Bulk configuration from YAML/JSON files.
- Interactive mode with validation of user inputs.
- Logging of configurations for audit purposes.

