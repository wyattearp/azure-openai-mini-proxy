# Azure OpenAI Mini Proxy

A minimal FastAPI-based reverse proxy that exposes a single OpenAI-compatible base URL and internally routes to various Azure OpenAI deployment endpoints.

## Features
- Unified `/v1` OpenAI-style API
- Per-route Azure config: deployment, API version, endpoint, and key
- Docker + pip package support
- Flexible config file locations

## Installation

### Using pip
```bash
pip install azure-openai-mini-proxy
```

### Using Docker
```bash
docker compose up --build
```

## Configuration

Create a `config.yaml` (see the `config.example.yaml`) file in one of these locations:
- Current directory (`./config.yaml`)
- Docker container path (`/app/config.yaml`)
- User config directory (`~/.config/azure-openai-mini-proxy/config.yaml`)

Example config:
```yaml
routes:
  chat/completions:
    endpoint: "https://your-resource.openai.azure.com"
    deployment: "gpt-4"
    api_version: "2023-05-15"
    api_key: "your-api-key"
```

## Usage

### Running directly
```bash
azure-openai-mini-proxy
```

### Using Docker
```bash
docker compose up --build
```

Then set your OpenAI-compatible tools to use:

```bash
export OPENAI_API_KEY=irrelevant
export OPENAI_BASE_URL=http://localhost:11434/v1
```