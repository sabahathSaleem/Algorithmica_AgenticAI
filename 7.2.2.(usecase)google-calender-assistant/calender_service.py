import datetime
import calendar
from pathlib import Path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from models import MeetingInvite, UpdateInvite, RetrievalRequest

class CalenderService:
    def __init__(self):
        script_location = Path(__file__).parent
        cred_file_path = script_location / 'cred.json'
        SCOPES = ['https://www.googleapis.com/auth/calendar']
        flow = InstalledAppFlow.from_client_secrets_file(cred_file_path, SCOPES)
        creds = flow.run_local_server(port=0)
        self.service = build('calendar', 'v3', credentials=creds)

    def create_google_invite(self, invite: MeetingInvite) -> str:
        try:
            end_time = invite.start_time + datetime.timedelta(minutes=invite.duration_minutes)
            start_str = invite.start_time.strftime('%Y-%m-%dT%H:%M:%SZ')
            end_str = end_time.strftime('%Y-%m-%dT%H:%M:%SZ')
            
            event_body = {
                'summary': invite.title,
                'start': {'dateTime': start_str, 'timeZone': 'UTC'},
                'end': {'dateTime': end_str, 'timeZone': 'UTC'},
                'attendees': [{'email': email} for email in invite.attendees],
            }
            print(event_body)
            event = self.service.events().insert(
                calendarId='primary', body=event_body, sendUpdates='all'
            ).execute()
            return f"New invite sent for '{invite.title}'! Link: {event.get('htmlLink')}"
        except Exception as e:
            print(f"Failed to create invite: {str(e)}")
            raise e
        

    def update_google_invite(self, update: UpdateInvite) -> str:
        try:
            event = self.service.events().get(calendarId='primary', eventId=update.event_id).execute()
            current_attendees = event.get('attendees', [])
            existing_emails = {a.get('email') for a in current_attendees}
            
            for email in update.new_attendees:
                if email not in existing_emails:
                    current_attendees.append({'email': email})

            self.service.events().patch(
                calendarId='primary', eventId=update.event_id, 
                body={'attendees': current_attendees}, sendUpdates='all'
            ).execute()
            return f"Successfully added {len(update.new_attendees)} people to event {update.event_id}."
        except Exception as e:
            print(f"Failed to update invite: {str(e)}")
            raise e

    def list_google_calender_events_by_date(self, params: RetrievalRequest) -> str:
        try:
            if params.month:
                start = datetime.datetime(params.year, params.month, 1)
                _, last = calendar.monthrange(params.year, params.month)
                end = datetime.datetime(params.year, params.month, last, 23, 59, 59)
            else:
                start = datetime.datetime(params.year, 1, 1)
                end = datetime.datetime(params.year, 12, 31, 23, 59, 59)

            all_events, page_token = [], None
            while True:
                res = self.service.events().list(
                    calendarId='primary', timeMin=start.isoformat()+'Z', timeMax=end.isoformat()+'Z',
                    pageToken=page_token, singleEvents=True, orderBy='startTime'
                ).execute()
                all_events.extend(res.get('items', []))
                page_token = res.get('nextPageToken')
                if not page_token: break

            if not all_events: return "No events found for that period."
            return "\n".join([f"- {e['summary']} ({e['start'].get('dateTime', e['start'].get('date'))}) ID: {e['id']}" for e in all_events])
        except Exception as e:
            print(f"Failed to retrieve events: {str(e)}")
            raise e
        
    def list_google_calender_events_by_title(self, title_query: str) -> list:
        try:
            # The 'q' parameter performs a free-text search
            events_result = self.service.events().list(
                calendarId='primary',
                q=title_query, 
                singleEvents=True
            ).execute()
            
            return events_result.get('items', [])
        except Exception as e:
            print(f"Search failed: {str(e)}")
            return []
        
    def delete_google_invite(self, event_id: str) -> str:
        try:
            self.service.events().delete(
                calendarId='primary', 
                eventId=event_id, 
                sendUpdates='all'
            ).execute()
            return f"Successfully deleted event with ID: {event_id}"
        except Exception as e:
            print(f"Failed to delete invite: {str(e)}")
            raise e

