# Job Scraper

This scraper monitors job postings from multiple companies (Tkxel, VentureDive, and CodeFulcrum) and sends new job notifications to a Discord channel. It keeps track of previously seen jobs to avoid duplicate notifications.

## Features
- Scrapes job listings from multiple companies
- Sends notifications to Discord channel
- Tracks seen jobs to avoid duplicates
- Can be automated to run daily

## Setup Instructions

1. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Linux/Mac
# OR
.\venv\Scripts\activate  # On Windows
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Create `.env` file in the project root and add your Discord webhook URL:
```bash
DISCORD_WEBHOOK_URL=your_discord_webhook_url_here
```

## Running the Scraper

To run the scraper manually:
```bash
./start_scraper.sh
```

## Automated Daily Execution

To run the scraper daily, you can set up a cron job. Here's how:

1. Open crontab editor:
```bash
crontab -e
```

2. Add the following line to run the scraper daily at 9 AM:
```bash
0 9 * * * cd /path/to/new_jobs && ./start_scraper.sh >> /path/to/new_jobs/logs/cron.log 2>&1
```

Make sure to:
- Replace `/path/to/new_jobs` with your actual project path
- Ensure `start_scraper.sh` has execute permissions:
```bash
chmod +x start_scraper.sh
```

## Project Structure
- `spiders/`: Contains individual spiders for each company
- `jobs_data/`: Stores seen jobs data
- `logs/`: Contains scraper logs
- `start_scraper.sh`: Script to run all spiders
- `.env`: Configuration file for environment variables
