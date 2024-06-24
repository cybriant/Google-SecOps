# import the libs
from axonius_api_client.exceptions import ApiError, ConnectError, JsonError

def get_axonius_data(client, num_devices=-1):
    """
    get data from the Axonius API.
    connect to Axonius and then fetch all device data available
    catch and report specific errors related to the process
    Returns:
        list: data retrieved from Axonius, or none if an error occurs.
    """

    try:
        # Write regex to specify fields required
        fields_regex = ["^os\.|specific_data\.data\.public_ips|labels|specific_data\.data\.hostname|specific_data\.data\.last_seen"]

        # adapters = client.devices.get(fields_root="gui", max_rows=10)
        # fields_root gets us the following lines per asset:
        # "adapters_data.gui.custom_business_unit": "WSC",
        # "adapters_data.gui.custom_data_center_location": "IO",
        # "adapters_data.gui.custom_location": "IMPHX",

        # get the device data
        # If no device limit is set (defualt num_devices) then get data for all devices
        if num_devices == -1:
            data = client.devices.get(fields_root = "gui", fields_regex=fields_regex)
        # Else limit the number of devices
        else:
            data = client.devices.get(fields_root = "gui", max_rows=num_devices, fields_regex=fields_regex)
        return data

    except ConnectError as e:
        print(f"Connection error: {e}")
    except ApiError as e:
        print(f"API error: {e}")
    except JsonError as e:
        print(f"JSON error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    return None
