# OpenTelemetry and Grafana Setup

This project includes OpenTelemetry instrumentation for observability and Grafana for visualization.

## Architecture

The observability stack consists of:
- **OpenTelemetry SDK**: Instrumented in the Python application
- **OpenTelemetry Collector**: Receives and processes telemetry data
- **Tempo**: Stores distributed traces
- **Prometheus**: Stores metrics
- **Grafana**: Visualizes traces and metrics

## Quick Start

### 1. Start the Observability Stack

Start all services using Docker Compose:

```bash
docker-compose up -d
```

This will start:
- OpenTelemetry Collector on ports 4317 (gRPC) and 4318 (HTTP)
- Tempo on port 3200
- Prometheus on port 9090
- Grafana on port 3000

### 2. Access Grafana

1. Open your browser and navigate to `http://localhost:3000`
2. Login with:
   - Username: `admin`
   - Password: `admin`
3. The Prometheus and Tempo datasources are automatically configured
4. Navigate to Dashboards to view the AutoRepoReview dashboard

### 3. Run the Application with Telemetry

The application automatically initializes OpenTelemetry on startup. You can configure it using environment variables:

```bash
# Optional: Set custom service name (default: autoreporeview)
export OTEL_SERVICE_NAME=autoreporeview

# Optional: Set OTLP endpoint (default: http://localhost:4318)
export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4318

# Optional: Enable HTTP request instrumentation (default: false)
export OTEL_INSTRUMENT_REQUESTS=true

# Run your application
uv run autoreporeview summary <path> <commit_a> <commit_b>
```

## Configuration

### Environment Variables

- `OTEL_SERVICE_NAME`: Service name for telemetry (default: `autoreporeview`)
- `OTEL_EXPORTER_OTLP_ENDPOINT`: OTLP exporter endpoint (default: `http://localhost:4318`)
- `OTEL_INSTRUMENT_REQUESTS`: Enable HTTP request instrumentation (default: `false`)

### OpenTelemetry Collector

The collector configuration is in `otel-collector-config.yaml`. It:
- Receives OTLP data on ports 4317 (gRPC) and 4318 (HTTP)
- Exports traces to Tempo
- Exports metrics to Prometheus
- Logs all telemetry data

### Grafana

Grafana is pre-configured with:
- Prometheus datasource for metrics
- Tempo datasource for traces
- AutoRepoReview dashboard for visualization

## Viewing Traces

1. Open Grafana at `http://localhost:3000`
2. Navigate to **Explore** in the left menu
3. Select **Tempo** as the datasource
4. Use the search to find traces by:
   - Service name
   - Operation name
   - Tags/attributes
   - Trace ID

## Viewing Metrics

1. Open Grafana at `http://localhost:3000`
2. Navigate to **Dashboards** → **AutoRepoReview Observability**
3. View metrics including:
   - Trace duration (95th and 50th percentile)
   - Trace count per operation
   - Error rates
   - Service overview statistics

## Stopping the Stack

To stop all services:

```bash
docker-compose down
```

To stop and remove all data volumes:

```bash
docker-compose down -v
```

## Troubleshooting

### No traces appearing in Grafana

1. Check that the OpenTelemetry Collector is running: `docker-compose ps`
2. Verify the application is sending data to the correct endpoint
3. Check collector logs: `docker-compose logs otel-collector`
4. Verify Tempo is receiving data: `docker-compose logs tempo`

### Port conflicts

If ports are already in use, modify the port mappings in `docker-compose.yml`.

### Application not sending telemetry

1. Verify environment variables are set correctly
2. Check that the telemetry module is imported in `app/__main__.py`
3. Review application logs for OpenTelemetry errors

