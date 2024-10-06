from api.selenium import JobScrapper
from time import sleep

# Initialize the JobScrapper class and open the browser if needed
jobScrapper = JobScrapper(
    "https://www.linkedin.com"    # "https://fr.indeed.com"
    , browserOpened=False
)
# # go to the url
# open = jobScrapper.open_url()
# # add a sleep to wait for the page to load
# sleep(3)
# # dismiss the google popup if any
# dismissed_google = jobScrapper.dismiss_google_popup()
# # sign in
# jobScrapper.login()
# # add a sleep
# sleep(3)
# # accept the cookies if any
# acceptTerms = jobScrapper.accept_cookies()
# # add a sleep
# sleep(1)
# # go to the jobs page
# jobScrapper.go_to_jobs_page()
# # add a sleep
# sleep(3)
# # find jobs by keywords
# jobScrapper.find_jobs()
# # add a sleep
# sleep(3)

# read the saved jobs
jobScrapper.read_saved_jobs()
# show the jobs titles
jobScrapper.show_jobs_titles()
