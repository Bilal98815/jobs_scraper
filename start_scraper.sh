#!/bin/bash

# Activate the virtual environment
source /home/user/DjangoProjects/new_jobs/.venv/bin/activate

cd /home/user/DjangoProjects/new_jobs

scrapy crawl tkxel_jobs
scrapy crawl codefulcrum_jobs
scrapy crawl venturedive_jobs
scrapy crawl xref_jobs
scrapy crawl netsol_jobs
scrapy crawl cogentlabs_jobs
scrapy crawl 10pearls_jobs

deactivate
