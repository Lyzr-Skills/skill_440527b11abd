---
name: validate-rrf
description: Download JD and approval PDF files from remote asset URLs and validate RRF payloads by uploading multipart/form-data to the TAS API. Use this skill whenever the user provides asset URLs instead of local files for jdFile and approvalFile uploads.
---

# Validate RRF Skill

This skill validates TAS RRF requests when the user has:

- Remote asset URLs
- Lyzr asset URLs
- PDF links instead of local files
- Multipart upload requirements

The skill performs the following workflow:

1. Download JD PDF from asset URL
2. Download approval PDF from asset URL
3. Convert downloaded files into multipart/form-data
4. Call TAS validation API
5. Return validation response

## When To Use

Use this skill when:

- The API requires multipart file uploads
- The user only has remote asset URLs
- jdFile and approvalFile are URLs instead of filesystem paths
- TAS RRF validation API must be called
- Files need to be uploaded dynamically

## Input Format

```json
{
  "jd_file_url": "https://url-shortner.studio.lyzr.ai/14fed814",
  "approval_file_url": "https://url-shortner.studio.lyzr.ai/14fed815",
  "rrf_data": {
    "userEmail": "test.khan@movate.com",
    "userName": "test Khan"
  }
}
```

Execution Steps
Step 1 — Download Files

Download both:

JD PDF
Approval PDF

from remote URLs.

Verify:

HTTP status code
content-type
file size
Step 2 — Build Multipart Request

Construct multipart/form-data payload:

jdFile
approvalFile
rrfData

rrfData must be serialized JSON string.

Step 3 — Call TAS API

POST request:

https://tasapi-qa.movate.com/api/rrf/validate

Headers:

Authorization: Bearer <TOKEN>
Step 4 — Return Response

Return:

status code
success flag
response body
validation errors if any
Important Rules
Always preserve multipart upload format
Never send URLs directly as file fields
Always download URLs first
Validate PDF MIME type before upload
Handle redirects automatically
Support large PDF uploads
Use request timeout
Return meaningful errors
Error Handling

Handle:

Invalid URLs
Timeout errors
Non-PDF content
TAS API failures
Authentication errors
Multipart upload failures
Security Guidelines
Never log bearer tokens
Never expose sensitive headers
Mask confidential fields in logs
Validate external URLs before downloading
Use HTTPS URLs only
Example Use Cases
Example 1

User has:

jdFile=https://url-shortner.studio.lyzr.ai/abc123

Instead of local filesystem path.

Example 2

Agent receives:

{
  "jd_file_url": "...",
  "approval_file_url": "...",
  "rrf_data": {...}
}

and must transform them into multipart uploads.

Script

Use: scripts/validate_rrf.py for execution logic.
