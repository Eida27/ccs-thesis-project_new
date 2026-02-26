import os
import json
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables (e.g., OPENAI_API_KEY)
load_dotenv()

# Initialize the OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def analyze_ticket_nlp(description: str) -> dict:
    """
    Performs Zero-Shot Classification and Sentiment Analysis on the ticket description.
    Returns a dictionary with category, sentiment_label, and priority_score.
    """
    
    system_prompt = """
    You are an IT Support Triage AI for a university College of Computer Studies.
    Analyze the following IT incident description.
    
    Task 1 (Zero-Shot Classification): Categorize the issue as strictly either 'Hardware', 'Network', or 'Software'.
    Task 2 (Sentiment Analysis): Assess the urgency and emotional state of the user. Label as 'Calm', 'Frustrated', or 'Panicking'.
    Task 3 (Priority Scoring): Assign a priority score from 1 (Lowest) to 10 (Highest) based on the severity of the issue and the user's sentiment.
    
    You MUST output ONLY a raw JSON object with the exact keys: 'category', 'sentiment', and 'priority_score'. Do not include markdown formatting.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini", # Cost-effective and fast for simple classification
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": description}
            ],
            temperature=0.2 # Low temperature for highly deterministic outputs
        )
        
        # Parse the JSON response from the LLM
        result = json.loads(response.choices[0].message.content)
        return result
        
    except Exception as e:
        # Fallback mechanism in case the API fails
        print(f"AI Triage Failed: {e}")
        return {"category": "Unknown", "sentiment": "Unknown", "priority_score": 5}