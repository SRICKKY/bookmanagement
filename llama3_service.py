import httpx

LLAMA3_API_URL = "http://localhost:11434/api/generate"

async def generate_summary(text: str, model_name: str = "llama3.1") -> str:
    payload = {
        "model": model_name,
        "prompt": text,
        "stream": False
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(LLAMA3_API_URL, json=payload)
            response.raise_for_status()  # Raises an HTTPError for bad responses
            result = response.json()
            # Ensure the "summary" field exists in the result
            return result.get("summary", "No summary available.")
        except httpx.HTTPStatusError as e:
            # Handle HTTP errors, such as connection problems or 4xx/5xx responses
            print(f"HTTP error occurred: {e}")
            return "Error HTTPStatusError."
        except httpx.RequestError as e:
            # Handle network-related errors
            print(f"Request error occurred: {e}")
            return "Error RequestError."
        except Exception as e:
            # Handle other possible exceptions
            print(f"An unexpected error occurred: {e}")
            return "Error Exception"

