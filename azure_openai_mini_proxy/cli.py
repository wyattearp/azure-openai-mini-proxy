from fastapi import FastAPI, Request
from azure_openai_mini_proxy.azure_router import route_request

app = FastAPI()

@app.post("/v1/{endpoint:path}")
async def proxy(request: Request, endpoint: str):
    return await route_request(request, endpoint)

def start():
    import uvicorn
    uvicorn.run("azure_openai_mini_proxy.cli:app", host="0.0.0.0", port=11434, reload=False)