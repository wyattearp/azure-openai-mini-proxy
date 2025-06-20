import httpx
import yaml
import logging
import time
import os
from fastapi import Request
from starlette.responses import JSONResponse

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(name)s - %(filename)s:%(lineno)d - %(message)s")

def load_config():
    config_paths = [
        "config.yaml",  # Current directory
        "/app/config.yaml",  # Docker container path
        os.path.expanduser("~/.config/azure-openai-mini-proxy/config.yaml"),  # User config
    ]
    
    for path in config_paths:
        if os.path.exists(path):
            with open(path) as f:
                logging.debug(f"Loading config from {path}")
                return yaml.safe_load(f)["routes"]
    logging.error("No config.yaml found in any of the expected locations")
    raise FileNotFoundError("No config.yaml found in any of the expected locations")

ROUTES = load_config()

async def route_request(request: Request, endpoint: str):
    route_config = ROUTES.get(endpoint)
    if not route_config:
        logging.error(f"No route found for /v1/{endpoint}")
        return JSONResponse({"error": f"No route for /v1/{endpoint}"}, status_code=404)

    azure_url = (
        f"{route_config['endpoint']}/openai/deployments/"
        f"{route_config['deployment']}/{endpoint}"
        f"?api-version={route_config['api_version']}"
    )

    body = await request.body()
    headers = {
        "api-key": route_config["api_key"],
        "Content-Type": "application/json"
    }

    start = time.time()
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            azure_resp = await client.post(azure_url, content=body, headers=headers)
        elapsed = time.time() - start

        logging.info(f"Proxied /v1/{endpoint} -> {azure_url} [{azure_resp.status_code}] in {elapsed:.2f}s")

        return JSONResponse(content=azure_resp.json(), status_code=azure_resp.status_code)
    except Exception as e:
        logging.exception(f"Proxy error for /v1/{endpoint}")
        return JSONResponse({"error": "Internal proxy error"}, status_code=500)