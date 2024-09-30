from api.selenium import JobScrapper
from time import sleep

# Initialize the JobScrapper class
jobScrapper = JobScrapper(
    "https://www.linkedin.com"
    # "https://fr.indeed.com"
)
open = jobScrapper.open_url()
# add a sleep to wait for the page to load
sleep(3)
# dismiss the google popup if any
dismissed_google = jobScrapper.dismiss_google_popup()
# sign in
jobScrapper.login()
# add a sleep
sleep(3)
# accept the cookies if any
acceptTerms = jobScrapper.accept_cookies()
# add a sleep
sleep(1)
# go to the jobs page
jobScrapper.go_to_jobs_page()
# add a sleep
sleep(3)
# search for jobs in specific location and with specific keywords
jobScrapper.search_jobs(location='France', keywords="")
# add a sleep
sleep(3)
# scrape the jobs
jobs = jobScrapper.scrap_jobs()
# add a sleep
sleep(3)
