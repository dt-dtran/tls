# Data Models

## Account Service

`Account` model is used to store Customer account data. All accounts password are encrpyed and stored as a hashed password.

<details>
<summary>Account</summary>

| name       | type        | unique | optional      |
| ---------- | ----------- | ------ | ------------- |
| id         | serial      | yes    | autogenerated |
| account_id | string UUID | yes    | autogenerated |
| email      | string      | yes    | no            |
| password   | string      | no     | no            |
| first_name | string      | no     | no            |
| last_name  | string      | no     | no            |

</details>