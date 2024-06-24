# import the libs
from google.oauth2 import service_account
from googleapiclient import _auth
from google.auth.transport.requests import Request


# Initialize an authorized credential with SecOps.

def initialize_secops(SERVICE_ACCOUNT_FILE, SCOPES):
    try:

        # Create a credential using Google Developer Service Account Credential and Chronicle API
        credentials = service_account.Credentials.from_service_account_info(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        # Fetch the token w object request
        request = Request()
        # Try to refresh creds w new token if the current one is expired
        credentials.refresh(request)

        return credentials
    except Exception as e:
        print("Could not connect to SecOps.")
        print(e)
        exit()