from fastapi import FastAPI
from pydantic import BaseModel, Field
from opal_tools_sdk import ToolsService, tool
from textblob import TextBlob

app = FastAPI()
tools_service = ToolsService(app)  # Auto-generates the /discovery endpoint for Opal

# Define the input schema
class ReviewParams(BaseModel):
    text: str = Field(..., description="The raw customer review text to analyze.")

@tool(
    name="analyze_review_sentiment",
    description="Analyzes review text to determine Sentiment and Business Category (Technical, Guidance, Positive, Negative)."
)
async def analyze_review_sentiment(params: ReviewParams):
    text_lower = params.text.lower()
    blob = TextBlob(params.text)
    polarity = blob.sentiment.polarity
    
    # --- LOGIC: Categorize the review ---
    category = "General"
    
    # 1. Technical Keywords (High Priority)
    tech_keywords = ["bug", "crash", "error", "slow", "fail", "broken", "login", "500", "api"]
    
    # 2. Guidance Keywords
    guidance_keywords = ["how to", "guide", "help", "where is", "manual", "instruction"]

    if any(word in text_lower for word in tech_keywords):
        category = "Technical Issue"
    elif any(word in text_lower for word in guidance_keywords):
        category = "Guidance"
    elif polarity >= 0:
        category = "Positive"
    else:
        category = "Negative"

    # --- OUTPUT: Structured JSON ---
    return {
        "review": params.text,
        "sentiment_score": round(polarity, 2),
        "category": category,
        "summary": f"Detected {category} with score {polarity:.2f}"
    }

# To run: uvicorn main:app --reload --port 8000