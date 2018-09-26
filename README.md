# UltiManager API

API for managing an ultimate Frisbee team.

## Development

### Environment Variables

When using `pipenv` to execute commands, the local `.env` file will be loaded to populate environment variables. The `.env` file for a basic development environment would look like:

```
DJANGO_DEBUG=true
```

## Deployment

### Environment Variables

The following environment variables can be used to configure the application.

Note that if any of `DJANGO_DB_NAME`, `DJANGO_DB_PASSWORD`, or `DJANGO_DB_USER` are not set, we will fall back to a local Sqlite database.

#### `DJANGO_ALLOWED_HOSTS`

Default: `''`

A comma separated list of hostnames allowed to access the application. This is only required when debug mode is disabled.

#### `DJANGO_DB_HOST`

Default: `localhost`

The host for the Postgres DB to connect to.

#### `DJANGO_DB_NAME`

Default: `''`

The name of the database to use.

#### `DJANGO_DB_PASSWORD`

Default: `''`

The password to use when connecting to the Postgres database.

#### `DJANGO_DB_PORT`

Default: `5432`

The port to use when connecting to the Postgres database.

#### `DJANGO_DB_USER`

Default: `''`

The name of the user to connect to the Postgres database as.

#### `DJANGO_DEBUG`

Default: `false`

Setting this to `true` (case insensitive) will enable Django's debug mode.

#### `DJANGO_SECRET_KEY`

Default: `secret`\*

The secret key Django uses for certain security operations.

\* The key is only set to a default if debug mode is enabled. This is to avoid having a default secret key in a production environment.

#### `DJANGO_SES_ENABLED`

Default: `false`

Setting this to `true` (case insensitive) will enabled sending of emails using AWS SES. If this option is enabled, AWS credentials authorizing SES use must be accessible to the server process. The easiest way to accomplish this is by running the server on an EC2 instance with a role that grants the appropriate permissions, but can also be accomplished using any of the methods described in [the `boto` documentation][boto-credentials].

## Testing

Tests are run on each push using Travis CI.


[boto-credentials]: https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html#configuring-credentials
