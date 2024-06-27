# This file parses Axonius data into the respective UDM fields
# It uploads Entity data into SecOps to provide Asset Context and decrease TTR

# Mapping from Axonius to UDM:

# specific_data.data.hostname (may be a list or string)      <---> asset.hostname (cannot be repeated)
# internal_axon_id (always a string)                         <---> asset.product_object_id AND asset.asset_id
# adapters_data.gui.custom_business_unit                     <---> asset.labels (key, value)
# adapters_data.gui.custom_data_center_location              <---> asset.labels (key, value)
# adapters_data.gui.custom_location                          <---> asset.labels (key, value)
# specific_data.data.last_seen (always a string)             <---> asset.last_discover_time (protobuf timestamp)
# specific_data.data.public_ips (always a list)              <---> asset.ip (can be a list) + asset.nat_ip
# specific_data.data.network_interfaces.ips (always a list)  <---> asset.ip and asset.nat_ip
# specific_data.data.network_interfaces.mac (always a list)  <---> asset.mac (can be a list)
# specific_data.data.os.distribution_preferred               <---> asset.platform_software (platform)
# specific_data.data.os.distribution_name_preferred          <---> asset.platform_software (platform_version)

# imports
from apis.axonius import initialize_client
from apis.secOps import initialize_secops
from functions.pull_data_from_axonius import get_axonius_data
from functions.parse_data_to_UDM import parse_axonius_data
from functions.upload_data_to_SecOps import upload_axonius_data
import logger
from dotenv import load_dotenv
import os
import json
from time import sleep

# Load environment variables from .env file
load_dotenv()

# Set Up Logging
myLogger = logger.main(".\\Axonius_Parser_log.txt")
myLogger.info("Starting Axonius Parser.....")

# Initialize Axonius Client
client = initialize_client(os.getenv("AXONIUS_API_ENDPOINT"), os.getenv("AXONIUS_API_KEY"), os.getenv("AXONIUS_API_SECRET"))

# Initialize SecOps Credentials (Service Account, Scopes)
service_account_details = json.loads(os.getenv("SECOPS_API_SERVICE_ACCOUNT"))
scopes = ["https://www.googleapis.com/auth/malachite-ingestion"]
credentials = initialize_secops(service_account_details, scopes)

# Retrive Axonius Data
# You can also specify max_rows to get (-1 implies get all data)
myLogger.info("Getting Data from Axonius...")
data, e = get_axonius_data(client, num_devices=-1)
if e != "Complete":
    myLogger.info(f"Error Retrieving Data From Axonius. {e}")
    exit()

myLogger.info("Got Data from Axonius.")     

# Parse and upload in batches of 1000 assets
myLogger.info("Parsing and uploading Axonius data...")

BATCH_SIZE = 1000
total_assets_parsed = 0
hostname_errors = 0
total_assets = len(data)

if data:
    for i in range(0, len(data), BATCH_SIZE):
        data_batch = data[i:i+BATCH_SIZE]
        parsed_axonius_data, no_hostname_assets = parse_axonius_data(data_batch)
        total_assets_parsed += len(parsed_axonius_data)
        hostname_errors += len(no_hostname_assets)
        if(len(parsed_axonius_data) != 0):
            # with open(f".\\parsed_{i}.json", "w") as file:
            #     json.dump(parsed_axonius_data, file)
            upload_axonius_data(myLogger, credentials, parsed_axonius_data, os.getenv("CUSTOMER_ID"))
                
        for j in range(1):
            sleep(1)

    myLogger.info("Parsed and uploaded Axonius Data!")
    myLogger.info(f"Parsed {total_assets_parsed} assets out of {total_assets}")
    myLogger.info(f"{hostname_errors} assets did not have a hostname!")
else:
    myLogger.critical("No data received from Axonius...")
    print("No data retrieved from Axonius...")
