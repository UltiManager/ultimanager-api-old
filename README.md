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

#### `DJANGO_ALLOWED_HOSTS`

Default: `''`

A comma separated list of hostnames allowed to access the application. This is only required when debug mode is disabled.

#### `DJANGO_DEBUG`

Default: `false`

Setting this to `true` (case insensitive) will enable Django's debug mode.

#### `DJANGO_SECRET_KEY`

Default: `secret`\*

The secret key Django uses for certain security operations.

\* The key is only set to a default if debug mode is enabled. This is to avoid having a default secret key in a production environment.
