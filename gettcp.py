import os

# Get list of all directories ending with "snap"
snap_dirs = [d for d in os.listdir('.') if os.path.isdir(d) and d.endswith('snap')]

# Search for tcpip.snap files in each tcpip directory and extract interface names and IP addresses
interface_ips_files = []

for snap_dir in snap_dirs:
    tcpip_dir = os.path.join(snap_dir, 'tcpip')
    if os.path.isdir(tcpip_dir):
        tcpip_snap_file = os.path.join(tcpip_dir, 'tcpip.snap')
        if os.path.isfile(tcpip_snap_file):
            with open(tcpip_snap_file, 'r') as f:
                lines = f.readlines()

            interfaces = []
            current_interface = None

            for i, line in enumerate(lines):
                if line.startswith('en') and ':' in line:
                    current_interface = line.split(':')[0]
                    interfaces.append({'interface_name': current_interface, 'ips': []})
                elif 'inet ' in line and current_interface is not None:
                    ip = line.strip()
                    if current_interface == 'lo0':
                        interfaces[-1]['ips'].append(ip)
                    else:
                        parts = ip.split()
                        address = parts[1]
                        netmask_hex = parts[3][2:]  # Remove the "0x" prefix
                        netmask_decimal = ".".join(str(int(netmask_hex[i:i+2], 16)) for i in range(0, 8, 2))
                        ip_with_netmask = f"{address}/{netmask_decimal}"
                        if ip_with_netmask != '127.0.0.1/255.0.0.0':
                            interfaces[-1]['ips'].append(ip_with_netmask)

            interface_ips_files.append({'file_name': tcpip_snap_file, 'interfaces': interfaces})

for interface_ips_file in interface_ips_files:
    print(f"\nFile location: {interface_ips_file['file_name']}")
    for interface in interface_ips_file['interfaces']:
        if interface['ips']:
            print(f"Interface name: {interface['interface_name']}")
            print("IP addresses:")
            for ip in interface['ips']:
                print(ip)
