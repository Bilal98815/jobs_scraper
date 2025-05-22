import scrapy
import os
import json

from ..discord_client import DiscordClient


class VenturediveJobsSpider(scrapy.Spider):
    name = "venturedive_jobs"
    allowed_domains = ["venturedive.applytojob.com"]
    start_urls = ["https://venturedive.applytojob.com/apply"]

    seen_jobs_file = "jobs_data/venturedive_jobs.json"
    seen_jobs = set()
    discord_client = None

    def __init__(self, *args, **kwargs):
        super(VenturediveJobsSpider, self).__init__(*args, **kwargs)
        self.discord_client = DiscordClient(log=self.log)

        if os.path.exists(self.seen_jobs_file):
            with open(self.seen_jobs_file, "r") as file:
                self.seen_jobs = set(json.load(file))

    def parse(self, response):
        jobs = response.xpath('//tr[contains(@class,"resumator-table-row")]')
        for job in jobs:
            title = job.xpath('.//td[@class="resumator-job-title-column"]/a/text()').get().strip()
            location = job.xpath('.//td[@class="resumator-job-location-column"]/text()').get().strip()
            job_url = job.xpath('.//td[@class="resumator-job-title-column"]/a/@href').get()
            full_url = response.urljoin(job_url)

            if full_url not in self.seen_jobs:
                self.seen_jobs.add(full_url)
                self.discord_client.send_discord_notification(title, location, full_url, "Venturedive")

        self.discord_client.send_scraper_alert()
        self.save_seen_jobs()

    def save_seen_jobs(self):
        with open(self.seen_jobs_file, "w") as file:
            json.dump(list(self.seen_jobs), file)
        self.log(f"Saved {len(self.seen_jobs)} seen jobs.")
