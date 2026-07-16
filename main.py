import os
import asyncio
import requests
import nest_asyncio
from crewai import Crew, Process

nest_asyncio.apply()

os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
os.environ["SERPER_API_KEY"] = os.getenv("SERPER_API_KEY")

# --- PASTE YOUR WORKING AGENT AND TASK CONFIGURATIONS RIGHT HERE ---
# researcher = Agent(...)
# writer = Agent(...)
# research_task = Task(...)
# write_task = Task(...)

def discover_live_trend():
    print("🔍 Scanning live Google News index for top business trends...")
    url = "https://google.serper.dev/search"
    payload = {
        "q": "trending corporate business economy technology news india july 2026",
        "gl": "in",
        "hl": "en"
    }
    headers = {
        'X-API-KEY': os.environ["SERPER_API_KEY"],
        'Content-Type': 'application/json'
    }
    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            search_data = response.json()
            first_result_title = search_data['organic'][0]['title']
            first_result_snippet = search_data['organic'][0]['snippet']
            return f"{first_result_title} (Context: {first_result_snippet})"
        else:
            return "Enterprise GenAI and IT integration trends in corporate India"
    except Exception as e:
        return "Digital transformation and supply chain adaptations in India"

def send_to_linkedin_pipeline(post_content, search_topic):
    webhook_url = "https://hook.eu1.make.com/u024yiy13fuqkkynfi9mo4r3slzwxh9m"
    data = {
        "post_text": str(post_content),
        "image_keyword": str(search_topic),
        "status": "approved"
    }
    try:
        response = requests.post(webhook_url, json=data)
        if response.status_code == 200:
            print("🚀 Success! Data accepted by Make.com endpoint.")
    except Exception as network_error:
        print(f"❌ Connection error: {network_error}")

async def run_pipeline():
    linkedin_automation_crew = Crew(
        agents=[researcher], # Make sure both agents match your list
        tasks=[research_task], # Make sure both tasks match your list
        process=Process.sequential,
        verbose=True
    )
    try:
        my_topic = discover_live_trend()
        result = await linkedin_automation_crew.kickoff_async(inputs={'topic': my_topic})
        final_post_text = str(result.raw) if hasattr(result, 'raw') else str(result)
        send_to_linkedin_pipeline(final_post_text, my_topic)
    except Exception as execution_failure:
        print(f"❌ Error: {execution_failure}")

if __name__ == '__main__':
    asyncio.run(run_pipeline())
