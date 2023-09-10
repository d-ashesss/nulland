# Note taking API

REST API backend for note taking application.

[![test status](https://github.com/d-ashesss/nulland/actions/workflows/test.yml/badge.svg?branch=main)](https://github.com/d-ashesss/nulland/actions/workflows/test.yml)
[![MIT license](https://img.shields.io/github/license/d-ashesss/nulland?color=blue)](https://opensource.org/licenses/MIT)
[![latest tag](https://img.shields.io/github/v/tag/d-ashesss/nulland?include_prereleases&sort=semver)](https://github.com/d-ashesss/nulland/tags)
![feline reference](https://img.shields.io/badge/may%20contain%20cat%20fur-%F0%9F%90%88-blueviolet)

## Running the app

To run the app first you must install the dependencies from requirements.txt then use Uvicorn to run the app.

```bash
pip install -r requirements.txt
python -m uvicorn app.main:app
```

Alternalively, to run in Docker (provide environment variables as needed):

```bash
docker run -p 8000:8000 -e 'DATABASE_URI=postgresql://postgres:postpwd@localhost' -e 'AUTH_OPENID_CONFIGURATION_URL=https://accounts.google.com/.well-known/openid-configuration' ashesss/nulland:latest
```

Or even with docker compose, configure environment in `docker-compose.override.yml` (see [example](https://github.com/d-ashesss/nulland/wiki/example-docker%E2%80%90compose.override.yml)), then simply run:
```bash
docker-compose up
```

## Configuration

### Authentication

The API handles authentication using JWT tokens. The token is passed in the `Authorization` header as a bearer token. It is possible to use OIDC service like [Auth0](https://auth0.com) to obtain the token and then use it with this API. It is required to provide the app with the URL to the OIDC discovery documents in the `AUTH_OPENID_CONFIGURATION_URL` environment variable.

### Database

The API uses PostgreSQL database. The connection string must be passed in the `DATABASE_URL` environment variable.

### Logging

To get the log format compatible with Google Cloud structured logging, set the `LOG_FORMAT` environment variable to `json`.

### Event logging

Application is able to post events to Kafka topic. To configure this feature set `EVENT_PRODUCER` environment variable to `kafka` and the hostname of Kafka server in `KAFKA_BOOTSTRAP_SERVERS` variable. Additionaly, `KAFKA_SASL_USERNAME` and `KAFKA_SASL_PASSWORD` must be set if Kafka server requires authentication.

### CORS

To configure CORS to allow access from a specific domain, set the `CORS_ALLOWED_ORIGINS` environment variable to JSON-formatted list of allowed URLs,
for example `CORS_ALLOWED_ORIGINS='["http://localhost:5000"]'`.

## API documentation

OpenAPI documentation is available at `/docs` endpoint.
