from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import (
    books_router,
    auth_router,
    # recommendation_router,
    # summary_router 
)

app = FastAPI(title="Book Management API service")

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:3000",
]

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def read_main():
    return {"message": "Hello World"}

app.include_router(auth_router, tags=["Authentication"])
app.include_router(books_router, prefix="/books", tags=["Endpoints"])
# app.include_router(recommendation_router)
# app.include_router(summary_router)


# if __name__ == '__main__':
#     import uvicorn
#     uvicorn.run(app)