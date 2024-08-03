import httpx
from fastapi import APIRouter

summary_router = router = APIRouter()


LLAMA3_API_URL = "http://localhost:11434/api/generate"

async def generate_summary(text: str) -> str:
    payload = {
        "model": "llama3.1",
        "prompt": text,
        "stream": False
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(LLAMA3_API_URL, json=payload)
            response.raise_for_status()
            result = response.json()
            return result.get("result", "No summary available.")
        except httpx.HTTPStatusError as e:
            print(f"HTTP error occurred: {e}")
            return "Error HTTPStatusError."
        except httpx.RequestError as e:
            print(f"Request error occurred: {e}")
            return "Error RequestError."
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return "Error Exception"

