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

"""Implementation of API v1."""

import logging
import json
import time

import requests
import connexion
import jaeger_client
from connexion import NoContent

from opentracing_instrumentation.client_hooks import install_all_patches

from stub import __version__
from configuration import Configuration

_LOGGER = logging.getLogger(__name__)


def info_get():
    with Configuration.tracer.start_span("info_get") as span:
        span.log_kv({"event": "info_get", "stub_api_version": __version__})

        # Automatically trace all requests made with 'requests' library.
        install_all_patches()

        with Configuration.tracer.start_span("google_query", child_of=span) as google_query_span:
            google_query_span.log_kv({"event": "query_google"})
            url = "http://google.com/"
            # Make the actual request to webserver.
            requests.get(url)

        return (
            {
                "version": __version__,
                "connexionVersion": connexion.__version__,
                "jaegerClientVersion": jaeger_client.__version__,
            },
            200,
            {"x-thoth-stub-api-version": __version__},
        )
