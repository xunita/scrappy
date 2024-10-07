from api.selenium import JobScrapper
from getpass import getpass
from time import sleep

# variables
openedTentatives = 0
logged = False
opened = False
#
print("-------------------- LinkedIn Job Scrapper --------------------")
print("Welcome to the LinkedIn Job Scrapper !")
print("This program will scrap the job offers from the website of your choice and suggest the skills you need to acquire to get the job you want.")
print("Please, follow the instructions below to get started.")
print("make sure to have access to internet for the application to work properly.")
print("------------------------------------------------------")

print("Please connect to your LinkedIn account to get started.")
print("username: ")
username = input()
password = getpass("password: ")

# Initialize the JobScrapper class and open the browser if needed
jobScrapper = JobScrapper(
    "https://www.linkedin.com/login"    # "https://fr.indeed.com"
    , browserOpened=True
)

# open the browser (hidden to the user if the browserOpened is set to False)
while not opened:
    opened = jobScrapper.open_url()
    openedTentatives += 1
    if (openedTentatives > 3):
        break

# exit if the browser is not opened
if (not opened):
    print("Please verify your internet connection and try again.")
    exit()

while not logged:
    logged = jobScrapper.login(username, password)
    if not logged:
        print("Please verify your credentials and try again or you may need to manually enter a code to login.")
        username = input("username: ")
        password = getpass("password: ")

print("You have successfully logged in.")

print("-------------------- Scrapping Options --------------------")
print("Enter 1 to scrap the job offers (will suggest the skills you need to acquire).")

# coming soon
print("Enter 2 to scrap a profile.")
print("Enter 3 to scrap a company.")
print("Enter 0 to exit.")
print("------------------------------------------------------")

option = input("Enter your choice: ")
while option != "0":
    if option == "1":
        keyword = input("Please enter a job title: ")
        location = input(
            "Please enter a location (press Enter to skip with default location to France): ")
        nbJobs = input(
            "Please enter the number of jobs to scrap (large number is recommended for better suggestions but it may take longer): ")
        # check if the number of jobs is a valid number
        while not nbJobs.isdigit() or int(nbJobs) <= 0:
            print("Please enter a valid number (greater than 0).")
            nbJobs = input("Please enter the number of jobs to scrap: ")
        # check if the location is empty
        if location == "":
            location = "France"

        # go to the job search page
        inJobPage = jobScrapper.go_to_jobs_page()
        while not inJobPage:
            print("retrying to go to the job search page.")
            inJobPage = jobScrapper.go_to_jobs_page()

        print("Scrapping the job offers. Please wait...")
        # launch the scrapping
        jobScrapper.find_and_suggest(keyword, location, int(nbJobs))

    elif option == "2":
        print("Please enter the profile you want to scrap.")
        profile = input()
        jobScrapper.scrap_profile(profile)
    elif option == "3":
        print("Please enter the company you want to scrap.")
        company_url = input()
        jobScrapper.scrap_company(company_url)
    else:
        print("Invalid choice. Please enter a valid choice.")
    print("-------------------- Scrapping Options --------------------")
    print("Enter 1 to scrap the job offers (will suggest the skills you need to acquire).")
    print("Enter 2 to scrap a profile.")
    print("Enter 3 to scrap a company.")
    print("Enter 0 to exit.")
    print("------------------------------------------------------")
    option = input("Enter your choice: ")

print("Thank you for using the LinkedIn Job Scrapper. Goodbye !")
