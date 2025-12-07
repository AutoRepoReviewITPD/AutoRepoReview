#!/bin/bash
# Script to generate otel-collector-config.yaml from template with environment variables

set -e

TEMPLATE_FILE="otel-collector-config.yaml.template"
OUTPUT_FILE="otel-collector-config.yaml"

# Check if template exists
if [ ! -f "$TEMPLATE_FILE" ]; then
    echo "Error: Template file $TEMPLATE_FILE not found!"
    exit 1
fi

# Check if envsubst is available
if ! command -v envsubst &> /dev/null; then
    echo "Error: envsubst is not installed."
    echo "Install it with: brew install gettext (macOS) or apt-get install gettext-base (Linux)"
    exit 1
fi

# Generate config file from template
envsubst < "$TEMPLATE_FILE" > "$OUTPUT_FILE"

echo "Generated $OUTPUT_FILE from template"
echo "Make sure GRAFANA_CLOUD_OTLP_ENDPOINT and GRAFANA_CLOUD_OTLP_AUTH are set in your environment"

