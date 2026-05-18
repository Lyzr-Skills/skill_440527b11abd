
import io
import json
import requests
from typing import Dict, Any

TAS_API_URL = "https://tasapi-qa.movate.com/api/rrf/validate"

# Move to env variable in production
TAS_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJUQVN5c3RlbS5BcGkuQXV0aCIsImVtYWlsIjoiYWRtaW5AbW92YXRlLmNvbSIsImp0aSI6IjZkMjVkYjMyLTAxZjgtNDljOS04OTA4LWEyMzY1MDVkYzkzMCIsInVzZXJJZCI6IjEiLCJmdWxsTmFtZSI6IkFkbWluIFVzZXIiLCJodHRwOi8vc2NoZW1hcy5taWNyb3NvZnQuY29tL3dzLzIwMDgvMDYvaWRlbnRpdHkvY2xhaW1zL3JvbGUiOiJBZG1pbiIsImV4cCI6MTc3OTA5NDA5MSwiaXNzIjoiVEFTeXN0ZW0uQXBpIiwiYXVkIjoiVEFTeXN0ZW0uQXBpQ2xpZW50cyJ9.kR18giVhdmfX0kZa16h4IfjPRjwGq82KHreARwoPPWE"


def download_file(url: str) -> bytes:
    response = requests.get(
        url,
        timeout=60,
        allow_redirects=True
    )

    response.raise_for_status()

    content_type = response.headers.get("content-type", "")

    if "pdf" not in content_type.lower():
        raise Exception(
            f"Invalid content-type: {content_type}"
        )

    return response.content


def validate_rrf(
    jd_file_url: str,
    approval_file_url: str,
    rrf_data: Dict[str, Any]
):

    jd_bytes = download_file(jd_file_url)
    approval_bytes = download_file(approval_file_url)

    files = {
        "jdFile": (
            "jdFile.pdf",
            io.BytesIO(jd_bytes),
            "application/pdf"
        ),
        "approvalFile": (
            "approvalFile.pdf",
            io.BytesIO(approval_bytes),
            "application/pdf"
        )
    }

    data = {
        "rrfData": json.dumps(rrf_data)
    }

    headers = {
        "Authorization": f"Bearer {TAS_TOKEN}"
    }

    response = requests.post(
        TAS_API_URL,
        headers=headers,
        data=data,
        files=files,
        timeout=180
    )

    return {
        "success": response.ok,
        "status_code": response.status_code,
        "response": response.text
    }