from google.auth.transport.requests import Request
from typing import Mapping, Any
import requests
from google.oauth2 import service_account
import json
import os


def get_chronicle_credentials(environment):
    """Retrieves Chronicle API credentials from environment variable."""
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


def verify_rule(
    credentials, rule_text: str
) -> Mapping[str, Any]:
    """Verifies that a rule is a valid YARA-L 2.0 rule without creating a new rule or evaluating it over data.

    Args:
        credentials: Authorized session creds for HTTP requests.
        rule_text: The content of the YARA-L 2.0 rule.

    Returns:
        Response message with results of whether rule was verified successfully.

    Raises:
        requests.exceptions.HTTPError: HTTP request resulted in an error
          (response.status_code >= 400).
    """
    url = "https://backstory.googleapis.com/v2/detect/rules:verifyRule"
    body = {"ruleText": rule_text}

    response = requests.post(
        url,
        headers={"Authorization": f"Bearer {credentials.token}"},
        json=body
    )

    if response.status_code >= 400:
        print(response.text)
    response.raise_for_status()
    print(response.json())
    return response.json()


def verify_rule_tool(environment: str = "default", rule_text: str = "") -> dict:
    """Verifies a detection rule's syntax and structure without creating it.

    Args:
        environment (str, optional): The environment from which to fetch credentials.
        rule_text (str): The content of the YARA-L 2.0 rule to verify.

    Returns:
        dict: status and result or error message.
    """
    try:
        if not rule_text.strip():
            return {"status": "error", "error_message": "Rule text cannot be empty."}

        credentials = get_chronicle_credentials(environment)
        result = verify_rule(credentials, rule_text)

        return {"status": "success", "verification": result}
    except requests.exceptions.HTTPError as e:
        return {"status": "error", "error_message": f"HTTP error verifying rule: {e}"}
    except ValueError as e:
        return {"status": "error", "error_message": str(e)}
    except Exception as e:
        return {"status": "error", "error_message": f"An unexpected error occurred: {e}"}
