# Note taking API

REST API backend for note taking application.

[![test status](https://github.com/d-ashesss/nulland/actions/workflows/test.yml/badge.svg?branch=main)](https://github.com/d-ashesss/nulland/actions/workflows/test.yml)
[![MIT license](https://img.shields.io/github/license/d-ashesss/nulland?color=blue)](https://opensource.org/licenses/MIT)
[![latest tag](https://img.shields.io/github/v/tag/d-ashesss/nulland?include_prereleases&sort=semver)](https://github.com/d-ashesss/nulland/tags)
![feline reference](https://img.shields.io/badge/may%20contain%20cat%20fur-%F0%9F%90%88-blueviolet)

## Authentication

The API handles authentication using JWT tokens. The token is passed in the `Authorization` header as a bearer token. It is possible to use OIDC service like [Auth0](https://auth0.com) to obtain the token and then use it with this API. It is required to provide the app with the URL to the OIDC discovery documents in the `AUTH_OPENID_CONFIGURATION_URL` environment variable.

## Database

The API uses PostgreSQL database. The connection string must be passed in the `DATABASE_URL` environment variable.

## Logging

To get the log format compatible with Google Cloud structured logging, set the `LOG_FORMAT` environment variable to `json`.
