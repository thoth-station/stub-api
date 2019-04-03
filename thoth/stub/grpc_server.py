#!/usr/bin/env python3
# Stub
# Copyright(C) 2019 Christoph Görn
#
# This program is free software: you can redistribute it and / or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""Thoth Stub gRPC server."""

import os

from concurrent import futures
import time
import math
import logging

import grpc


import opentracing
from jaeger_client import Config as JaegerConfig
from jaeger_client.metrics.prometheus import PrometheusMetricsFactory
from jaeger_client import Config

from grpc_opentracing import open_tracing_server_interceptor
from grpc_opentracing.grpcext import intercept_server

from thoth.common import init_logging

from thoth.stub import __version__
from thoth.stub.configuration import Configuration, init_jaeger_tracer

import thoth.stub.api as api
import thoth.stub.stub_pb2 as stub_pb2
import thoth.stub.stub_pb2_grpc as stub_pb2_grpc


# Configure global application logging using Thoth's init_logging.
init_logging(logging_env_var_start="STUB_LOG_")

_LOGGER = logging.getLogger("stub")
_LOGGER.setLevel(logging.DEBUG if bool(int(os.getenv("STUB_DEBUG", 0))) else logging.INFO)

_LOGGER.info(f"This is Stub gRPC server v{__version__}")
_LOGGER.debug("DEBUG mode is enabled!")


_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class StubServicer(stub_pb2_grpc.StubServicer):
    """Provides methods that implement functionality of the Stub gRPC server."""

    def __init__(self, tracer):
        self._tracer = tracer

    def Info(self, request, context):
        versions = api.info.info_response()

        with self._tracer.start_span("stub_server_span", child_of=context.get_active_span().context):
            return stub_pb2.InfoResponse(
                version=versions["version"],
                connexionVersion=versions["connexionVersion"],
                jaegerClientVersion=versions["jaegerClientVersion"],
            )


def serve():
    Configuration.tracer = init_jaeger_tracer("stub_api")

    tracer_interceptor = open_tracing_server_interceptor(Configuration.tracer)

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    server = intercept_server(server, tracer_interceptor)

    stub_pb2_grpc.add_StubServicer_to_server(StubServicer(Configuration.tracer), server)
    server.add_insecure_port("[::]:8443")
    server.start()

    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)

    Configuration.tracer.close()


if __name__ == "__main__":
    serve()
