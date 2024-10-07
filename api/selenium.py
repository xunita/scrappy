from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import os
import spacy


from keywords.jobsKeys import jobsKeys
from utils.utils import urls

# class to navigate to a page


class JobScrapper:
    # selectors
    __jobId = 0
    __indeedSelectors = {
        "accept_cookies": {
            'id': 'onetrust-accept-btn-handler'
        }
    }
    __linkedinSelectors = {
        "dismiss_popup": {
            'selector': 'button.modal__dismiss',
        },
        "google_popup": {
            'id': 'close',
        },
        "accept_cookies": {
            'selector': 'button.artdeco-global-alert-action.artdeco-button.artdeco-button--inverse.artdeco-button--2.artdeco-button--primary',
        },
        "jobs_btn": {
            'xpath': '//ul[contains(@class, "top-nav-menu")]/li/a[4]',
            'selector': 'ul.global-nav__primary-items li:nth-child(3) a'
        },
        "join_form": {
            "selector": "form.join-form",
        },
        "login_form": {
            'class': 'login__form',
            "selector": "form.login__form",
        },
        'organization': {
            'class': 'org-top-card__primary-content',
            'selector': 'div.org-top-card__primary-content',
        },
        'profile': {
            'existed': 'div.pv-top-card__non-self-photo-wrapper',
            'class': 'profile-card-profile-picture-container',
            'selector': 'button.profile-card-profile-picture-container',
        },
        "sign_in": {
            'page_btn': {
                'selector': 'a.nav__button-secondary',
            },
            'submit_btn': {
                'selector': 'div.login__form_action_container button.btn__primary--large',
            },
            'username': {
                'id': 'username',
            },
            'password': {
                'id': 'password',
            },
        },
        'jobs_page': {
            'home': 'nav.jobs-home-scalable-nav',
            'selector': 'div.base-serp-page__filters',
            'search_location': {
                'selector': 'div.jobs-search-box__input--location input.jobs-search-box__text-input',
            },
            'search_keywords': {
                'selector': 'div.jobs-search-box__input--keyword input.jobs-search-box__text-input',
            },
            'form': {
                'selector': 'form.base-search-bar__form',
            },

            'submit_btn': {
                'selector': 'button.base-search-bar__submit-btn',
            }
        },
        'jobs_results': {
            'description': {
                'selector': '#job-details > div:nth-child(1)',
            },
            'read_jobs': {},
            'html_data': {},
            'card': {
                'selector': 'li.jobs-search-results__list-item div.job-card-container',
            },
            'search_list': {
                'selector': 'div.jobs-search-results-list',
            },
            'pagination_next': {
                'selector': 'button.jobs-search-pagination__button--next',
            },
        },
        'job_details': {
            'skills': {},
            'title': '',
        },
        'bs4': {
            'job_title': {
                'selector': '.job-details-jobs-unified-top-card__job-title',
            }
        }

    }

    # active url
    __activeUrl = {
        "linkedin": __linkedinSelectors,
        "indeed": __indeedSelectors
    }
    __driver = None
    # constructor

    def __init__(self, url, browserOpened=True):
        # the url
        self.__url = url
        if ('indeed' in url):
            self.__selectors = self.__activeUrl['indeed']
        elif ('linkedin' in url):
            self.__selectors = self.__activeUrl['linkedin']
        else:
            raise Exception("The url is not supported")
        # init the driver
        self.init_driver(browserOpened)

    # close the browser

    def exit_browser(self):
        self.__driver.quit()

    # destructor

    # quit the driver when the object is deleted
    # todo: be careful with this as it can cause browser to close unexpectedly when the object is deleted

    # def __del__(self):
    #     self.__driver.quit()

    # get the url

    def get_url(self):
        return self.__url

    # get the driver

    def get_driver(self):
        return self.__driver

    # init the driver

    def init_driver(self, browserOpened=True):
        # if the driver is not initialized(firefox by default)
        if (self.__driver is None):

            options = Options()

            # will not open the browser if the browserOpened is set to false
            if (not browserOpened):
                options.add_argument('--headless')
            self.__driver = webdriver.Firefox(options=options)

    # open the url

    def open_url(self):
        try:
            self.__driver.get(self.__url)
            self.__driver.maximize_window()
            login_page = WebDriverWait(self.__driver, 5).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, self.__selectors['login_form']['selector']))
            )
            if login_page is not None:
                return True
            return False
        except Exception as e:
            return False

    #  find elements by xpath

    def find_element_by_xpath(self, xpath):
        try:
            return self.__driver.find_element(By.XPATH, xpath)
        except Exception as e:
            return None

    #  find elements by selector

    def find_element_by_selector(self, selector):
        try:
            return self.__driver.find_element(By.CSS_SELECTOR, selector)
        except Exception as e:
            return None

    #  find elements by id

    def find_element_by_id(self, id):
        try:
            return self.__driver.find_element(By.ID, id)
        except Exception as e:
            return None

    #  find elements by tag name

    def find_element_by_tag(self, tag):
        try:
            return self.__driver.find_element(By.TAG_NAME, tag)
        except Exception as e:
            print(e)
            return None

    # find elements by class

    def find_elements_by_selector(self, selector):
        try:
            return self.__driver.find_elements(By.CSS_SELECTOR, selector)
        except Exception as e:
            return None

    # accept the cookies

    def accept_cookies(self):
        try:
            # check if the element has an id
            hasId = 'id' in self.__selectors['accept_cookies']
            # get the cookies element
            cookies = self.find_element_by_id(self.__selectors['accept_cookies']['id']) if hasId else self.find_element_by_selector(
                self.__selectors['accept_cookies']['selector'])

            # loop until the cookies element is found
            if cookies is not None:
                cookies.click()
            # return true if the cookies are accepted
            return True
        except Exception as e:
            return False

    # dismiss the popup

    def dismiss_popup(self):
        try:
            popup = self.find_element_by_selector(
                self.__selectors['dismiss_popup']['selector'])

            if popup is not None:
                popup.click()
            # return true if the popup is dismissed
            return True
        except Exception as e:
            return False

    # dismiss the dismiss_google_popup

    def dismiss_google_popup(self):
        try:
            # look  for a frame
            iframe = self.find_element_by_tag('iframe')
            if iframe is not None:
                #  switch to the iframe
                self.__driver.switch_to.frame(iframe)
                # get the google popup
                google_popup = self.find_element_by_id(
                    self.__selectors['google_popup']['id'])

                if google_popup is not None:
                    google_popup.click()

                # switch back to the default content
                self.__driver.switch_to.default_content()

            # return true if the popup is dismissed
            return True
        except Exception as e:
            return False

    # login to the page

    def login(self, username, password):
        try:
            # get the username input
            usernameTag = self.find_element_by_id(
                self.__selectors['sign_in']['username']['id'])
            # get the password input
            passwordTag = self.find_element_by_id(
                self.__selectors['sign_in']['password']['id'])
            # get the submit button
            submitTag = self.find_element_by_selector(
                self.__selectors['sign_in']['submit_btn']['selector'])
            # if the username and password are found
            if usernameTag is not None and passwordTag is not None:
                usernameTag.clear()
                passwordTag.clear()
                usernameTag.send_keys(username)
                passwordTag.send_keys(password)
                submitTag.click()
                profile = WebDriverWait(self.__driver, 5).until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, self.__selectors['profile']['selector']))
                )
                if (self.__selectors['profile']['class'] in profile.get_attribute('class')):
                    return True
                else:
                    # redirect to the login page
                    self.__driver.get(self.__url)
            else:
                self.__driver.get(self.__url)
            return False
        except Exception as e:
            return False

    # go to the jobs page

    def go_to_jobs_page(self):
        try:
            # go to the jobs page
            self.__driver.get('https://www.linkedin.com/jobs/')
            # check if the jobs page is loaded
            job_home = WebDriverWait(self.__driver, 5).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, self.__selectors['jobs_page']['home']))
            )
            if job_home is not None:
                return True
            return False
        except Exception as e:
            return False

    #  scroll to the bottom of the page

    def scroll_to_bottom(self, selector):
        try:
            # get the body element
            list = self.find_element_by_selector(selector)
            if list is not None:
                # Scroll down and check if new content is loaded
                last_height = self.__driver.execute_script(
                    "return arguments[0].scrollHeight;", list)
                # scroll to the bottom of the page
                while True:
                    # Scroll down the div
                    self.__driver.execute_script(
                        "arguments[0].scrollTop = arguments[0].scrollHeight;", list)

                    # Wait for new content to load (adjust time if needed)
                    sleep(1.5)

                    # Check new scroll height and compare with last scroll height
                    new_height = self.__driver.execute_script(
                        "return arguments[0].scrollHeight;", list)

                    if new_height == last_height:
                        # If the height hasn't changed, all content is loaded
                        break
                    last_height = new_height
                return True
            return False
        except Exception as e:
            return False

    # find and suggest
    def find_and_suggest(self, keyword, location, maxjobs):
        try:
            # read the saved
            nbJobs = 0
            self.search_jobs(location, keyword)
            self.scrap_jobs(nbJobs, maxjobs)
            # print nbJobs scrapped
            print(
                f'{len(self.__selectors['jobs_results']['html_data'])} jobs scrapped')
            return True
        except Exception as e:
            return False

    # search for jobs
    def search_jobs(self, location='France', keywords=""):
        try:
            # get the search location
            search_location = self.find_element_by_selector(
                self.__selectors['jobs_page']['search_location']['selector'])
            # get the search keywords
            search_keywords = self.find_element_by_selector(
                self.__selectors['jobs_page']['search_keywords']['selector'])

            # if the search keywords is found
            if search_keywords is not None:
                search_keywords.clear()
                search_keywords.send_keys(keywords)
            # if the search location is found
            if search_location is not None:
                search_location.clear()
                search_location.send_keys(location)
            #  sleep for 4 seconds
            sleep(2)
            #  press the enter key
            actions = ActionChains(self.__driver)
            actions.send_keys(Keys.ENTER)
            actions.perform()
            # sleep for 4 seconds
            sleep(3)
            # scroll to the bottom of the page
            return self.scroll_to_bottom(
                self.__selectors['jobs_results']['search_list']['selector'])

        except Exception as e:
            return False

    # go next page

    def go_next_page(self):
        try:
            # get the next button
            next_btn = self.find_element_by_selector(
                self.__selectors['jobs_results']['pagination_next']['selector'])
            # if the next button is found
            if next_btn is not None:
                next_btn.click()
                # add a sleep
                sleep(2.5)
                # scroll to the bottom of the page
                return self.scroll_to_bottom(
                    self.__selectors['jobs_results']['search_list']['selector'])
            return False
        except Exception as e:
            return False

    # scrap the jobs

    def scrap_jobs(self, nbJobs, maxJobs):
        try:
            breakFor = False
            while True:
                # get the jobs results
                jobs_results = self.find_elements_by_selector(
                    self.__selectors['jobs_results']['card']['selector'])
                # if the jobs results are found
                if jobs_results is not None:
                    for job in jobs_results:
                        self.__jobId = self.__jobId + 1
                        job.click()
                        #
                        sleep(2)
                        # save the html data
                        self.__selectors['jobs_results']['html_data'][f'{
                            self.__jobId}'] = self.__driver.page_source

                        # increment the number of jobs
                        nbJobs += 1

                        if nbJobs >= maxJobs:
                            breakFor = True
                            break

                    if breakFor:
                        break
                    # go to the next page
                    hasNext = self.go_next_page()
                    #
                    if not hasNext:
                        break
                else:
                    break
            # check if the html data is not empty
            if not self.__selectors['jobs_results']['html_data']:
                return False
            # save the jobs data to a json file
            return self.save_jobs_html()
        except Exception as e:
            print(e)
            return False

    # save the jobs data as individual html files

    def save_jobs_html(self):
        try:
            # save the jobs data to a json file
            for jobId, jobData in self.__selectors['jobs_results']['html_data'].items():
                with open(f'jobs/job_{jobId}.html', 'w', encoding='utf-8') as f:
                    f.write(jobData)
            return True
        except Exception as e:
            return False

    # read jobs from jobs dir (html files), i dont know number of jobs so i will read all the files in the jobs dir
    def read_saved_jobs(self):
        try:
            # get the jobs dir
            jobsDir = os.listdir('jobs')
            # iterate over the jobs dir
            for job in jobsDir:
                # read the job file
                with open(f'jobs/{job}', 'r', encoding='utf-8') as f:
                    self.__selectors['jobs_results']['read_jobs'][job] = f.read()
            return True
        except Exception as e:
            print(e)
            return False

    #  show the jobs titles
    def show_jobs_titles(self):
        try:
            if (len(self.__selectors['jobs_results']['read_jobs']) == 0):
                print("No jobs saved")
                return False
            for job, jobData in self.__selectors['jobs_results']['read_jobs'].items():
                # format and save the job data to a pandas dataframe
                soup = BeautifulSoup(jobData, 'html.parser')
                jobTitles = soup.select_one(
                    self.__selectors['bs4']['job_title']['selector'])
                jobDescriptionsP = soup.find(id='job-details')
                jobDescriptions = jobDescriptionsP.find('div')
                print(jobTitles.get_text(strip=True))
                print(jobDescriptions.get_text(strip=True))
                print(self.extract_skills(
                    jobTitles.get_text(strip=True), jobDescriptions.get_text(strip=True)))
            return True
        except Exception as e:
            print(e)
            return False

    # scrap a profile
    def scrap_profile(self, profile):
        try:
            # open the profile url
            profile_url = f'https://www.linkedin.com/in/{profile}'
            self.__driver.get(profile_url)
            exist = WebDriverWait(self.__driver, 5).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, self.__selectors['profile']['existed']))
            )
            if exist is not None:
                # exist
                print("Profile exists")
                return True

            return False
        except Exception as e:
            return False

    # scrap a company
    def scrap_company(self, company):
        try:
            # open the company url
            company_url = f'https://www.linkedin.com/company/{company}'
            self.__driver.get(company_url)
            exist = WebDriverWait(self.__driver, 5).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, self.__selectors['organization']['selector']))
            )
            if exist is not None:
                # exist
                print("Company exists")
                return True
            else:
                print("Company does not exist")
            return False
        except Exception as e:
            return False

    #  extract skills (this will transform the job description into a list of potential skills to clean and analyze)
    def extract_skills(self, jobTitle, description):
        try:
            print('------------------------------------------------------')
            print(f'Extracting skills for Job: {jobTitle}')
            print('------------------------------------------------------')
            # extract the
            nlp = spacy.load("fr_core_news_sm")
            skills = []
            doc = nlp(description)
            # Extract nouns, proper nouns, and verbs
            for token in doc:
                if token.pos_ in ['NOUN', 'PROPN', 'VERB']:
                    skills.append(token.text)

            # only return the skills that might be relevant to the job (prediction)

            return skills
        except Exception as e:
            return []
