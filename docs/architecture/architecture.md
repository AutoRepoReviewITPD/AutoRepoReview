# Context Diagram

```mermaid

graph TD
    User -->|Give 2 commits and get the summary| CLI
    CLI -->|Ask for summary based on 2 given commits| API
    API -->|Ask for summary based on 2 given commits| Model

    Model -->|Give the result| API
    API -->|Postprocess the result and return it as a response to client| CLI
    CLI -->|Print the result| User
```

## External Actors

| Actor | Description |
|---|---|
|User|An individual that uses this project|
|CLI|A program that is used by user in terminal to interact with the system|
|API|A program that is used by CLI to use core of the system|
|LLM model|An LLM model that gives the summary of changes between 2 commits|

