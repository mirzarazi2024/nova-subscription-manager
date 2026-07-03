# Security Policy

## Secrets
Never commit production secrets. The following files are intentionally ignored:

- `backend/.env`
- `backend/config/panels.json`
- `.env*` except examples

Panel API keys must be stored encrypted via the Dashboard or `make setup-panels`.

## Hiddify API
For the uploaded Hiddify OpenAPI schema, the required API key header is:

```http
Hiddify-API-Key: <API_KEY>
```

Do not use direct database access to Hiddify. NSM must integrate only through Hiddify REST APIs.

## Reporting vulnerabilities
Open a private GitHub security advisory or contact the maintainers directly.
