# dgpt-api

A tiny, dependency-free Python smoke test for a DeutschlandGPT API endpoint.

## Tech stack

- Python 3.9+
- Python standard library only (no package installation)

## Run

Set the API token in an environment variable (if required), then pass the full endpoint URL:

```sh
export DEUTSCHLANDGPT_API_KEY="your-token"
python3 test_api.py "https://your-api-host.example/path"
```

For a JSON POST request:

```sh
python3 test_api.py "https://your-api-host.example/path" --method POST --json '{"input":"hello"}'
```

The endpoint and request schema depend on your API setup. The script prints the HTTP status and response body, exits with 0 for a 2xx response, 1 for an HTTP error, and 2 for a request/usage error. It never prints the bearer token.
