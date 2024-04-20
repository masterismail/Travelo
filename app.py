from fastapi import FastAPI, Request
import requests
import uvicorn

app = FastAPI()

# Replace with your actual API key (don't commit this line)
GEMINI_API_KEY = 'AIzaSyAgIB8FDultd5rNBAcTLRxRQaXfWv8Tx1g'
GEMINI_API_URL = 'https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent'

@app.post("/gemini-travel-recommendations")
async def gemini_travel_recommendations(request: Request):
    """
    Processes user data and retrieves travel recommendations from Gemini.

    Returns a JSON response containing the recommended places to travel
    based on budget and age, or an error message if the request fails.
    """

    # Get request data
    data = await request.json()

    # Extract data (ensure required fields are present)
    text = data.get("text", "")
    budget = data.get("budget")
    age = data.get("age")

    if not all([text, budget, age]):
        return {"error": "Missing required fields: text, budget, or age"}

    # Define headers
    headers = {'Content-Type': 'application/json'}

    # Craft user-friendly prompt, emphasizing place recommendations
    text1 = f"Can you suggest some great places in India for {text} to travel to, considering their budget of {budget} and age of {age}? Focus on providing specific place names."

    # Define payload
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": text1}
                ]
            }
        ]
    }

    # Make request to Gemini API
    try:
        response = requests.post(
            f'{GEMINI_API_URL}?key={GEMINI_API_KEY}', headers=headers, json=payload
        )
        response.raise_for_status()  # Raise exception for non-2xx status codes
    except requests.exceptions.RequestException as e:
        return {"error": f"Error making request to Gemini API: {str(e)}"}

    # Extract recommended places from response (handle potential errors)
    try:
        # Assuming the response structure follows Gemini's documentation
        generated_text = response.json()["contents"][0]["generatedText"]
        places = [place.strip() for place in generated_text.split(",") if place.strip()]
    except (KeyError, ValueError) as e:
        return {"error": f"Error parsing response: {str(e)}"}

    # Return success response with recommended places
    return {"places": places}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
