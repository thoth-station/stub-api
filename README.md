# Stub API

This is a project demonstrating the basic structure of a API Service as
used by the Thoth-Station. The service itself exports Prometheus metrics,
and is instrumented to send Jaeger tracing.

The gRPC server is using a self signed TLS certificate.

## installing dependencies

You should know it by now: `pipenv install`

## run the OpenAPI Service locally

`STUB_DEBUG=1 STUB_API_APP_SECRET_KEY=start123 gunicorn thoth.stub.openapi_server:app`

## run the gRPC Service

### Generate X.509 Certificates

```shell
openssl req -newkey rsa:2048 -nodes -keyout server.key -x509 -days 365 -out server.crt -config <(
cat <<-EOF
[req]
default_bits = 2048
prompt = no
default_md = sha256
req_extensions = req_ext
distinguished_name = dn

[ dn ]
C=DE
L=Bonn
CN=stub-grpc-goern-thoth-dev.cloud.paas.psi.redhat.com

[ req_ext ]
subjectAltName = @alt_names

[ alt_names ]
DNS.1=localhost
EOF
)
```

### run locally

`STUB_DEBUG=1 STUB_API_APP_SECRET_KEY=start123 PYTHONPATH=. ./thoth/stub/grpc_server.py` Check for the hostname the demo client is communication with!

### Generate GRPC code (optinal)

You could generate all the files required for gRPC client and server: `./run_codegen.py`

### Deploy to OpenShift

The repository contains templates for deploying the Stub API to OpenShift. The TLS key and
certificate are mounted into the gRPC server pod from a secret.

## run Jaeger locally

```shell
podman run --rm -ti -e COLLECTOR_ZIPKIN_HTTP_PORT=9411 \
    -p 5775:5775/udp \
    -p 6831:6831/udp \
    -p 6832:6832/udp \
    -p 5778:5778 \
    -p 16686:16686 \
    -p 14268:14268 \
    -p 9411:9411 \
    jaegertracing/all-in-one:latest`
```
