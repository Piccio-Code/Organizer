import datetime
import json
import os.path
from colorist import hex

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


SCOPES = ["https://www.googleapis.com/auth/calendar"]

def delete_all_events(service):
  events = service.events().list(calendarId='primary').execute()['items']

  for event in events:
    service.events().delete(calendarId='primary', eventId=event['id']).execute()

def print_colors(service):
  colors: dict = service.colors().get().execute()['event']

  for code, body in colors.items():
    hex_code = body['background']
    hex(code, hex_code)


def main():
  creds = None

  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)

  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  event = {
    'summary': 'SCHOOL',
    'location': '800 Howard St., San Francisco, CA 94103',
    'description': 'A chance to hear more about Google\'s developer products.',
    'start': {
      'dateTime': '2025-08-18T08:00:00',
      'timeZone': 'Europe/Rome',
    },
    'end': {
      'dateTime': '2025-08-18T14:00:00',
      'timeZone': 'Europe/Rome',
    },
    'recurrence': [
      'RRULE:FREQ=WEEKLY;BYDAY=MO,TU,WE,TH,FR'
    ],
    'colorId': '8',
    'reminders': {
      'useDefault': False,
      'overrides': [
        {'method': 'email', 'minutes': 24 * 60},
        {'method': 'popup', 'minutes': 10},
      ],
    },
  }

  try:
    service = build("calendar", "v3", credentials=creds)




    delete_all_events(service)

    # event = service.events().insert(calendarId='primary', body=event).execute()

    print_colors(service)

  except HttpError as error:
    print(f"An error occurred: {error}")



if __name__ == "__main__":
  main()