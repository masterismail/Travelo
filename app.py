from fastapi import FastAPI, Request
import requests
import uvicorn

app = FastAPI()

GEMINI_API_KEY = 'AIzaSyAgIB8FDultd5rNBAcTLRxRQaXfWv8Tx1g'
GEMINI_API_URL = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent'

@app.post("/gemini-endpoint")
async def gemini_endpoint(request: Request):
    # Get the request data
    data = await request.json()
    
    # Define headers
    headers = {
        'Content-Type': 'application/json',
    }
    
    # Define request payload
    payload = {
        'contents': [{
            'parts': [{
                'text': data.get('text')
            }]
        }]
    }
    
    # Make the request to Gemini API
    response = requests.post(
        f'{GEMINI_API_URL}?key={GEMINI_API_KEY}',
        headers=headers,
        json=payload
    )
    
    # Return the API response as JSON
    return response.json()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
else:
    asgi = uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")