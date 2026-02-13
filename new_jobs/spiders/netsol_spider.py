import scrapy
import os
import json

from ..discord_client import DiscordClient


class NetsolJobsSpider(scrapy.Spider):
    name = "netsol_jobs"
    allowed_domains = ["careers.netsoltech.com"]
    start_urls = ["https://careers.netsoltech.com/openings/"]

    seen_jobs_file = "jobs_data/netsol_jobs.json"
    seen_jobs = set()
    discord_client = None

    def __init__(self, *args, **kwargs):
        super(NetsolJobsSpider, self).__init__(*args, **kwargs)
        self.discord_client = DiscordClient(log=self.log)

        if os.path.exists(self.seen_jobs_file):
            with open(self.seen_jobs_file, "r") as file:
                self.seen_jobs = set(json.load(file))

    def parse(self, response):
        jobs = response.xpath('//div[contains(@class,"loadmore-wrap")]/article[contains(@class,"noo_job")]')

        for job in jobs:
            title = job.xpath('.//h2[contains(@class,"loop-item-title")]/a/text()').get()
            location = job.xpath('.//span[contains(@class,"job-location")]/a/text()').get()
            full_url = job.xpath('./@data-url').get()

            if full_url not in self.seen_jobs:
                self.seen_jobs.add(full_url)
                self.discord_client.send_discord_notification(title, location, full_url, "Netsol")

        self.save_seen_jobs()

    def save_seen_jobs(self):
        with open(self.seen_jobs_file, "w") as file:
            json.dump(list(self.seen_jobs), file)
        self.log(f"Saved {len(self.seen_jobs)} seen jobs.")
