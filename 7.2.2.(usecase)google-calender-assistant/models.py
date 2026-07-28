from pydantic import BaseModel, Field
from typing import Optional, List
import datetime

class MissingInfo(BaseModel):
    question: str = Field(description="Ask for missing fields like title, date, or emails")

class MeetingInvite(BaseModel):
    title: str = Field(description="The subject of the meeting")
    attendees: List[str] = Field(description="List of email addresses for participants")
    start_time: datetime.datetime = Field(description="The starting date and time")
    duration_minutes: int = Field(default=30, description="Meeting duration in minutes")

class UpdateInvite(BaseModel):
    event_id: str = Field(description="The unique ID of the existing Google Calendar event")
    new_attendees: List[str] = Field(description="New email addresses to add to the meeting")

class RetrievalRequest(BaseModel):
    year: int = Field(description="The year to filter by (e.g., 2024)")
    month: Optional[int] = Field(
        default=None, ge=1, le=12, 
        description="Optional month to filter by (1-12). If omitted, retrieves the whole year."
    )

class DeleteInvite(BaseModel):
    event_id: str = Field(description="The unique ID of the existing Google Calendar event")
