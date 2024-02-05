# Account Management Endpoints

## Endpoint: /api/accounts/

### Method: POST

Create Account

Parameters: JSON request

```json
{
  "email": "string",
  "password": "string",
  "first_name": "string",
  "last_name": "string"
}
```

Results: JSON object

```json
{
  "message": "Account created"
}
```

### Method: GET

Get all accounts

Results: JSON object

```json
[
  {
    "id": 1,
    "account_id": "b0bcd211-514d-480a-99c4-d358496fdf96",
    "email": "email@provider.com",
    "password": "$5$rounds=535000$Gv/kQYMDlgR2QpUu$5Mxy9R4P7oHZKsJJRv544DisFMI6O1dtj5qpHHlDch4",
    "first_name": "Diana",
    "last_name": "T"
  }
]
```

## Endpoint: /api/accounts/{account_id}

### Method: GET

Get account by account_id. Account ID is in UUID format.

Parameters: JSON request

```json
"account_id": "b0bcd211-514d-480a-99c4-d358496fdf96"
```

Results: JSON object

```json
{
  "id": 1,
  "account_id": "b0bcd211-514d-480a-99c4-d358496fdf96",
  "email": "email@provider.com",
  "password": "$5$rounds=535000$Gv/kQYMDlgR2QpUu$5Mxy9R4P7oHZKsJJRv544DisFMI6O1dtj5qpHHlDch4",
  "first_name": "Diana",
  "last_name": "T"
}
```

### Method: DELETE

Parameters: JSON request

```json
"account_id": "b0bcd211-514d-480a-99c4-d358496fdf96"
```

Results: JSON object

```json
{
  "message": "Account deleted"
}
```
