from fastapi import FastAPI

app = FastAPI(title="Ecommerce API", version="1.0.0")


@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "Healthy"}
