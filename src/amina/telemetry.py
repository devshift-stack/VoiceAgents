"""LiveKit → Langfuse via official OTLP export. No keys in this file."""

from __future__ import annotations

import base64
import logging
import os

from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.util.types import AttributeValue

log = logging.getLogger("amina.telemetry")

_V4_INGEST_HEADER = "x-langfuse-ingestion-version=4"


def setup_langfuse(metadata: dict[str, AttributeValue] | None = None):
    """Route LiveKit spans to Langfuse OTLP v4. No-op if keys are missing."""
    public_key = os.environ.get("LANGFUSE_PUBLIC_KEY")
    secret_key = os.environ.get("LANGFUSE_SECRET_KEY")
    base_url = os.environ.get("LANGFUSE_BASE_URL") or os.environ.get("LANGFUSE_HOST")
    if not public_key or not secret_key or not base_url:
        log.warning("Langfuse keys missing — traces stay local only")
        return None

    from livekit.agents.telemetry import set_tracer_provider
    from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor

    auth = base64.b64encode(f"{public_key}:{secret_key}".encode()).decode()
    otel_base = f"{base_url.rstrip('/')}/api/public/otel"
    os.environ["OTEL_EXPORTER_OTLP_ENDPOINT"] = otel_base
    os.environ["OTEL_EXPORTER_OTLP_TRACES_ENDPOINT"] = f"{otel_base}/v1/traces"
    os.environ["OTEL_EXPORTER_OTLP_HEADERS"] = (
        f"Authorization=Basic {auth},{_V4_INGEST_HEADER}"
    )
    os.environ["OTEL_EXPORTER_OTLP_TRACES_HEADERS"] = os.environ[
        "OTEL_EXPORTER_OTLP_HEADERS"
    ]
    provider = TracerProvider(resource=Resource.create({SERVICE_NAME: "livekit-agents"}))
    provider.add_span_processor(BatchSpanProcessor(OTLPSpanExporter()))
    set_tracer_provider(provider, metadata=metadata)
    return provider
