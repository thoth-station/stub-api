# Stub API

This is a project demonstrating the basic structure of a API Service as used by the Thoth-Station.

## run the API locally

`DEBUG=1 STUB_API_APP_SECRET_KEY=start123 gunicorn stub.entrypoint:app -p 8000`