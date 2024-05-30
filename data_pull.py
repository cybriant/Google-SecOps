# This file retrieves the following information from Axonius:
# Hostname
# Last Seen
# Public IP
# Network Interface
# OS
# Distribution
# Custom Data Tags (Location, Business Unit, Data Center Location)
# NIC IP Addresses


# import the libs
import axonius_api_client
from axonius_api_client.connect import Connect
from axonius_api_client.exceptions import ApiError, ConnectError, JsonError
import json
import warnings
warnings.filterwarnings(action="ignore", category=axonius_api_client.exceptions.ExtraAttributeWarning)
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# axonius api creds
AXONIUS_API_ENDPOINT = os.getenv("AXONIUS_API_ENDPOINT")
AXONIUS_API_KEY = os.getenv("AXONIUS_API_KEY")
AXONIUS_API_SECRET = os.getenv("AXONIUS_API_SECRET")


def get_axonius_data(num_devices=-1):

    """
    get data from the Axonius API.
    connect to Axonius and then fetch all device data available
    catch and report specific errors related to the process
    Returns:
        list: data retrieved from Axonius, or none if an error occurs.
    """

    try:
        # make the main connection to axonius
        client = Connect(url=AXONIUS_API_ENDPOINT, key=AXONIUS_API_KEY, secret=AXONIUS_API_SECRET)

        # Write regex to specify fields required
        fields_regex = ["^os\.|specific_data\.data\.public_ips|labels"]

        # get the device data
        # If no device limit is set (defualt num_devices) then get data for all devices
        if(num_devices==-1):
            data = client.devices.get(fields_regex=fields_regex)
        # Else limit the number of devices
        else:
            data = client.devices.get(max_rows=num_devices, fields_regex=fields_regex)

        # print(data)
        # Save to json
        with open('data.json', 'w') as json_file:
            json.dump(data, json_file, indent=4)

    except ConnectError as e:   
        print(f"Connection error: {e}")
    except ApiError as e:
        print(f"API error: {e}")
    except JsonError as e:
        print(f"JSON error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    return None

# main exec block
if __name__ == "__main__":
    get_axonius_data()
