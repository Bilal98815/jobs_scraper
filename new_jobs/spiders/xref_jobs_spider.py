import scrapy
import os
import json

from ..discord_client import DiscordClient


class XrefJobsSpider(scrapy.Spider):
    name = "xref_jobs"
    allowed_domains = ["careers.smartrecruiters.com"]
    start_urls = ["https://careers.smartrecruiters.com/Xref3"]

    seen_jobs_file = "jobs_data/xref_jobs.json"
    seen_jobs = set()
    discord_client = None

    def __init__(self, *args, **kwargs):
        super(XrefJobsSpider, self).__init__(*args, **kwargs)
        self.discord_client = DiscordClient(log=self.log)

        if os.path.exists(self.seen_jobs_file):
            with open(self.seen_jobs_file, "r") as file:
                self.seen_jobs = set(json.load(file))

    def parse(self, response):
        sections = response.xpath('//section[contains(@class,"opening")]')
        for section in sections:
            location = section.xpath('.//h3[contains(@class,"opening-title")]/text()').get(default="").strip()
            jobs = section.xpath('.//li[contains(@class,"opening-job")]')
            for job in jobs:
                title = job.xpath('.//h4[contains(@class,"job-title")]/text()').get(default="").strip()
                job_url = job.xpath('.//a/@href').get()
                if not job_url:
                    continue
                full_url = response.urljoin(job_url)

                if full_url not in self.seen_jobs:
                    self.seen_jobs.add(full_url)
                    self.discord_client.send_discord_notification(title, location, full_url, "Xref")

        self.save_seen_jobs()

    def save_seen_jobs(self):
        with open(self.seen_jobs_file, "w") as file:
            json.dump(list(self.seen_jobs), file)
        self.log(f"Saved {len(self.seen_jobs)} seen jobs.")
