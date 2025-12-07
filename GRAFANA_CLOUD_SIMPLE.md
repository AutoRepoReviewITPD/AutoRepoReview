# Connect to Grafana Cloud - Simple Setup

The simplest way to send traces directly to Grafana Cloud - no collector configuration needed!

## Step 1: Get Your Credentials

1. Go to https://ilnarkhasanov.grafana.net/
2. Navigate to **Connections** → **Add new connection** → **OpenTelemetry**
3. You'll see:
   - **OTLP Endpoint**: `https://otlp-gateway-prod-<region>.grafana.net/otlp`
   - **Instance ID**: Your instance ID
   - **API Key**: Your API key

## Step 2: Create Authentication String

```bash
# Replace with your actual Instance ID and API Key
echo -n "YOUR_INSTANCE_ID:YOUR_API_KEY" | base64
```

Copy the output (e.g., `MTIzNDU2OnlvdXItYXBpLWtleS1oZXJl`)

## Step 3: Set Environment Variables and Run

That's it! Just set these environment variables:

```bash
# Set Grafana Cloud endpoint (add /v1/traces will be added automatically)
export OTEL_EXPORTER_OTLP_ENDPOINT="https://otlp-gateway-prod-us-central-0.grafana.net/otlp"

# Set authentication header
export OTEL_EXPORTER_OTLP_HEADERS="authorization=Basic MTIzNDU2OnlvdXItYXBpLWtleS1oZXJl"

# Run your application
uv run autoreporeview summary <path> <commit_a> <commit_b>
```

## Or Create a `.env` File

Create a `.env` file in the project root:

```bash
OTEL_EXPORTER_OTLP_ENDPOINT=https://otlp-gateway-prod-us-central-0.grafana.net/otlp
OTEL_EXPORTER_OTLP_HEADERS=authorization=Basic MTIzNDU2OnlvdXItYXBpLWtleS1oZXJl
```

Then load it before running:

```bash
export $(cat .env | xargs)
uv run autoreporeview summary <path> <commit_a> <commit_b>
```

## View Your Traces

1. Go to https://ilnarkhasanov.grafana.net/
2. Click **Explore** (compass icon)
3. Select **Tempo** datasource
4. Search for: `{resource.service.name="autoreporeview"}`

## That's It!

No collector configuration, no Docker changes - just set two environment variables and your traces go directly to Grafana Cloud!

## Switching Between Local and Cloud

- **Local (default)**: Don't set the environment variables, or set:
  ```bash
  export OTEL_EXPORTER_OTLP_ENDPOINT="http://localhost:4318"
  unset OTEL_EXPORTER_OTLP_HEADERS
  ```

- **Grafana Cloud**: Set both `OTEL_EXPORTER_OTLP_ENDPOINT` and `OTEL_EXPORTER_OTLP_HEADERS`

## Troubleshooting

- **401/403 errors**: Check your Instance ID and API Key are correct in the base64 string
- **Connection errors**: Verify the endpoint URL matches your Grafana Cloud region
- **No traces**: Make sure you've run the application after setting the environment variables

