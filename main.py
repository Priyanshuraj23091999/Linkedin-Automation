import os
import asyncio
import requests
import nest_asyncio
from crewai import Crew, Process

# 1. Initialize event loop modifications for nested environments
nest_asyncio.apply()

# 2. Extract API credentials from system environment variables
# (GitHub Actions will inject these automatically from your secrets)
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
os.environ["SERPER_API_KEY"] = os.getenv("SERPER_API_KEY")

# --- AGENT DEFINITIONS ---
# Ensure your 'researcher' and 'writer' agent definitions from earlier cells are here
# Example layout (make sure these match your exact working agent configurations):
# researcher = Agent(...)
# writer = Agent(...)

# --- TASK DEFINITIONS ---
# Ensure your 'researcher_task' and 'write_task' definitions from earlier cells are here
# research_task = Task(...)
# write_task = Task(...)


# 3. Dynamic Trend Finder Function
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
            print("⚠️ Live discovery failed, falling back to generalized tracking.")
            return "Enterprise GenAI and IT integration trends in corporate India"
    except Exception as e:
        print(f"⚠️ Search discovery error: {e}. Using fallback.")
        return "Digital transformation and supply chain adaptations in India"


# 4. Webhook Pipeline Outbox Function
def send_to_linkedin_pipeline(post_content, search_topic):
    # CRITICAL: Ensure your exact Make.com Webhook URL string is pasted here
    webhook_url = "YOUR_MAKE_WEBHOOK_URL_HERE"
    
    data = {
        "post_text": str(post_content),
        "image_keyword": str(search_topic),
        "status": "approved"
    }
    
    print("\n📡 Transmitting post data directly to Make.com pipeline...")
    try:
        response = requests.post(webhook_url, json=data)
        if response.status_code == 200:
            print("🚀 Success! Data successfully accepted by Make.com endpoint.")
        else:
            print(f"❌ Webhook communication failed. Status Code: {response.status_code}")
    except Exception as network_error:
        print(f"❌ Connection error: {network_error}")


# 5. Core Asynchronous Orchestration Loop
async def run_pipeline():
    # Assemble the operational Crew structure
    linkedin_automation_crew = Crew(
        agents=[researcher, writer],
        tasks=[research_task, write_task],
        process=Process.sequential,
        verbose=True
    )

    try:
        # A. Discover live trend
        my_topic = discover_live_trend()
        print(f"🎯 Selected Topic: '{my_topic}'")
        
        # B. Execute Agent workflow asynchronously
        result = await linkedin_automation_crew.kickoff_async(inputs={'topic': my_topic})
        
        final_post_text = str(result.raw) if hasattr(result, 'raw') else str(result)
        
        print("\n\n####################################")
        print("## GENERATED LINKEDIN POST BY AI ##")
        print("####################################\n")
        print(final_post_text)
        
        # C. Route to Make.com Webhook pipeline
        send_to_linkedin_pipeline(final_post_text, my_topic)

    except Exception as execution_failure:
        print(f"\n❌ Execution pipeline halted. Error trace: {execution_failure}")


# 6. Standard Python Entry Point
if __name__ == "__main__":
    # Standard Python scripts outside of Colab use an event loop runner
    asyncio.run(run_pipeline())