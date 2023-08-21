# Note taking API

REST API backend for note taking application.

[![MIT license](https://img.shields.io/github/license/d-ashesss/nulland?color=blue)](https://opensource.org/licenses/MIT)
[![latest tag](https://img.shields.io/github/v/tag/d-ashesss/nulland?include_prereleases&sort=semver)](https://github.com/d-ashesss/nulland/tags)
![feline reference](https://img.shields.io/badge/may%20contain%20cat%20fur-%F0%9F%90%88-blueviolet)

## Authentication

The API handles authentication using JWT tokens. The token is passed in the `Authorization` header as a bearer token. It is possible to use OIDC service like 0Auth to obtain the token and then use it with this API. It is required to provide the app with the URL to the OIDC public key in the `AUTH_JWKS_URL` environment variable to make it able to verify the token.

## Database

The API uses PostgreSQL database. The connection string must be passed in the `DATABASE_URL` environment variable.
