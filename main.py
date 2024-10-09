from api.selenium import JobScrapper
from getpass import getpass
from time import sleep

# variables
openedTentatives = 0
logged = False
opened = False
#
print("-------------------- LinkedIn Scrapper --------------------")
print("Welcome to the LinkedIn Alumni scrapper !")
print("This program will scrap data about alumni from a specific school with a range of years and job titles.")
print("Please, follow the instructions below to get started.")
print("make sure to have access to internet for the application to work properly.")
print("------------------------------------------------------")
print("Initializing the Scrapper...")

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

print("The Scrapper is ready to use.")


print("Please connect to your LinkedIn account to get started.")
print("username: ")
username = input()
password = getpass("password: ")


while not logged:
    logged = jobScrapper.login(username, password)
    if not logged:
        print(
            "Please verify your credentials and try again or you may need to manually enter a code to login.")
        username = input("username: ")
        password = getpass("password: ")

print("You have successfully logged in.")
# add a sleep time
sleep(2)

school = input("Enter the school name (school id on linkedin) or 0 to quit: ")
while school != "0":
    job = input("Enter the job title: ")
    startYear = input("Enter the start year: ")
    # check years are valid
    while (not startYear.isdigit() or int(startYear) < 1900):
        print("Please enter a valid year.")
        startYear = input("Enter the start year: ")

    endYear = input("Enter the end year: ")
    # check years are valid
    while (not endYear.isdigit() or int(endYear) < 1900):
        print("Please enter a valid year.")
        endYear = input("Enter the end year: ")

    print("Getting the data...")

    jobScrapper.find_school_alumni(school, job, startYear, endYear)

    school = input(
        "Enter the school name (school id on linkedin) or 0 to quit: ")

print("Goodbye !")
