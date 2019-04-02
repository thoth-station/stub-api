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

import stub_pb2
import stub_pb2_grpc

import opentracing
from jaeger_client import Config as JaegerConfig
from jaeger_client.metrics.prometheus import PrometheusMetricsFactory

from thoth.common import init_logging

from configuration import Configuration

import api

# Configure global application logging using Thoth's init_logging.
init_logging(logging_env_var_start="STUB_LOG_")

_LOGGER = logging.getLogger("stub")
_LOGGER.setLevel(logging.DEBUG if bool(int(os.getenv("STUB_DEBUG", 0))) else logging.INFO)

_LOGGER.info(f"This is Stub gRPC server v{__version__}")
_LOGGER.debug("DEBUG mode is enabled!")


_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class StubServicer(stub_pb2_grpc.StubServicer):
    """Provides methods that implement functionality of the Stub gRPC server."""

    def Info(self, request, context):
        _info = get_feature(self.db, request)
        if _info is None:
            return stub_pb2.Info()
        else:
            return _info


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    stub_pb2_grpc.add_StubServicer_to_server(StubServicer(), server)
    server.add_insecure_port("[::]:50051")
    server.start()

    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == "__main__":
    serve()
