from datetime import datetime
import ipaddress

def parse_axonius_data(data):
    """
    parse data collected from Axonius endpoint and convert to UDM
    catch and report specific errors related to the process
    returns:
        List: list of parsed asset data (in UDM format) or None if error occurs
    """
    parsed_data = []
    
    print(f"Parsing {len(data)} assets...")
    current_datetime = datetime.utcnow()
    formatted_datetime = current_datetime.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'    
    for asset in data:
        parsed_asset = {}

        try:
            parsed_asset["metadata"] = {"collected_timestamp": formatted_datetime, "entity_type": "ASSET"}
            
            # Asset Id and Product Object Id are mapped to Internal Axon Id
            asset_id = "internal_axon_id:" + str(asset.get("internal_axon_id", ""))
            
            # Hostname can be a list or string
            hostname = ""
                
            try:
                if "specific_data.data.hostname" in asset:
                    if isinstance(asset.get("specific_data.data.hostname"), str):
                        hostname = asset["specific_data.data.hostname"]
                    elif isinstance(asset.get("specific_data.data.hostname"), list):
                        hostname = asset["specific_data.data.hostname"][0]
                else:
                    print("Hostname not found!")
                    print(f"Skipping this asset: {asset_id}")
                    continue
            except Exception as e:
                print("Error gathering hostname!")
                print(f"Skipping this asset: {asset_id}")
                print(e)                    
                continue
                
            
            # IPS
            # From Axonius --> public_ips && network_interface_ips
            # To SecOps --> ip && nat_ip
            
            # Parse through public ips --> copy over to the ips field
            ips = set()
            try:
                for _ in asset.get("specific_data.data.public_ips", []):
                    ips.add(_)
            except Exception as e:
                print("Error gathering Ip")
                print(e)                    

            # For nat_ips, we find all non-private ips (not in below range):
            # 192.168.x.x, 172.x.x.x, or 10.x.x.x, 169.254.x.x
            
            # Also, collect all ips in following range:
            # 100.64.0.0/10, i.e. IP addresses from 100.64.0.0 to 100.127.255.255 (CGNAT)

            # We also add IpV6 addresses

            nat_ips = set()
            try:
                # Define the IP ranges
                private_ranges = [
                    # Range: 192.168.0.0 to 192.168.255.255
                    ipaddress.IPv4Network("192.168.0.0/16"),
                    # Range: 172.16.0.0 to 172.31.255.255
                    ipaddress.IPv4Network("172.16.0.0/12"),
                    # Range: 10.0.0.0 to 10.255.255.255
                    ipaddress.IPv4Network("10.0.0.0/8"),
                    # Range: 169.254.0.0 to 169.254.255.255
                    ipaddress.IPv4Network("169.254.0.0/16"),
                ]
                
                other_ranges = [                
                    # Range: 100.64.0.0 to 100.127.255.255
                    ipaddress.IPv4Network("100.64.0.0/10")
                ]

                def is_in_private_ranges(ip):
                    ip_obj = ipaddress.IPv4Address(ip)
                    return any(ip_obj in network for network in private_ranges)

                def is_in_other_ranges(ip):
                    ip_obj = ipaddress.IPv4Address(ip)
                    return any(ip_obj in network for network in other_ranges)

                # Check public IPs
                for ip in asset.get("specific_data.data.public_ips", []):
                    if isinstance(ipaddress.ip_address(ip), ipaddress.IPv6Address):
                        ips.add(ip)
                        break
                    if not is_in_private_ranges(ip):
                        nat_ips.add(ip)
                    if is_in_other_ranges(ip):
                        nat_ips.add(ip)

                # Check network interface IPs
                for ip in asset.get("specific_data.data.network_interfaces.ips", []):
                    if isinstance(ipaddress.ip_address(ip), ipaddress.IPv6Address):
                        ips.add(ip)
                        break
                    if not is_in_private_ranges(ip):
                        nat_ips.add(ip)
                    if is_in_other_ranges(ip):
                        nat_ips.add(ip)
            except Exception as e:
                print("Error gathering Nat IPs")
                print(e)                    

            # Mac address mapped to mac
            mac = []
            try:
                mac = asset.get("specific_data.data.network_interfaces.mac", "")
            except Exception as e:
                print("Error gathering mac address")
                print(e)

            # Last Seen mapped to last_discover_time
            last_discover_time = formatted_datetime
            try:
                last_discover_time = datetime.strptime(asset.get("specific_data.data.last_seen", ""), "%a, %d %b %Y %H:%M:%S %Z").strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
            except Exception as e:
                print(f"Error gathering last seen time --> {asset["internal_axon_id"]}")

            # Distribution Name and Distribution are combined and mapped to platform_software
            platform_software = {}
            platform_software["platform"] = "UNKNOWN_PLATFORM"
            platform_software["platform_patch_level"] = ""
            platform_software["platform_version"] = ""
            
            try:
                if "specific_data.data.os.distribution_name_preferred" in asset:
                    if "windows" in asset["specific_data.data.os.distribution_name_preferred"].lower():
                        dist_name = "WINDOWS"
                    elif "ios" in asset["specific_data.data.os.distribution_name_preferred"].lower():                        
                        dist_name = "IOS"
                    elif "mac" in asset["specific_data.data.os.distribution_name_preferred"].lower():
                        dist_name = "MAC"
                    elif "linux" in asset["specific_data.data.os.distribution_name_preferred"].lower():                        
                        dist_name = "LINUX"
                    elif "gcp" in asset["specific_data.data.os.distribution_name_preferred"].lower():
                        dist_name = "GCP"
                    elif "chrome_os" in asset["specific_data.data.os.distribution_name_preferred"].lower():
                        dist_name = "CHROME_OS"
                    elif "azure" in asset["specific_data.data.os.distribution_name_preferred"].lower():
                        dist_name = "AZURE"
                    elif "aws" in asset["specific_data.data.os.distribution_name_preferred"].lower():
                        dist_name = "AWS"
                    elif "android" in asset["specific_data.data.os.distribution_name_preferred"].lower():
                        dist_name = "ANDROID"
                    else:                        
                        dist_name = "UNKNOWN_PLATFORM"
                else:
                    dist_name = "UNKNOWN_PLATFORM"

                if "specific_data.data.os.distribution_preferred" in asset:
                    version = asset["specific_data.data.os.distribution_preferred"]
                else:
                    version = ""

                platform_software["platform"] = dist_name
                platform_software["platform_version"] = version
            except Exception as e:
                print("Error gathering distribution/name")
                print(e)

            # These are the labels we need:
            # "adapters_data.gui.custom_business_unit" --> asset.labels (key-> business unit)
            # "adapters_data.gui.custom_data_center_location" --> asset.labels (key-> data_center_location)
            # "adapters_data.gui.custom_location" --> asset.labels (key-> custom_location)

            try:
                business_unit = asset.get("adapters_data.gui.custom_business_unit", "")
                data_center_location = asset.get("adapters_data.gui.custom_data_center_location", "")
                location = asset.get("adapters_data.gui.custom_location", "")
            except Exception as e:
                print(e)
                print("GUI Adapter Data Not Found...")
                print(asset_id)

            parsed_asset["entity"] = {
                "asset": {
                    "asset_id": asset_id,
                    "product_object_id": asset_id,
                    "hostname": hostname,
                    "ip": list(ips),
                    "nat_ip": list(nat_ips),
                    "mac": mac,
                    "last_discover_time": last_discover_time,
                    "platform_software": platform_software,
                    "labels": [
                        {"key": "Custom Business Unit", "value": business_unit},
                        {"key": "Custom Data Center Location", "value": data_center_location},
                        {"key": "Custom Location", "value": location},                        
                    ]
                }
            }
        except Exception as e:
            print("Exception in parsing asset...")
            print(e)

        parsed_data.append(parsed_asset)            

    print(f"Parsed {len(data)} assets...")

    return parsed_data
