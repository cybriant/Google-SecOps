
# Axonius To UDM Parser

This script parses Axonius data into the respective UDM (Unified Data Model) fields and uploads Entity data into SecOps to provide Asset Context and decrease TTR (Time to Resolution).

## Setup
### Prerequisites
- Python 3.x
Required Python packages (install using pip install -r requirements.txt):
- axonius_api_client
- google-auth
- google-auth-oauthlib
- google-auth-httplib2
- google-api-python-client
- googleapis-common-protos
- python-dotenv

## Usage
### Environment Variables
Create a .env file in the root directory with the following variables:
- AXONIUS_API_ENDPOINT=''
- AXONIUS_API_KEY=''
- AXONIUS_API_SECRET=''
- CUSTOMER_ID=''
- SECOPS_API_SERVICE_ACCOUNT = ''

### Logging
Log output is recommeded to be stored in a text file. Currently, log output is stored in "Axonius_Parser_log.txt".

### Running the Script
To run the script, execute the following command:

- python main.py

## Script Breakdown
### Imports and Initial Setup:

* Load environment variables.
* Set up logging.

### Initialize Clients:
* Axonius client using the API endpoint, key, and secret.
* SecOps credentials using the service account details and scopes.

### Retrieve Axonius Data:

* Fetch data from Axonius (all data if num_devices=-1).

### Parse and Upload Data:

* Parse and upload data in batches of 1000 assets.
* Log the progress and errors.

## Field Mapping

| Axonius Field                                       | UDM Field                            |
| --------------------------------------------------- | ------------------------------------ |
| specific_data.data.hostname (may be a list or string) | asset.hostname (cannot be repeated)  |
| internal_axon_id (always a string)                  | asset.product_object_id AND asset.asset_id |
| adapters_data.gui.custom_business_unit              | asset.labels (key, value)            |
| adapters_data.gui.custom_data_center_location       | asset.labels (key, value)            |
| adapters_data.gui.custom_location                   | asset.labels (key, value)            |
| specific_data.data.last_seen (always a string)      | asset.last_discover_time (protobuf timestamp) |
| specific_data.data.public_ips (always a list)       | asset.ip (can be a list) + asset.nat_ip |
| specific_data.data.network_interfaces.ips (always a list) | asset.ip and asset.nat_ip     |
| specific_data.data.network_interfaces.mac (always a list) | asset.mac (can be a list)   |
| specific_data.data.os.distribution_preferred        | asset.platform_software (platform)   |
| specific_data.data.os.distribution_name_preferred   | asset.platform_software (platform_version) |
