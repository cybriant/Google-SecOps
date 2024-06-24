# import the libs
from axonius_api_client.connect import Connect


# Initialize an authorized client with Axonius.

def initialize_client(AXONIUS_API_ENDPOINT, AXONIUS_API_KEY, AXONIUS_API_SECRET):
    try:
        client = Connect(url=AXONIUS_API_ENDPOINT, key=AXONIUS_API_KEY, secret=AXONIUS_API_SECRET)
        return client
    except Exception as e:
        print("Could not connect to Axonius Client.")
        print(e)
        exit()