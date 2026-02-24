# CrewAI Hierarchical Process Demo (Dockerized)

This project demonstrates CrewAI's Hierarchical Process (Manager Agent Orchestration) running inside Docker with:

- Explicit LLM API endpoint and model configuration
- Full logging of model inputs and outputs
- Model call limiting (hard stop after N calls)
- Pause / resume execution via external file
- Clean containerized setup

The demo showcases how a Manager Agent dynamically delegates work to specialist agents using:

    process=Process.hierarchical

---

## Project Structure

crewai-hierarchical-demo/
│
├── Dockerfile
├── requirements.txt
├── main.py
└── README.md

---

## What This Demonstrates

### 1. Hierarchical Agent Orchestration
A Project Manager agent dynamically delegates work to:
- Senior Researcher
- Technical Writer

### 2. Explicit LLM Configuration
The LLM endpoint and model are configurable via environment variables.

### 3. Full Model Logging
Logs include:
- Model call number
- Full prompt input
- Model output
- Agent actions (via verbose mode)

### 4. Model Call Limiting
Execution automatically stops after a configurable number of model calls.

### 5. Pause / Resume Execution
If a file named `pause-agents.txt` exists, execution pauses until the file is removed.

---

## Build Instructions

### 1. Build Docker Image

    docker build -t crewai-hierarchical-demo .

### 2. Run the Demo

    docker run --rm \
      -e OPENAI_API_KEY=your_openai_key \
      crewai-hierarchical-demo

---

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|----------|-------------|
| OPENAI_API_KEY | Yes | None | API key for the LLM provider |
| LLM_MODEL_NAME | No | gpt-4o-mini | Model name to use |
| LLM_API_BASE | No | https://api.openai.com/v1 | Custom API endpoint |
| MAX_MODEL_CALLS | No | 10 | Maximum allowed LLM calls before stopping |

---

## Example with Full Configuration

    docker run --rm \
      -e OPENAI_API_KEY=your_key \
      -e LLM_MODEL_NAME=gpt-5.1-codex-mini \
      -e LLM_API_BASE=https://api.openai.com/v1 \
      -e MAX_MODEL_CALLS=15 \
      crewai-hierarchical-demo

---
## Current OpenAI models

1. gpt-5.3-codex            Latest frontier agentic coding model.        
2. gpt-5.2-codex            Frontier agentic coding model.
3. gpt-5.1-codex-max        Codex-optimized flagship for deep and
                              fast reasoning.                              
4. gpt-5.2                  Latest frontier model with improvements
                              across knowledge, reasoning and coding
5. gpt-5.1-codex-mini       Optimized for codex. Cheaper, faster, but
                              less capable.

## Pause / Resume Execution

The system checks for a file named:

    pause-agents.txt

### Pause execution:

    touch pause-agents.txt

Agents will log:

    Execution paused. Waiting for pause file to be removed...

### Resume execution:

    rm pause-agents.txt

Execution automatically continues.

---

## Logging Behavior

The system logs:
- Model call number
- Full prompt sent to model
- Model response
- Agent delegation steps
- Stop condition (if call limit exceeded)

Example:

    MODEL CALL #3
    Prompt:
    ...

    MODEL RESPONSE:
    ...

---

## Model Call Limiting

To prevent runaway agent loops, the demo stops execution after a configurable number of model calls.

If exceeded:

    Max model call limit reached. Stopping execution.

This is useful for:
- Cost control
- Debugging
- Safety constraints
- Production governance

---

## Architecture Overview

User Task
   ↓
Manager Agent
   ↓ (delegates dynamically)
Researcher Agent
   ↓
Writer Agent
   ↓
Final Structured Report

Process type used:

    Process.hierarchical

---

## Security Notes

- API keys are injected via environment variables.
- No secrets are stored in the Docker image.
- The container exits cleanly after execution.
- Model call limits prevent runaway costs.

---

## Why This Demo Matters

This project demonstrates how to move from:

Simple agent demo  
to  
Governed, observable, production-ready multi-agent orchestration

It combines:
- Hierarchical delegation
- Runtime control
- Cost governance
- External execution management
- Dockerized deployment

---

## License

Demo project for educational and experimental purposes.
