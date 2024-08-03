import requests

LLAMA3_API_URL = "http://localhost:11434/api/generate"

def generate_summary(text: str, model_name: str = "llama3.1") -> str:
    payload = {
        "model": model_name,
        "prompt": text,
        "stream": False
    }
    
    try:
        response = requests.post(LLAMA3_API_URL, json=payload)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        result = response.json()
        return result.get("response", "No summary available.")
    except requests.HTTPError as e:
        # Handle HTTP errors, such as connection problems or 4xx/5xx responses
        print(f"HTTP error occurred: {e}")
        return "Error HTTPError."
    except requests.RequestException as e:
        # Handle network-related errors
        print(f"Request error occurred: {e}")
        return "Error RequestException."
    except Exception as e:
        # Handle other possible exceptions
        print(f"An unexpected error occurred: {e}")
        return "Error Exception."
