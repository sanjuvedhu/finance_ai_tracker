import os
import pandas as pd
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def get_saving_tips(df: pd.DataFrame) -> str:
    summary = df.groupby("Category")["Amount"].sum().to_dict()
    
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        prompt = f"""
        A user's monthly spending breakdown is:
        {summary}
        
        Give 3 specific, practical money-saving tips based on their spending.
        Be friendly and concise. Use emojis.
        """
        response = model.generate_content(prompt)
        return response.text
    except Exception:
        return "💡 Track your spending regularly to find saving opportunities!"