FROM python:3.12-slim

ARG CUSTOM_CERT_DIR="certs"

# Update certificates if custom ones were provided and copied successfully
RUN if [ -n "${CUSTOM_CERT_DIR}" ]; then \
        mkdir -p /usr/local/share/ca-certificates && \
        if [ -d "${CUSTOM_CERT_DIR}" ]; then \
            cp -r ${CUSTOM_CERT_DIR}/* /usr/local/share/ca-certificates/ 2>/dev/null || true; \
            update-ca-certificates; \
            echo "Custom certificates installed successfully."; \
        else \
            echo "Warning: ${CUSTOM_CERT_DIR} not found. Skipping certificate installation."; \
        fi \
    fi
WORKDIR /app

COPY NOTICE .
COPY pyproject.toml .
COPY azure_openai_mini_proxy azure_openai_mini_proxy

RUN pip install --no-cache-dir .

EXPOSE 11434

CMD ["azure-openai-mini-proxy"]