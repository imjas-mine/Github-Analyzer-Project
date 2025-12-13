from openai import AsyncOpenAI
from app.core.config import settings
import json
class OpenAIService:
    def __init__(self):
        self.client=AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.model="gpt-4o-mini"

    async def send_prompt(self, system_prompt: str, user_prompt: str):
        response=await self.client.chat.completions.create(
            model=self.model,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )
        return json.loads(response.choices[0].message.content)


    async def analyze_repository(self, repoContext: dict)->dict:
        system_prompt = "You analyze GitHub repos and return JSON with: project_type, frameworks (list), generated_description, key_features (list), tech_stack_summary, complexity_score (1-10)."
        
        user_prompt = f"Analyze this repo: {repoContext}"
        
        return await self.send_prompt(system_prompt, user_prompt)

    async def summarize_contribution(self, contributionContext: dict)->dict:
        system_prompt = "You analyze a developer's GitHub contributions and return JSON with: relationship (Owner/Core Contributor/Contributor), contribution_percentage, primary_areas (list), summary_text, notable_contributions (list)."
        
        user_prompt = f"Summarize this developer's contributions: {contributionContext}"
        
        return await self.send_prompt(system_prompt, user_prompt)

    