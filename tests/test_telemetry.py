import os
from pathlib import Path

from amina.telemetry import _V4_INGEST_HEADER, setup_langfuse

_SRC = Path(__file__).resolve().parents[1] / "src"


def test_langfuse_noop_without_keys(monkeypatch) -> None:
    monkeypatch.delenv("LANGFUSE_PUBLIC_KEY", raising=False)
    monkeypatch.delenv("LANGFUSE_SECRET_KEY", raising=False)
    monkeypatch.delenv("LANGFUSE_BASE_URL", raising=False)
    monkeypatch.delenv("LANGFUSE_HOST", raising=False)
    assert setup_langfuse() is None


def test_v4_otlp_endpoint_and_header(monkeypatch) -> None:
    monkeypatch.setenv("LANGFUSE_PUBLIC_KEY", "pk-test")
    monkeypatch.setenv("LANGFUSE_SECRET_KEY", "sk-test")
    monkeypatch.setenv("LANGFUSE_BASE_URL", "https://cloud.langfuse.com")
    provider = setup_langfuse(metadata={"langfuse.session.id": "room-1"})
    assert provider is not None

    assert os.environ["OTEL_EXPORTER_OTLP_ENDPOINT"].endswith("/api/public/otel")
    assert os.environ["OTEL_EXPORTER_OTLP_TRACES_ENDPOINT"].endswith(
        "/api/public/otel/v1/traces"
    )
    headers = os.environ["OTEL_EXPORTER_OTLP_HEADERS"]
    assert _V4_INGEST_HEADER in headers
    assert "Authorization=Basic " in headers
    assert "/api/public/ingestion" not in os.environ["OTEL_EXPORTER_OTLP_ENDPOINT"]
    provider.shutdown()


def test_no_deprecated_langfuse_apis_in_src() -> None:
    banned = (
        "/api/public/ingestion",
        "set_current_trace_io",
        "set_trace_io",
        "setActiveTraceIO",
        "langfuse.trace.input",
        "langfuse.trace.output",
    )
    hits: list[str] = []
    for path in _SRC.rglob("*.py"):
        text = path.read_text(encoding="utf-8")
        for token in banned:
            if token in text:
                hits.append(f"{path}: {token}")
    assert hits == []


def test_session_id_passed_at_every_entrypoint() -> None:
    agents = list((_SRC / "amina").rglob("agent*.py"))
    agents += list((_SRC / "alans_mujo_v3").rglob("agent.py"))
    assert agents
    missing = []
    for path in agents:
        text = path.read_text(encoding="utf-8")
        if "setup_langfuse" not in text:
            continue
        if '"langfuse.session.id"' not in text and "'langfuse.session.id'" not in text:
            missing.append(str(path))
    assert missing == []
