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

"""Thoth Stub gRPC client."""

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

import thoth.stub.stub_pb2 as stub_pb2
import thoth.stub.stub_pb2_grpc as stub_pb2_grpc


# Configure global application logging using Thoth's init_logging.
init_logging(logging_env_var_start="STUB_LOG_")

_LOGGER = logging.getLogger("stub")
_LOGGER.setLevel(logging.DEBUG if bool(int(os.getenv("STUB_DEBUG", 0))) else logging.INFO)

_LOGGER.info(f"This is Stub gRPC client v{__version__}")
_LOGGER.debug("DEBUG mode is enabled!")


def main():
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = stub_pb2_grpc.StubStub(channel)
        e = stub_pb2.Empty()

        info = stub.Info(e)

        print(info)


if __name__ == "__main__":
    main()

