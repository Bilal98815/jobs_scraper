#!/bin/bash

# Activate the virtual environment
source /home/bilal/DjangoProjects/venv/bin/activate

cd /home/bilal/DjangoProjects/new_jobs

scrapy crawl tkxel_jobs
scrapy crawl codefulcrum_jobs
scrapy crawl venturedive_jobs

deactivate
