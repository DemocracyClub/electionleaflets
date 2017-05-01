# Configuration

The Election Leaflets app is configured via the following environment variables:

| Variable name              | Description                                                                                                                            | Default value                                    |
|:---------------------------|:---------------------------------------------------------------------------------------------------------------------------------------|:-------------------------------------------------|
| `ADMINS`                   | Semicolon separated list of admins, with their names and emails separated by commas. eg. `Alice,alice@example.com;Bob,bob@example.com` | `Admin,admin@example.com`                        |
| `AWS_ACCESS_KEY_ID`        | AWS Credentials                                                                                                                        |                                                  |
| `AWS_S3_FILE_OVERWRITE`    | Overwrite files in S3 as they're uploaded. Use in production only.                                                                     | `False`                                          |
| `AWS_S3_HOST`              | S3 Host if different from US Standard                                                                                                  | `s3-eu-west-1.amazonaws.com`                     |
| `AWS_SECRET_ACCESS_KEY`    | AWS Credentials                                                                                                                        |                                                  |
| `AWS_STORAGE_BUCKET_NAME`  | S3 Bucket to store images in                                                                                                           | Not configured                                   |
| `DATABASE_URL`             | A connection string. `postgres://` is replaced with `postgis://` to set the correct engine.                                            | `postgres://postgres@localhost/electionleaflets` |
| `DEBUG`                    | Django debug                                                                                                                           | False                                            |
| `DEFAULT_FROM_EMAIL`       | Address the Report Abuse form is sent from                                                                                             | `team@electionleaflets.org`                      |
| `EMAIL_RECIPIENT`          | Address the Report Abuse form is sent to                                                                                               | `team@electionleaflets.org`                      |
| `GOOGLE_ANALYTICS_ENABLED` |                                                                                                                                        | False                                            |
| `MAINTENANCE_MODE`         | Shows a Maintenance message                                                                                                            | False                                            |
| `REDIS_PROVIDER`           | Name of an environment variable to get a Redis key from, eg. `REDISTOGO_URL`.                                                          | `REDIS_URL`                                      |
| `REPORT_EMAIL_SUBJECT`     | Subject for the Report Abuse form email                                                                                                | `ELECTION LEAFLET REPORT`                        |
| `SECRET_KEY`               | Django Secret Key                                                                                                                      | `INSECURE`                                       |
