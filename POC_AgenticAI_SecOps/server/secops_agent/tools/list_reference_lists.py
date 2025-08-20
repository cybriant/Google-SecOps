from google.auth.transport.requests import Request
from typing import Sequence, Mapping, Any, Tuple
import requests
from google.oauth2 import service_account
from google.auth.transport.requests import Request
import json
import os


def get_chronicle_credentials(environment):
    """Retrieves Chronicle API credentials from environment variable."""
    api_key = os.environ.get(environment)
    if not api_key:
        raise ValueError(
            f"{environment} environment variable not set. Please set your API key."
        )

    credential = service_account.Credentials.from_service_account_info(json.loads(api_key), scopes=['https://www.googleapis.com/auth/chronicle-backstory'])
    request = Request()
    credential.refresh(request)        
    return credential


def list_reference_lists_tool(environment: str = "default") -> dict:
    """Lists all Chronicle detection reference_lists for a specific environment.

    Args:
        environment (str, optional): The environment to list reference_lists for.
            Defaults to "default". This parameter is primarily for documentation
            and doesn't directly impact the API call in this simplified tool.
            The API key from the environment variable determines the actual
            environment being accessed.

    Returns:
        dict: status and result (list of reference lists) or error message.
    """
    try:
        credentials = get_chronicle_credentials(environment)

        next_page_token = None

        lists, next_page_token = list_reference_lists(                
            credentials=credentials,
            page_size=None,
            page_token=next_page_token,
        )

        all_lists = list(lists) if lists else []
        while next_page_token:
            lists, next_page_token = list_reference_lists(
                credentials=credentials,
                page_size=None,
                page_token=next_page_token,
            )

            if lists:
                all_lists.extend(lists)

        return {"status": "success", "lists": all_lists}
    except requests.exceptions.HTTPError as e:
        return {"status": "error", "error_message": f"HTTP error listing lists: {e}"}
    except ValueError as e:
        return {"status": "error", "error_message": str(e)}
    except Exception as e:
        return {"status": "error", "error_message": f"An unexpected error occurred: {e}"}


def list_reference_lists(
    credentials,
    page_size: int | None = None,
    page_token: str | None = None,
) -> Tuple[Sequence[Mapping[str, Any]], str]:
  """Retrieve a list of reference_lists.

  Args:
    credentials: Authorized credentials to make requests.
    page_size (optional): Maximum number of reference_lists to return.
      Must be non-negative, and is capped at a server-side limit of 1000.
      A server-side default of 100 is used if the size is 0 or a None value.
    page_token (optional): Page token from a previous list_reference_lists call used for
      pagination.
      The first page is retrieved if the token is the empty string or a None
      value.

  Returns:
    List of reference_lists and a page token for the next page of reference_lists, if there are any.

  Raises:
      requests.exceptions.HTTPError: HTTP request resulted in an error
        (response.status_code >= 400).
  """
  
  url = f"https://backstory.googleapis.com/v2/lists"
  params = {"page_size": page_size, "page_token": page_token, "view":"FULL"}

  response = requests.get(
      url,
      headers={"Authorization": f"Bearer {credentials.token}"},
      params=params
  )

  if response.status_code >= 400:
    print(response.text)
    response.raise_for_status()

  response_json = response.json()
  
  return response_json.get("lists"), response_json.get("nextPageToken")


