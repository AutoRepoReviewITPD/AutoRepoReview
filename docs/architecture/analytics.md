## Value Moment

The value moment is the point where the user receives meaningful value from the product.

**Value Moment:** A developer gets an accurate, intent-aligned summary of changes between two versions of a repository.

This is the moment when the user understands *what changed* without reading raw diffs.

## 3–5 Possible Metrics Measuring This Value Moment

These metrics reflect how often and how well users reach the value moment:

1. Successful diff summaries generated
2. End-to-end summary response time
3. Error rate of summary attempts

## North Star Metric (NSM)

NSM: Number of successful diff summaries per active user session

### Why this NSM satisfies the criteria:

* **Measures customer value:**
  The value comes from receiving a correct, helpful summary. Counting these directly measures delivered value.

* **Represents core product strategy:**
  AutoRepoReview exists to help developers understand diffs faster. This is exactly what this metric tracks.

* **Leading indicator:**
  More high-quality summaries ⇒ more adoption, retention, and trust
  Fewer summaries ⇒ users are stuck/confused ⇒ likely to lose retention

* **Actionable now:**
  We can immediately influence it through:

  * improving prompt types
  * reducing errors
  * optimizing latency
  * improving Git extraction stability

## Counter Metric

**Counter Metric:** Count of summaries that result in an error or re-run within 30 seconds

### Why this protects against over-optimization:

* If we optimize only for “number of summaries”, the system may push summaries out quickly but with low quality.
* This counter metric captures:
  * Git/LLM/validation failures
  * user dissatisfaction (immediate re-run)
* This minimizes the unintended side effects (outputting poor summaries) of focusing on success metrics

## What Data We Collect

### Currently Collected Metrics

At present, the system collects only the following metrics for each LLM interaction:

- **LLM input length** — Length of the request sent to the LLM
- **LLM output length** — Length of the response received from the LLM

These metrics are collected to monitor token usage and understand basic interaction patterns.

### Planned Future Metrics

To calculate the metrics described above and understand customer intent, the system will collect the following analytics data for each relevant CLI invocation (planned for future implementation):  

- Command-level data:  
  - Command name and subcommand 
  - High-level outcome: success, error, cancelled

- Error data:  
  - Error category (Git, configuration/LLM key, network, LLM failure, unknown)  
  - Non-sensitive error code/label (no repository contents or LLM prompts)  

- Performance data:  
  - Duration from CLI command start until LLM response received  
  - Duration from CLI command start until output written to the terminal  

- Session-level data (non-identifying):  
  - Anonymous session id  
  - Tool version  

Sensitive repository content (diff body, code, commit messages, raw prompts) will not be stored in analytics. Only high-level metadata will be recorded.

## Measurement Approach and Pipeline (Planned)

To support analytics, the system will be instrumented using OpenTelemetry for metrics and events (planned for future implementation).

- Instrumentation points:  
  - At CLI command parsing: record command name and session id
  - At summary flow start/end: record start timestamp, end timestamp, outcome (success/error/re-run)
  - At error handling: record error type and code

## Planned Analytics Experiments

Because the customer value moment is that “the AI understands what the user wants to see in the summary”, the product will support multiple prompt options and experiment on their effectiveness.  

Planned experiments:  
- Add explicit prompt options in the CLI (e.g., `--doc`, `--features`, `--tests`, `--mixed`) and track usage and follow-up re-runs.  
- Compare re-run rates and error rates across prompt types as a proxy for how well the AI matched the user’s intent.  
- Track response time per prompt type to ensure new prompt templates do not significantly increase latency.  

