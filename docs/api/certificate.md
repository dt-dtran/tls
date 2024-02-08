# Certificate Management Endpoints

## Endpoint: /api/certificates/

### Method: POST

Create Certificate
Parameters: JSON Request of Account ID

```json
"account_id": "b0bcd211-514d-480a-99c4-d358496fdf96"
```

Results: JSON object of certificate to deserialized into data form for DB.

- httpbin POST response sent
- datetime is in UTC format.

```json
{
  "id": 1,
  "account_id": "b0bcd211-514d-480a-99c4-d358496fdf96",
  "is_active": false,
  "private_key": "---BEGIN PRIVATE KEY--- ---END PRIVATE KEY---",
  "certificate_body": "---BEGIN CERTIFICATE--- ---END CERTIFICATE---",
  "created_at": "2023-08-20T18:41:30.755440",
  "deleted_at": "2023-08-20T18:41:30.755440"
}
```

### Method: GET

Get all certificates

- Parameters: None
- Response: JSON Object List of Certificates

## Endpoint: /api/certificates/{certificate_id}

### Method: GET

Get a specific certificate by certificate ID

- Parameters: JSON Request of Certificate ID
- Response: JSON Object of a certificate

## Endpoint: /api/certificates/{account_id}/

### Method: GET

Get certificates by Account ID

- Parameters: JSON Request of Account ID (UUID string)
  - Since Account ID is an UUID format, Account is coverted to str.
- Response: JSON Object List of certificates belonging to that Account ID

## Endpoint: /api/certificates/{certificate_id}/deactivate/

### Method: PATCH

- Parameters: JSON Request of Certificate ID
  - is_active becomes false
- Response: JSON Object of the certificate
  - httpbin response sent

## Endpoint: /api/certificate/{certificate_id}/activate/

### Method: PATCH

- Parameters: JSON Request of Certificate ID
  - is_active becomes true
- Response: JSON Object of the certificate
  - httpbin response sent
