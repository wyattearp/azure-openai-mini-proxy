from fastapi import FastAPI, Request
from azure_openai_mini_proxy.azure_router import route_request
import os

app = FastAPI()

@app.post("/v1/{endpoint:path}")
async def proxy(request: Request, endpoint: str):
    return await route_request(request, endpoint)

def print_startup_notice():
    notice_paths = ["./NOTICE", "/app/NOTICE"]
    notice_content = None
    
    # Try to read the NOTICE file
    for path in notice_paths:
        if os.path.exists(path):
            with open(path, "r") as f:
                notice_content = f.read().strip()
            break

    print("""
╔════════════════════════════════════════════════════════════════╗
║             Azure OpenAI Mini Proxy Starting Up                ║
║----------------------------------------------------------------║
║ - Listening on: http://0.0.0.0:11434                           ║
║ - OpenAI-compatible endpoint: http://localhost:11434/v1        ║
║ - Config file locations:                                       ║
║   * ./config.yaml                                              ║
║   * /app/config.yaml (in container)                            ║
║   * ~/.config/azure-openai-mini-proxy/config.yaml              ║
╚════════════════════════════════════════════════════════════════╝
""")
    
    if notice_content:
        print("\nNOTICE:\n" + "="*7 + "\n" + notice_content + "\n")

def start():
    import uvicorn
    print_startup_notice()
    uvicorn.run("azure_openai_mini_proxy.cli:app", host="0.0.0.0", port=11434, reload=False)