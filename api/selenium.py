from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep

from keywords.jobsKeys import jobsKeys
from utils.utils import urls

# class to navigate to a page


class JobScrapper:
    # selectors
    __indeedSelectors = {
        "accept_cookies": {
            'id': 'onetrust-accept-btn-handler'
        }
    }
    __linkedinSelectors = {
        'username': 'theivorian97@gmail.com',
        'password': 'Azerty@12',
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
            'html_data': [],
            'card': {
                'selector': 'li.jobs-search-results__list-item div.job-card-container',
            },
            'search_list': {
                'selector': 'div.jobs-search-results-list',
            },
            'pagination_next': {
                'selector': 'button.jobs-search-pagination__button--next',
            },
        }

    }

    # active url
    __activeUrl = {
        "linkedin": __linkedinSelectors,
        "indeed": __indeedSelectors
    }
    __driver = None
    # constructor

    def __init__(self, url):
        # the url
        self.__url = url
        if ('indeed' in url):
            self.__selectors = self.__activeUrl['indeed']
        elif ('linkedin' in url):
            self.__selectors = self.__activeUrl['linkedin']
        # init the driver
        self.init_driver()

    # destructor

    def exit(self):
        self.__driver.quit()

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

    def init_driver(self):
        # if the driver is not initialized(firefox by default)
        if (self.__driver is None):
            self.__driver = webdriver.Firefox()

    # open the url async

    def open_url(self):
        try:
            self.__driver.get(self.__url)
            self.__driver.maximize_window()
            return True
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

    def login(self):
        try:
            # get the sign in button
            sign_in = self.find_element_by_selector(
                self.__selectors['sign_in']['page_btn']['selector'])
            # if the sign in button is found
            if sign_in is not None:
                sign_in.click()
                sleep(3)
                # get the username input
                username = self.find_element_by_id(
                    self.__selectors['sign_in']['username']['id'])
                # get the password input
                password = self.find_element_by_id(
                    self.__selectors['sign_in']['password']['id'])
                # get the submit button
                submit = self.find_element_by_selector(
                    self.__selectors['sign_in']['submit_btn']['selector'])
                # if the username and password are found
                if username is not None and password is not None:
                    username.send_keys(self.__selectors['username'])
                    password.send_keys(self.__selectors['password'])
                    submit.click()
                    return True
            return False
        except Exception as e:
            return False

    # go to the jobs page

    def go_to_jobs_page(self):
        try:
            # get the jobs button
            jobs = self.find_element_by_selector(
                self.__selectors['jobs_btn']['selector'])
            #  click the jobs button
            if jobs is not None:
                jobs.click()
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
                    sleep(3)

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
                sleep(5)
                # scroll to the bottom of the page
                return self.scroll_to_bottom(
                    self.__selectors['jobs_results']['search_list']['selector'])
            return False
        except Exception as e:
            return False

    # scrap the jobs

    def scrap_jobs(self):
        try:
            self.__selectors['jobs_results']['html_data'].clear()
            # iterate over the pages
            while True:
                # get the jobs results
                jobs_results = self.find_elements_by_selector(
                    self.__selectors['jobs_results']['card']['selector'])
                # if the jobs results are found
                if jobs_results is not None:
                    for job in jobs_results:
                        job.click()
                        sleep(3)
                        # save the html data
                        self.__selectors['jobs_results']['html_data'].append(
                            self.__driver.page_source)
                    # go to the next page
                    hasNext = self.go_next_page()
                    # check if there is no next page then break
                    if(not hasNext):
                        break
                    sleep(3)
                else:
                    break
            return True
        except Exception as e:
            return False
