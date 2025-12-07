# Observability

This document describes how we plan to monitor, diagnose, and respond to issues in **AutoRepoReview**, focusing on reliability, performance, and overall system health. Since our tool is a CLI that depends on Git and external LLM APIs, observability is essential to understand failures and keep the experience consistent for users.

## Technical Risks

Identifying the main reliability and performance risks helps us decide what to measure. The top risks for AutoRepoReview are:

1. LLM/API failures or timeouts — If the external LLM provider is slow or unavailable, summaries can't be generated.
2. Slow summary generation — Large diffs or slow LLM responses result in poor UX.
3. Git extraction errors — Corrupted local repos or Git errors can break the workflow.
4. Instrumentation/exporter failures — If telemetry isn't sent, we may not notice real problems.
5. High rate of failed or retried commands — Often indicates a deeper issue (API keys, network issues, malformed input).

From these, we select the two most critical risks to monitor through SLOs.

## Service Level Objectives (SLOs) (Planned)

The following SLOs are planned for future implementation once the necessary metrics collection is in place:

SLO 1 — LLM API Reliability

To ensure the core summarization feature works consistently, we will track the success rate of all LLM API calls. The LLM API success rate must stay above 99% over a 30-minute rolling window. This metric directly reflects whether the tool can actually produce summaries.

SLO 2 — Summary Latency

We want the user to receive results quickly; long delays make the CLI feel broken. End-to-end summary generation (from command start to printed output) must stay below 2 seconds for 95% of runs. This includes Git diff generation + LLM request + local processing.

## Instrumentation Plan

### Currently Collected Metrics

At present, the system collects only the following metrics:

- LLM input length — Length of the request sent to the LLM
- LLM output length — Length of the response received from the LLM

These metrics are collected to monitor token usage and understand basic interaction patterns.

### Planned Future Metrics

The following metrics are planned for future implementation to support SLO monitoring:

LLM API Success Rate

We count every request and categorize the result:

```
success_count / total_requests
```

Tracked via OpenTelemetry counters (success, timeout, error).

Summary Latency

We measure timestamps at the start and end of each summary:

```
summary_duration_seconds = end - start
```

Recorded as a histogram for percentiles.

### Additional Context Needed When SLOs Fail

When LLM reliability drops:

* type of error (timeout, HTTP code, invalid response)
* how long the LLM took to respond
* which prompt type was used
* trace ID for the specific request

When latency increases:

* Git diff duration
* LLM request duration
* number of changed files
* size of the repository
* version of CLI

This extra context speeds up debugging and helps identify if the problem is external (LLM provider), internal (Git), or user-specific.

### Telemetry Collection Pipeline (Planned)

The following telemetry collection pipeline is planned for future implementation:

AutoRepoReview will use OpenTelemetry to collect metrics, logs, and traces. Data will flow through a simple pipeline:

1. **CLI** emits metrics/traces/logs during execution.
2. **OpenTelemetry SDK** collects the data.
3. Data is exported using **OTLP**.
4. Backend tools such as **Grafana Cloud** store and visualize telemetry.

## Alerting Strategy (Planned)

The following alerting strategy is planned for future implementation once SLOs are in place:

We define alerts based on the two SLOs.

Alert 1: Low LLM Success Rate

* Trigger: success rate < 99% for 15 minutes
* Severity: High
* Delivery: Dashboard notification

Alert 2: High Summary Latency

* Trigger: p95 latency > 2 seconds for 10 minutes
* Severity: Medium
* Delivery: Dashboard notification

Alerts notify maintainers early, before users start experiencing consistent failures.

## Response Plan (Planned)

The following response plan is planned for future implementation:

Example Scenario: LLM Success Rate Drops

When alerts are triggered, maintainers are notified via dashboard. First response steps:

1. Check the dashboard to confirm the spike and look at error types.
2. Inspect recent traces to see where failures occur (network, provider, internal issue).
3. Review logs for repeated patterns such as:

   * timeouts
   * invalid API responses
   * authentication errors
4. Check the LLM provider status page to confirm if the outage is external.
5. If external:

   * Show a clear error message to users
   * Consider enabling fallback model (if configured)
6. If internal:

   * Roll back recent changes
   * Mitigate excessive token size or large diff extraction
   * Patch the issue

This keeps the tool stable and reduces user frustration during outages.
