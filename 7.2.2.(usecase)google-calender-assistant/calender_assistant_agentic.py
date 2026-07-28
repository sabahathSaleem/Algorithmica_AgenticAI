import asyncio

from pydantic_ai import Agent, ModelMessage
from dataclasses import dataclass
from pydantic_ai import RunContext
from calender_service import CalenderService
from models import DeleteInvite, MeetingInvite, UpdateInvite, RetrievalRequest
from dotenv import load_dotenv
import logfire

load_dotenv(override=True)
logfire.configure()
logfire.instrument_pydantic_ai()

@dataclass
class Deps:
    calender_service: CalenderService

calender_agent = Agent(
    #'groq:llama-3.3-70b-versatile',
    'github:openai/gpt-4o',
    #"ollama:llama3-groq-tool-use:8b",
    #"ollama:qwen3.5:9b",
    deps_type=Deps,
    instructions=(
        "You are a master calendar assistant. You can create meetings, add new groups of people "
        "to existing ones, and pull full historical schedules or filtered lists by year/month."
        "Dont hallucinate and make up data. If you dont have enough information to complete the task, ask for it clearly and concisely. "
    )
)

@calender_agent.tool
def create_invite(ctx: RunContext[Deps], invite: MeetingInvite) -> str:
    """Creates a brand new event on the user's primary Google Calendar."""   
    return ctx.deps.calender_service.create_google_invite(invite)

@calender_agent.tool
def update_invite(ctx: RunContext[Deps], update: UpdateInvite) -> str:
    """Adds new attendees to an existing meeting without removing current ones."""
    return ctx.deps.calender_service.update_google_invite(update)

@calender_agent.tool
def list_events_by_date(ctx: RunContext[Deps], request: RetrievalRequest) -> str:
    """Retrieves all events for a specific year or month using pagination."""
    return ctx.deps.calender_service.list_google_calender_events_by_date(request)

@calender_agent.tool
def delete_invite(ctx: RunContext[Deps], event_id: DeleteInvite) -> str:
    """Deletes an existing meeting from the calendar."""
    return ctx.deps.calender_service.delete_google_invite(event_id)

async def main():
    deps = Deps(calender_service=CalenderService())
    message_history = []
    
    print("Calendar Agent is ready! (Type 'exit' to quit)")
    
    while True:
        user_input = input("\nUser: ")
        if user_input.lower() in ("exit", "quit"):
            break

        result = await calender_agent.run(
            user_input, 
            deps=deps,
            message_history=message_history
        )
        message_history = result.all_messages()        
        print(f"Agent: {result.output}")

if __name__ == "__main__":
    asyncio.run(main())

# create a new meeting invite on 5th april 2026 at 10am IST with title "ProjectTest" and attendees algorithmica.desktop@gmail.com