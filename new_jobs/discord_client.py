import os
import requests

from dotenv import load_dotenv


load_dotenv()


class DiscordClient:
    def __init__(self, log):
        self.discord_webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
        self.log = log

    def send_discord_notification(self, title, location, url, company_name):
        message = f"**New Job Posted!**\n**Company:** {company_name}\n**Title:** {title}\n**Location:** {location}\n**Apply Here:** {url}"
        data = {"content": message}

        try:
            response = requests.post(self.discord_webhook_url, json=data)
            if response.status_code == 204:
                self.log(f"Discord notification sent for job: {title}")
            else:
                self.log(f"Failed to send Discord notification: {response.text}")
        except Exception as e:
            self.log(f"Error sending Discord notification: {e}")

    def send_scraper_alert(self):
        data = {"content": "Scraper has finished running."}
        try:
            response = requests.post(self.discord_webhook_url, json=data)
            if response.status_code == 204:
                self.log(f"Discord notification sent!")
            else:
                self.log(f"Failed to send Discord notification: {response.text}")
        except Exception as e:
            self.log(f"Error sending Discord notification: {e}")
