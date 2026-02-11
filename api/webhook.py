import uvicorn
from fastapi import FastAPI
from api.routes import router  # ajuste o caminho conforme seu projeto

webhook = FastAPI()

webhook.include_router(router)

if __name__ == "__main__":
    uvicorn.run(webhook, host="localhost", port=8000)
