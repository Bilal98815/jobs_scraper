import scrapy
import os
import json

from ..discord_client import DiscordClient


class TkxelJobsSpider(scrapy.Spider):
    name = "tkxel_jobs"
    allowed_domains = ["careers.tkxel.com"]
    start_urls = ["https://careers.tkxel.com/jobs/"]

    seen_jobs_file = "jobs_data/tkxel_jobs.json"
    seen_jobs = set()
    discord_client = None

    def __init__(self, *args, **kwargs):
        super(TkxelJobsSpider, self).__init__(*args, **kwargs)
        self.discord_client = DiscordClient(log=self.log)

        if os.path.exists(self.seen_jobs_file):
            with open(self.seen_jobs_file, "r") as file:
                self.seen_jobs = set(json.load(file))

    def parse(self, response):
        jobs = response.xpath('//div[@class="job-card"]')
        for job in jobs:
            title = job.xpath('.//h6/text()').get().strip()
            location = job.xpath('.//div[contains(@class, "job-location")]/p/text()').get().strip()
            job_url = job.xpath('.//a/@href').get()
            full_url = response.urljoin(job_url)

            if full_url not in self.seen_jobs:
                self.seen_jobs.add(full_url)
                self.discord_client.send_discord_notification(title, location, full_url, "Tkxel")

        self.save_seen_jobs()

    def save_seen_jobs(self):
        with open(self.seen_jobs_file, "w") as file:
            json.dump(list(self.seen_jobs), file)
        self.log(f"Saved {len(self.seen_jobs)} seen jobs.")
