# How to Find Traces in Tempo via Grafana

## Step-by-Step Guide

### 1. Access Grafana
- Open http://localhost:3000
- Login with `admin` / `admin`

### 2. Go to Explore
- Click **"Explore"** in the left sidebar (compass icon)

### 3. Select Tempo Datasource
- In the dropdown at the top, select **"Tempo"**

### 4. Search for Traces

**Option A: Search by Service Name**
1. In the search box, type: `{resource.service.name="autoreporeview"}`
2. Click "Run query"
3. You should see traces appear

**Option B: Search by Operation Name**
1. In the search box, type: `{name="test_operation"}` or `{name="summary_command"}`
2. Click "Run query"

**Option C: Search All Traces (Last Hour)**
1. Leave the search box empty or use: `{}`
2. Make sure the time range is set to "Last 1 hour" or "Last 15 minutes"
3. Click "Run query"

### 5. View Trace Details
- Click on any trace in the results
- You'll see the full trace with all spans and their attributes

## Common Issues

### No Traces Appearing?

1. **Check Time Range**: Make sure you're looking at the right time period
   - Traces were sent recently? Use "Last 15 minutes"
   - Traces sent earlier? Adjust the time range accordingly

2. **Verify Traces Are Being Sent**:
   ```bash
   # Run the test script again
   uv run python test_telemetry.py
   
   # Check collector logs
   docker compose logs otel-collector --tail 20
   ```

3. **Check Tempo is Receiving Data**:
   ```bash
   docker compose logs tempo --tail 20 | grep -i ingest
   ```

### Search Tips

- **Service Name**: `{resource.service.name="autoreporeview"}`
- **Operation Name**: `{name="summary_command"}`
- **Multiple Conditions**: `{resource.service.name="autoreporeview" AND name="test_operation"}`
- **Any Trace**: `{}` (empty query)

## Quick Test

Run this to generate fresh traces:
```bash
export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4318
uv run python test_telemetry.py
```

Then immediately search in Grafana with: `{resource.service.name="autoreporeview"}`

