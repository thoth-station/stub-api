# Stub API

This is a project demonstrating the basic structure of a API Service as
used by the Thoth-Station. The service itself exports Prometheus metrics,
and is instrumented to send Jaeger tracing.

## run the API locally

`STUB_DEBUG=1 STUB_API_APP_SECRET_KEY=start123 gunicorn thoth.stub.openapi_server:app`

## run Jaeger locally

```shell
docker run -d -e COLLECTOR_ZIPKIN_HTTP_PORT=9411 \
    -p 5775:5775/udp \
    -p 6831:6831/udp \
    -p 6832:6832/udp \
    -p 5778:5778 \
    -p 16686:16686 \
    -p 14268:14268 \
    -p 9411:9411 \
    jaegertracing/all-in-one:latest`
```

# Generate GRPC code

`./run_codegen.py`