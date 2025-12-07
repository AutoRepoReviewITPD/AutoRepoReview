# Grafana Cloud Quick Start

> **Simplest Method**: See `GRAFANA_CLOUD_SIMPLE.md` for direct connection (no collector setup needed!)

## Quick Setup (3 Steps) - Using Collector

### 1. Get Your Credentials from Grafana Cloud

1. Go to https://ilnarkhasanov.grafana.net/
2. Navigate to **Connections** → **Add new connection** → Search for **"OpenTelemetry"**
3. Copy:
   - **OTLP Endpoint URL** (e.g., `https://otlp-gateway-prod-us-central-0.grafana.net/otlp`)
   - **Instance ID** and **API Key**

### 2. Create Authentication String

```bash
# Replace YOUR_INSTANCE_ID and YOUR_API_KEY with your actual values
echo -n "YOUR_INSTANCE_ID:YOUR_API_KEY" | base64
```

Copy the output (e.g., `MTIzNDU2OnlvdXItYXBpLWtleS1oZXJl`)

### 3. Configure and Start

**Option A: Use the script (Easiest)**

```bash
# Set your credentials
export GRAFANA_CLOUD_OTLP_ENDPOINT="https://otlp-gateway-prod-us-central-0.grafana.net/otlp"
export GRAFANA_CLOUD_OTLP_AUTH="MTIzNDU2OnlvdXItYXBpLWtleS1oZXJl"  # Your base64 string

# Generate config
./generate-otel-config.sh

# Restart services
docker compose restart otel-collector
```

**Option B: Manual edit**

1. Edit `otel-collector-config.yaml`
2. Uncomment the `otlp/grafana-cloud` section (lines ~25-30)
3. Replace:
   - `endpoint:` with your OTLP endpoint URL
   - `authorization: "Basic ..."` with your base64 auth string
4. Add `otlp/grafana-cloud` to the exporters lists in pipelines (traces and metrics)
5. Restart: `docker compose restart otel-collector`

### 4. Verify

```bash
# Check logs for errors
docker compose logs otel-collector --tail 20

# Run a test to generate traces
export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4318
uv run python test_telemetry.py
```

Then check your traces in Grafana Cloud at https://ilnarkhasanov.grafana.net/ → **Explore** → **Tempo**

## Example Config

After configuration, your `otel-collector-config.yaml` should have:

```yaml
exporters:
  otlp/grafana-cloud:
    endpoint: https://otlp-gateway-prod-us-central-0.grafana.net/otlp
    headers:
      authorization: "Basic MTIzNDU2OnlvdXItYXBpLWtleS1oZXJl"
    tls:
      insecure: false

service:
  pipelines:
    traces:
      exporters: [otlp/tempo, otlp/grafana-cloud, debug]
    metrics:
      exporters: [prometheus, otlp/grafana-cloud, debug]
```

## Troubleshooting

- **401/403 errors**: Check your instance ID and API key are correct
- **Connection errors**: Verify the endpoint URL is correct for your region
- **No data**: Make sure you've added `otlp/grafana-cloud` to both traces and metrics pipelines

For detailed instructions, see `GRAFANA_CLOUD_SETUP.md`

