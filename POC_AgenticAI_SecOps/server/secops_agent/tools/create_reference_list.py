from google.auth.transport.requests import Request
from typing import Mapping, Any, List
import requests
from google.oauth2 import service_account
import json
import os
from typing import List, Dict, Any


def get_chronicle_credentials(environment: str):
    """Retrieves Chronicle API credentials from environment variable.

    Args:
        environment: The name of the environment variable containing the API key.

    Returns:
        The credentials object.

    Raises:
        ValueError: If the environment variable is not set.
    """
    api_key = os.environ.get(environment)
    if not api_key:
        raise ValueError(
            f"{environment} environment variable not set. Please set your API key."
        )

    credential = service_account.Credentials.from_service_account_info(
        json.loads(api_key),
        scopes=['https://www.googleapis.com/auth/chronicle-backstory']
    )
    request = Request()
    credential.refresh(request)
    return credential


def create_list(
    credentials,
    name: str,
    description: str,
    lines: List[str],
    content_type: str = "CONTENT_TYPE_DEFAULT_STRING",
) -> Mapping[str, Any]:
    """Creates a new reference list in Chronicle.

    Args:
        credentials: Authorized session credentials for HTTP requests.
        name: Unique name for the list.
        description: Description of the list.
        lines: List of line items.
        content_type: Type of list content (optional).

    Returns:
        The created list data.

    Raises:
        requests.exceptions.HTTPError: If the HTTP request resulted in an error
            (response.status_code >= 400).
    """
    url = "https://backstory.googleapis.com/v2/lists"
    body = {
        "name": name,
        "description": description,
        "lines": lines,
        "content_type": content_type,
    }

    response = requests.post(
        url,
        headers={"Authorization": f"Bearer {credentials.token}"},
        json=body,
    )

    if response.status_code >= 400:
        print(response.text)
        response.raise_for_status()

    return response.json()



def create_reference_list_tool(
        environment: str,
        name: str,
        lines: List[str],
        description: str,
) -> Dict[str, Any]:
    """Creates a new reference list in Chronicle.

    Args:
        environment: The environment from which to fetch credentials (e.g., 'TOMPEREZ_API').
        name: Unique name for the list.
        lines: List of line items.
        description: Description of the list.

    Returns:
        dict: status and result or error message.
    """
    try:
        if not name.strip():
            return {"status": "error", "error_message": "List name cannot be empty."}
        if not description.strip():
            return {"status": "error", "error_message": "List description cannot be empty."}
        if lines is None:
             return {"status": "error", "error_message": "List lines cannot be null."}
        if not isinstance(lines, list):
            if not all(isinstance(item, str) for item in lines):
                 return {"status": "error", "error_message": "All items in lines must be strings."}
            return {"status": "error", "error_message": "Lines must be a list of strings."}


        credentials = get_chronicle_credentials(environment)
        result = create_list(credentials, name, description, lines,  "CONTENT_TYPE_DEFAULT_STRING")
        return {"status": "success", "reference_list": result}
    except requests.exceptions.HTTPError as e:
        error_details = f"HTTP error creating list: {e}"
        if e.response is not None:
            error_details += f" Response: {e.response.text}"
        return {"status": "error", "error_message": error_details}
    except ValueError as e:
        return {"status": "error", "error_message": str(e)}
    except Exception as e:
        return {"status": "error", "error_message": f"An unexpected error occurred ({type(e).__name__}): {e}"}