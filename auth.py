# auth.py
from __future__ import annotations
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
import os

SCOPES = ["https://www.googleapis.com/auth/calendar"]

def main():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # Usa automaticamente redirect compatível com Desktop
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)  # NÃO muda redirect_uri na mão

        with open("token.json", "w") as token:
            token.write(creds.to_json())

    service = build("calendar", "v3", credentials=creds)
    print("✅ Google Calendar autenticado!")
    events_result = service.events().list(
        calendarId="primary", maxResults=3, singleEvents=True, orderBy="startTime"
    ).execute()
    for ev in events_result.get("items", []):
        print(" -", ev.get("summary"), ev.get("start"))

if __name__ == "__main__":
    main()
