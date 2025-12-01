# AutoRepoReview

[![codecov](https://codecov.io/gh/AutoRepoReviewITPD/AutoRepoReview/branch/main/graph/badge.svg)](https://codecov.io/gh/AutoRepoReviewITPD/AutoRepoReview)

AI-powered git repository change analysis

## Quick Start

1. **Install [uv](https://docs.astral.sh/uv/getting-started/installation/)** (if you don't have it)

2. **Run AutoRepoReview** directly from GitHub:
   ```bash
   uvx --from git+https://github.com/AutoRepoReviewITPD/AutoRepoReview autoreporeview summary <commit_a> <commit_b>
   ```

That's it! Have fun.

### Local Development

For development, clone the repository and run:
```bash
uv run autoreporeview summary <commit_a> <commit_b>
```

## Project Goals
- Automate routine review of repository changes
- Learn about the health and development dynamics of a project
- Quickly discover hidden patterns and issues in code
- Explain complex changes in simple terms using AI

## Description

This project develops a code summarizer tool that analyzes GitHub commits to generate concise summaries of code changes. It highlights key modifications, such as added/removed features, bug fixes, and the overall impact on functionality, enabling users to quickly understand what the new code can do without reviewing the entire diff.

## Threshold of Success Diagram

The project is considered successful if it meets the following criteria:
- Accurately summarizes at least 80% of simple commits (e.g., single-file changes) based on manual evaluation.
- Processes commits from public GitHub repositories in under 1 minute per commit.
- Provides readable summaries that include change type, affected components, and functional implications.
- Handles common programming languages like Python, JavaScript, and Java.
- Has a user-friendly interface, similar to the command-line interface of Git.
- Easily installable on Linux.

## Project Context

```mermaid
flowchart TD
    %% Define nodes with clean labels and subtitles
    A[GitHub Repository<br/><small>Commits & Diffs</small>] 
    B[AutoRepoReview<br/><small>Code Changes Summarizer</small>]
    C[User Interface<br/><small>View Summaries</small>]
    D[Summary Output<br/><small>Text Description</small>]
    E[LLM Provider<br/><small>External API</small>]

    %% Define data flows with arrows
    A -->|Provides commit diff| B
    B -->|Sends code changes| E
    E -->|Returns AI analysis| B
    B -->|Generates summary| C
    B -->|Produces| D

    %% Style the nodes for better readability
    classDef system fill:#4a90e2,stroke:#333,stroke-width:2px,color:white
    classDef output fill:#f39c12,stroke:#333,stroke-width:2px,color:white
    classDef input fill:#27ae60,stroke:#333,stroke-width:2px,color:white
    classDef ui fill:#9b59b6,stroke:#333,stroke-width:2px,color:white
    classDef external fill:#e74c3c,stroke:#333,stroke-width:2px,color:white,dashed

    class A input
    class B system
    class C ui
    class D output
    class E external
```

## Features Roadmap

### In Progress
- [ ] Commit difference summarization
- [ ] CLI for summary viewing

### Planned
- [ ] PDF report generation for visualization
- [ ] Advanced pattern recognition (identify stable, volatile, and recurrently-changing code patterns)
- [ ] Contributors activity analysis

## Documentation

**[View Documentation Site](https://AutoRepoReviewITPD.github.io/AutoRepoReview/)** with sprint reports, meeting notes, and project documentation.
- `./docs/sprints` — Contains scripts, meeting notes, sprint reports, and other iterative documentation reflecting project progress.
- `./docs/ai-usage.md` — Details how AI tools have been used within the project.
