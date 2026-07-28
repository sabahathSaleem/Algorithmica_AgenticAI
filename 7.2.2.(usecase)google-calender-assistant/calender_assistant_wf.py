import asyncio
from typing import Union
from pydantic_ai import Agent
from models import DeleteInvite, MeetingInvite, UpdateInvite, RetrievalRequest, MissingInfo
from calender_service import CalenderService
from dotenv import load_dotenv
import logfire

load_dotenv(override=True)
logfire.configure()
logfire.instrument_pydantic_ai()

agent = Agent(
    #"ollama:qwen3.5:9b",
    'groq:llama-3.3-70b-versatile',
    output_type=Union[MeetingInvite, UpdateInvite, RetrievalRequest, DeleteInvite, MissingInfo],
    system_prompt=(
        "You are a calendar assistant. Route the user's request to the correct model: "
        "1. NEW MEETING: Need title, attendees (emails), and start_time. "
        "2. UPDATE MEETING: Need event_id and new_attendees. "
        "3. RETRIEVAL: Need year (and optional month). "
        "If any required data is missing for the chosen intent, return MissingInfo."
    )
)

async def workflow():
    calender_service = CalenderService()

    message_history = []
    print("Calendar Agent is ready! (Type 'exit' to quit)")

    while True:
        user_input = input("\nUser: ")
        if user_input.lower() in ['exit', 'quit']: break

        result = await agent.run(user_input, message_history=message_history)
        
        # Handle the result based on type
        if isinstance(result.output, MissingInfo):
            print(f"AI: {result.output.question}")
            message_history = result.all_messages() 
        
        elif isinstance(result.output, MeetingInvite):
            result = calender_service.create_google_invite(result.output)
            print(result)
            message_history = [] # Reset after success

        elif isinstance(result.output, UpdateInvite):
            result = calender_service.update_google_invite(result.output)
            print(result)
            message_history = []

        elif isinstance(result.output, RetrievalRequest):
            result = calender_service.list_google_calender_events_by_date(result.output)
            print(result)
            message_history = []
        elif isinstance(result.output, DeleteInvite):
            print(result.output)
            result = calender_service.delete_google_invite(result.output)
            print(result)
            message_history = []

if __name__ == "__main__":
    asyncio.run(workflow())

# create a new meeting invite on 6th april 2026 at 10am IST with title "ProjectTest" and attendees algorithmica.desktop@gmail.com