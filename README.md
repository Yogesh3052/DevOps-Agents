# Kubernetes and Docker Agent

## Overview

`Kubernetes and Docker Agent` is a Python-based intelligent assistant that uses an Ollama-backed LLM to invoke live tools for inspecting Kubernetes, Docker, Git, and system state.

This project is focused on Kubernetes and Docker diagnostics. It exposes a set of tool functions that execute shell commands like `kubectl`, `docker`, `docker compose`, `git`, and `curl`, then makes those tools available to a LangChain agent for interactive analysis.

## Architecture

The repository is intentionally small and follows a simple, tool-driven agent design:

1. **Language Model Layer**
   - `ChatOllama` from `langchain_ollama` provides the LLM interface.
   - The agent uses this model to interpret natural language queries and choose the appropriate tool.

2. **Tool Layer**
   - Each tool is a Python function decorated with `@tool` from `langchain_core.tools`.
   - Tools use `subprocess.run(...)` to execute shell commands and return the command output.
   - Tools are grouped around Kubernetes and Docker diagnostics:
     - Kubernetes inspection: pods, nodes, services, deployments, events, pod logs
     - Docker inspection: containers, images, logs, stats, compose status, all containers
     - System and networking checks: Docker/Kubernetes health, HTTP endpoint checks, Git status

3. **Agent Layer**
   - `create_agent(...)` from `langchain.agents` creates an agent instance.
   - The agent is configured with the LLM, available tools, and a system prompt defining behavior and execution rules.
   - The system prompt directs the agent to call tools for any live state question, avoid fabrication, and stay concise.

4. **User Interaction**
   - The script prompts the user for a question and routes the input through the agent.
   - The final answer is printed based on the agent's reasoning and tool outputs.

## File Structure

- `agent.py` - Main application script. Defines tools, configures the LLM and agent, and handles user input.
- `requirements.txt` - Python dependencies needed to run the agent.

## Dependencies

Install dependencies from `requirements.txt`:

```bash
pip install -r requirements.txt
```

The project depends on:

- `langchain-ollama`
- `langchain-core`
- `langchain`

## Prerequisites

The following CLI tools must be installed and available in the execution environment:

- `kubectl`
- `docker`
- `docker compose`
- `git`
- `curl`

Additionally, the user should have access to the relevant Kubernetes cluster and Docker environment for the diagnostics to work properly.

## Usage

Run the agent script and ask a question about your environment:

```bash
python agent.py
```

Example queries:

- `List all Kubernetes pods across namespaces.`
- `Show Docker containers currently running.`
- `Get logs for a container named my_app.`
- `Check the health of the Docker and Kubernetes environment.`
- `What is the current git status?`

## Agent Behavior

The agent is designed to:

- Always use the appropriate tool when a live environment query is required.
- Never fabricate resource names, statuses, or output.
- Answer concisely and professionally.
- Explain likely causes when a tool fails.

## Notes and Safety

- The agent runs shell commands directly, so it should be used in trusted environments only.
- `subprocess` calls may expose sensitive information if the environment contains credentials or restricted data.
- If a command times out or fails, the returned output will include the command stderr.

## Extending the Agent

To add new capabilities:

1. Define a new `@tool` function in `agent.py`.
2. Add the function to the `tools=[...]` list in `create_agent(...)`.
3. Update the system prompt to describe the new tool and its expected usage.

## Contributing and Issues

If you have suggestions, improvements, or bug reports, please create an issue in the repository. Include:

- a short description of the problem or requested feature
- steps to reproduce or expected behavior
- relevant environment details (Kubernetes/Docker versions, OS, CLI command outputs)

## License

This repository does not include a license file. Add one if you want to define reuse permissions.
