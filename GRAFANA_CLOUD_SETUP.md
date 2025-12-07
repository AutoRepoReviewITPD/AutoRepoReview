# Grafana Cloud Setup Guide

This guide explains how to configure your OpenTelemetry setup to send traces and metrics to Grafana Cloud.

## Step 1: Get Your Grafana Cloud Credentials

1. **Log in to Grafana Cloud**: https://ilnarkhasanov.grafana.net/
2. **Navigate to Connections**:
   - Click on the **hamburger menu** (☰) in the top left
   - Go to **Connections** → **Add new connection**
   - Search for **"OpenTelemetry"** or **"OTLP"**
3. **Get Your OTLP Endpoint and Credentials**:
   - You'll see an OTLP endpoint URL (e.g., `https://otlp-gateway-prod-us-central-0.grafana.net/otlp`)
   - You'll also get an **Instance ID** and **API Key**
   - The authentication is typically in the format: `Basic <base64(instance_id:api_key)>`

## Step 2: Create Authentication String

You need to create a Base64-encoded string for authentication:

```bash
# Format: instance_id:api_key
# Example: 123456:your-api-key-here

# Create the auth string (replace with your actual values)
echo -n "YOUR_INSTANCE_ID:YOUR_API_KEY" | base64
```

This will output something like: `MTIzNDU2OnlvdXItYXBpLWtleS1oZXJl`

## Step 3: Set Environment Variables

Create a `.env` file in the project root (or export them in your shell):

```bash
# Grafana Cloud OTLP Endpoint (for traces and metrics)
export GRAFANA_CLOUD_OTLP_ENDPOINT="https://otlp-gateway-prod-us-central-0.grafana.net/otlp"

# Grafana Cloud Authentication (Base64 encoded instance_id:api_key)
export GRAFANA_CLOUD_OTLP_AUTH="MTIzNDU2OnlvdXItYXBpLWtleS1oZXJl"
```

**Or create a `.env` file:**
```bash
GRAFANA_CLOUD_OTLP_ENDPOINT=https://otlp-gateway-prod-us-central-0.grafana.net/otlp
GRAFANA_CLOUD_OTLP_AUTH=MTIzNDU2OnlvdXItYXBpLWtleS1oZXJl
```

## Step 4: Update Collector Configuration

Edit `otel-collector-config.yaml` and replace the placeholders with your actual Grafana Cloud credentials:

**Method 1: Use the generation script (Recommended)**

```bash
# Set your environment variables
export GRAFANA_CLOUD_OTLP_ENDPOINT="https://otlp-gateway-prod-us-central-0.grafana.net/otlp"
export GRAFANA_CLOUD_OTLP_AUTH="MTIzNDU2OnlvdXItYXBpLWtleS1oZXJl"  # Your base64 encoded auth

# Generate the config file
./generate-otel-config.sh
```

**Method 2: Manually edit the config file**

Edit `otel-collector-config.yaml` and replace the placeholders:

```yaml
exporters:
  otlp/grafana-cloud:
    endpoint: https://otlp-gateway-prod-us-central-0.grafana.net/otlp
    headers:
      authorization: "Basic MTIzNDU2OnlvdXItYXBpLWtleS1oZXJl"
```

## Step 5: Restart Services

```bash
docker compose down
docker compose up -d
```

## Step 6: Verify Data is Being Sent

1. **Check Collector Logs**:
   ```bash
   docker compose logs otel-collector --tail 50
   ```
   Look for any errors related to Grafana Cloud connection.

2. **Check Grafana Cloud**:
   - Go to https://ilnarkhasanov.grafana.net/
   - Navigate to **Explore** → Select **Tempo** or **Prometheus** datasource
   - Search for traces/metrics from your service

## Alternative: Send Directly from Application

You can also configure your application to send directly to Grafana Cloud:

```bash
export OTEL_EXPORTER_OTLP_ENDPOINT="https://otlp-gateway-prod-us-central-0.grafana.net/otlp/v1/traces"
export OTEL_EXPORTER_OTLP_HEADERS="authorization=Basic MTIzNDU2OnlvdXItYXBpLWtleS1oZXJl"
```

Then update `app/telemetry/setup.py` to use headers for authentication.

## Troubleshooting

### No data appearing in Grafana Cloud

1. **Check authentication**:
   - Verify your Base64 encoding is correct
   - Ensure instance ID and API key are correct

2. **Check endpoint URL**:
   - Make sure the endpoint URL is correct for your region
   - Verify it's accessible from your network

3. **Check collector logs**:
   ```bash
   docker compose logs otel-collector | grep -i grafana
   ```

4. **Verify network connectivity**:
   ```bash
   docker compose exec otel-collector wget -O- https://otlp-gateway-prod-us-central-0.grafana.net/otlp
   ```

### Authentication Errors

If you see 401/403 errors:
- Double-check your instance ID and API key
- Verify the Base64 encoding
- Make sure there are no extra spaces in the auth string

## Finding Your OTLP Endpoint

The exact endpoint URL depends on your Grafana Cloud region:
- US Central: `https://otlp-gateway-prod-us-central-0.grafana.net/otlp`
- EU West: `https://otlp-gateway-prod-eu-west-0.grafana.net/otlp`
- Other regions: Check your Grafana Cloud dashboard

Check your Grafana Cloud account settings or the OTLP connection setup page for the exact endpoint.

