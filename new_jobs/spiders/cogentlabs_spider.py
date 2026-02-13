import scrapy
import os
import json

from ..discord_client import DiscordClient


class CogentLabsJobsSpider(scrapy.Spider):
    name = "cogentlabs_jobs"
    start_urls = ["https://cogent-labs.hirestream.io/api/v1/jobs/published-jobs/?timezone=Asia%2FKarachi"]

    seen_jobs_file = "jobs_data/cogentlabs_jobs.json"
    seen_jobs = set()
    discord_client = None

    def __init__(self, *args, **kwargs):
        super(CogentLabsJobsSpider, self).__init__(*args, **kwargs)
        self.discord_client = DiscordClient(log=self.log)

        if os.path.exists(self.seen_jobs_file):
            with open(self.seen_jobs_file, "r") as file:
                self.seen_jobs = set(json.load(file))

    def parse(self, response):
        data = response.json()
        jobs = data.get('results')
        if not jobs:
            return

        for job in jobs:
            title = job.get('title', '')
            location = job.get('location', 'x')
            full_url = f"https://cogent-labs.hirestream.io/api/v1/jobs/{job.get('uuid')}/view-job/?timezone=Asia%2FKarachi"

            if full_url not in self.seen_jobs:
                self.seen_jobs.add(full_url)
                self.discord_client.send_discord_notification(title, location, full_url, "Cogent Labs")

        self.save_seen_jobs()

    def save_seen_jobs(self):
        with open(self.seen_jobs_file, "w") as file:
            json.dump(list(self.seen_jobs), file)
        self.log(f"Saved {len(self.seen_jobs)} seen jobs.")
