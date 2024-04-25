# Used Cars Scraping
# Task:
Scraping site via Selenium.

You need to create an application for periodic scraping of the AutoRia platform (a link can be hardcoded).
The application should be launched every day at the time specified in the settings (for example, 12:00)
and go through all pages from the start page to the end, going into each used car card and saving data to database.

Conditions:
- All data must be stored in a PostgreSQL database.
- No duplicates.
- The application should perform a daily database dump at the time specified in the settings (for example, 12:00) 
and store the dump files in the “dumps” folder, which should be located in the root folder of the application.
- Use pip as a package manager.
- Application settings should be stored in a .env file
- The application folder should contain a Readme.md file with a description of the structure and steps to launch the application.
- Send the finished test as a link to GitHub.

Database fields:
- url (string)
- title (string)
- price_usd (integer, $)
- odometer (integer, km)
- username (string)
- phone_number (string)
- image_url (string)
- images_count (string)
- car_number (string)
- car_vin (string)
- datetime_found (date)

# Overview
This repository contains Python scripts for scraping data from car sales site with daily period. 
The script is waiting activating time and start save dump database. 
After that it starts to scan first page of target site and finds all individual links of cars.
If link is not in database it scraps needed fields and save to database.
After all linksi script finds the next page and repeats. 
If it finds the end page or not finds next it finish scraps. 
Wait next activating time for dump and starts again.


# Requirements
- Python 3.10
- Selenium
- SQLAlchemy 2.0
- Alembic
- Other dependencies (install using "pip install -r requirements.txt")

# Usage:
- update project from Git
- create virtual environment 
```bash
pip install -r requirements.txt
```
- create '.env' file with credentials and set settings (sample names in '.env.example').
- run in terminal: `alembic upgrade head` -> implementation current models to DB
- run main.py for start 
```bash
python  main.py
```
- wait for the activation time when the database dump starts and scraping begins.

# Recommendation: 
- The start page is 1
- The end page is bigger than the start page
- The end page can be None for scraping all pages 
- 1 cars page is scraping about 10 seconds and 10 per page. So it is equal 1400 pages per day with target 30 000 pages
- Dump tested only for docker container of postgresql
