import scrapy
import os
import json

from ..discord_client import DiscordClient


class TenPearlsJobsSpider(scrapy.Spider):
    name = "10pearls_jobs"
    allowed_domains = ["10pearls.com"]
    start_urls = ["https://api.resumatorapi.com/v1/jobs?apikey=jB0b57gnKdU9rqBWvqQpxzITAPrHUFaz"]

    seen_jobs_file = "jobs_data/10pearls_jobs.json"
    seen_jobs = set()
    discord_client = None

    def __init__(self, *args, **kwargs):
        super(TenPearlsJobsSpider, self).__init__(*args, **kwargs)
        self.discord_client = DiscordClient(log=self.log)

        if os.path.exists(self.seen_jobs_file):
            with open(self.seen_jobs_file, "r") as file:
                self.seen_jobs = set(json.load(file))

    def parse(self, response):
        all_jobs = response.json()
        if not all_jobs:
            return

        lahore_jobs = []
        for job in all_jobs:
            if job.get("status") == 'Open' and 'lahore' in job.get('city', '').lower():
                lahore_jobs.append(job)

        if not lahore_jobs:
            return

        for job in lahore_jobs:
            title = job.get('title', '')
            location = 'Lahore'
            full_url = f"https://10pearls.com/lahore-job-openings/?jobid={job.get('id')}"

            if full_url not in self.seen_jobs:
                self.seen_jobs.add(full_url)
                self.discord_client.send_discord_notification(title, location, full_url, "10Pearls")

        self.discord_client.send_scraper_alert()
        self.save_seen_jobs()

    def save_seen_jobs(self):
        with open(self.seen_jobs_file, "w") as file:
            json.dump(list(self.seen_jobs), file)
        self.log(f"Saved {len(self.seen_jobs)} seen jobs.")
