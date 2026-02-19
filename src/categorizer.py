import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

_cache = {}

def categorize_expense(description: str) -> str:
    if description in _cache:
        return _cache[description]
    
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        prompt = f"""
        Categorize this bank transaction into ONE category only:
        [Food, Transport, Entertainment, Bills, Shopping, Health, Other]
        
        Transaction: {description}
        Reply with ONLY the category name, nothing else.
        """
        response = model.generate_content(prompt)
        category = response.text.strip()
        _cache[description] = category
        return category
    except Exception:
        return "Other"