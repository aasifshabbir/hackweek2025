from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import os
import requests
from dotenv import load_dotenv
import os
from openai import OpenAI
# client = OpenAI()
app = FastAPI()



# Allow all origins for development; restrict in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class JobInput(BaseModel):
    description: str = None
    url: str = None

@app.post("/extract-skills")
def extract_skills(input: JobInput):
    # load_dotenv()
    # openai_api_key = os.getenv("OPENAI_API_KEY")
    # response = client.responses.create(
    # model="gpt-4.1",
    # input="Write a one-sentence bedtime story about a unicorn.")
    # print(response.output_text)
    """
    Extracts the top 10 technical and soft skills from a job description or URL using GPT-4.1.
    """
    # If a URL is provided, fetch the job description from the URL (basic implementation)
    job_text = input.description or ""
    if input.url:
        try:
            resp = requests.get(input.url, timeout=5)
            if resp.ok:
                job_text = resp.text
        except Exception as e:
            return {"error": f"Failed to fetch job description from URL: {str(e)}"}
    if not job_text:
        return {"error": "No job description provided."}

    # Prepare prompt for GPT-4.1
    prompt = (
        "Extract the top 10 technical and soft skills required for the following job description. "
        "Return the result as a JSON array of skill names only.\n\nJob Description:\n" + job_text
    )

    # Call OpenAI GPT-4.1 API
    load_dotenv()
    openai_api_key = os.getenv("OPENAI_API_KEY")
    #print('openai_api_key----->',openai_api_key)
    if not openai_api_key:
        return {"error": "OpenAI API key not set in environment variable OPENAI_API_KEY."}
    headers = {
        "Authorization": f"Bearer {openai_api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-4-1106-preview",
        "messages": [
            {"role": "system", "content": "You are an expert at extracting skills from job descriptions."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 256,
        "temperature": 0.2
    }
    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=20
        )
        response.raise_for_status()
        result = response.json()
        # Try to parse the skills from the response
        content = result["choices"][0]["message"]["content"]
        import json as pyjson
        skills = pyjson.loads(content)
        if isinstance(skills, list):
            return {"skills": skills}
        else:
            return {"error": "Unexpected response format from GPT-4.1."}
    except Exception as e:
        return {"error": f"Failed to extract skills: {str(e)}"}

@app.get("/")
def root():
    return {"message": "Job Skills Extractor API is running."}