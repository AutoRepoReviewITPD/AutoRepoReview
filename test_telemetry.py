#!/usr/bin/env python3
"""Simple test script to verify OpenTelemetry traces are being sent."""

import os
import time
from app.telemetry import setup_telemetry
from opentelemetry import trace

# Set the OTLP endpoint
os.environ.setdefault("OTEL_EXPORTER_OTLP_ENDPOINT", "http://localhost:4318")

# Initialize telemetry
setup_telemetry()

# Get tracer
tracer = trace.get_tracer(__name__)

print("Sending test traces...")

# Create a test span
with tracer.start_as_current_span("test_operation") as span:
    span.set_attribute("test.attribute", "test_value")
    span.set_attribute("test.number", 42)
    print("Created test span with attributes")

    # Create a child span
    with tracer.start_as_current_span("test_child_operation") as child_span:
        child_span.set_attribute("child.attribute", "child_value")
        print("Created child span")
        time.sleep(0.1)  # Simulate some work

print("Test traces sent! Check Grafana/Tempo to see if they appear.")
print("Wait a few seconds for traces to be processed...")
