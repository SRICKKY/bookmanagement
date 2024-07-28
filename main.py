from fastapi import FastAPI
from routers import books_router, recommendation_router, summary_router

app = FastAPI(title="Book Management API service")


@app.get("/")
async def read_main():
    return {"msg": "Hello World"}


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app)