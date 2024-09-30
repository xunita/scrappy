from api.selenium import JobScrapper
from time import sleep

# Initialize the JobScrapper class
jobScrapper = JobScrapper(
    "https://www.linkedin.com"
    # "https://fr.indeed.com/jobs?q=dev&l=France"
)
open = jobScrapper.open_url()
# add a sleep to wait for the page to load
sleep(3)
# dismiss the popup if any
dismissed = jobScrapper.dismiss_popup()
# dismiss the popup if any
dismissed_google = jobScrapper.dismiss_google_popup()
# accept the cookies if any
acceptTerms = jobScrapper.accept_cookies()
# sign in
jobScrapper.login()
# add a sleep
sleep(3)
# go to the jobs page
jobScrapper.go_to_jobs_page()
# add a sleep
sleep(3)
# search for jobs
jobScrapper.search_jobs(location='France', keywords="")
# add a sleep
sleep(3)
# scrape the jobs
jobs = jobScrapper.scrap_jobs()
# add a sleep
sleep(3)
