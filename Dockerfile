FROM python:3.12-slim

WORKDIR /app

COPY NOTICE .
COPY pyproject.toml .
COPY azure_openai_mini_proxy azure_openai_mini_proxy

RUN pip install --no-cache-dir .

EXPOSE 11434

CMD ["azure-openai-mini-proxy"]