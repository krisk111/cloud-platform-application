import os
from functools import lru_cache

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    ConsoleSpanExporter,
    SimpleSpanProcessor,
)


@lru_cache(maxsize=1)
def create_tracer_provider():
    resource = Resource.create(
        {
            "service.name": "cloud-platform-application",
            "deployment.environment.name": "development",
        }
    )

    provider = TracerProvider(resource=resource)

    exporter_type = os.getenv("OTEL_TRACES_EXPORTER", "console")

    if exporter_type == "console":
        provider.add_span_processor(SimpleSpanProcessor(ConsoleSpanExporter()))

    elif exporter_type == "otlp":
        endpoint = os.getenv(
            "OTEL_EXPORTER_OTLP_TRACES_ENDPOINT",
            "http://localhost:4318/v1/traces",
        )

        provider.add_span_processor(
            BatchSpanProcessor(OTLPSpanExporter(endpoint=endpoint))
        )

    else:
        raise ValueError(f"Unsupported OTEL_TRACES_EXPORTER: {exporter_type}")

    trace.set_tracer_provider(provider)

    return provider
