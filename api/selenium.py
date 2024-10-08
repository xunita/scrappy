from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import json


from keywords.jobsKeys import jobsKeys
from utils.utils import urls

# class to navigate to a page


class JobScrapper:
    # selectors
    __linkedinSelectors = {
        'show_more': {
            'selector': 'button.org-people__show-more-button',
        },
        'no_alumni': {
            'selector': 'div.org-people__no-data-container'
        },
        'has_alumni_result': {
            'selector': 'div.org-people__insights-container div.artdeco-carousel__content'
        },
        'profile': {
            'existed': 'div.pv-top-card__non-self-photo-wrapper',
            'class': 'profile-card-profile-picture-container',
            'selector1': 'a.profile-card-profile-picture-container',
            'selector2': 'button.profile-card-profile-picture-container',
        },
        'login_form': {
            'class': 'login__form',
            "selector": "form.login__form",
        },
        'sign_in': {
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
        'bs4': {
            'alumni_cols': 'artdeco-carousel__item-container',
            'next_btn': 'div.org-people__insights-container button.artdeco-pagination__button--next',
        }

    }

    __alumni_data = []

    # active url
    __activeUrl = {
        "linkedin": __linkedinSelectors,
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
                # add a sleep
                sleep(3)

                usernameTag = self.find_element_by_id(
                    self.__selectors['sign_in']['username']['id'])

                if usernameTag is None:
                    return True
                else:
                    # redirect to the login page
                    self.__driver.get(self.__url)
            else:
                self.__driver.get(self.__url)
            return False
        except Exception as e:
            return False

    # find a school
    def find_school_alumni(self, school, jobTitle, startYear, endYear):
        try:
            # go to the alumni page
            self.__driver.get(
                f'https://www.linkedin.com/school/{school}/people/?educationEndYear={endYear}&educationStartYear={startYear}&keywords={jobTitle}')
            # check if the alumni page is loaded
            sleep(2)
            alumni_page = self.find_element_by_selector(
                self.__selectors['has_alumni_result']['selector'])

            if alumni_page is not None:
                show_more = self.find_element_by_selector(
                    self.__selectors['show_more']['selector'])
                #
                if show_more is not None:
                    show_more.click()
                    sleep(3)
                #
                # save the page source
                data = self.format_page_source(
                    school, jobTitle, startYear, endYear)
                if len(data) > 0:
                    self.__alumni_data.append(data)
                    print("Saving the data...")
                    # save alumni data to json replace file if it exists
                    with open('jobs/alumni.json', 'w') as fp:
                        json.dump(self.__alumni_data, fp)
                    print("Data saved successfully")
                else:
                    print("No alumni data found")
                return True
            print("No alumni data found")
            return False
        except Exception as e:
            print(e)
            return False

    # format the page source
    def format_page_source(self, school, jobTitle, startYear, endYear):
        # do everything here
        soup = BeautifulSoup(self.__driver.page_source, 'html.parser')
        data = {}
        data['school'] = school
        data['jobTitle'] = jobTitle
        data['startYear'] = startYear
        data['endYear'] = endYear
        data['cols'] = []

        all_cols = soup.find_all(class_=self.__selectors['bs4']['alumni_cols'])
        # print(all_cols)
        for i in range(len(all_cols)):
            column = {}
            c_data = all_cols[i].find_all(
                'button', class_='org-people-bar-graph-element')
            c = all_cols[i].find('h3')
            if (c is None):
                next_btn = self.find_element_by_selector(
                    self.__selectors['bs4']['next_btn'])
                while all_cols[i].find('h3') is None:
                    next_btn.click()
                    sleep(1.5)
                    soup = BeautifulSoup(
                        self.__driver.page_source, 'html.parser')
                    all_cols = soup.find_all(
                        class_=self.__selectors['bs4']['alumni_cols'])
                #
                c_data = all_cols[i].find_all(
                    'button', class_='org-people-bar-graph-element')
                c = all_cols[i].find('h3')
            #
            # print(c.get_text(strip=True))
            column[f'{c.get_text(strip=True)}'] = []
            # print('data for:', c.get_text(strip=True))
            # print(c_data)
            for elem in c_data:
                col_list = {}
                # print(elem)
                nb = elem.find('strong')
                # print(nb.get_text())
                value = elem.find(
                    'span', class_='org-people-bar-graph-element__category')
                # print(value)
                col_list['number'] = nb.get_text(strip=True)
                col_list['value'] = value.get_text(strip=True)
                column[f'{c.get_text(strip=True)}'].append(col_list)
                #
                data['cols'].append(column)
        return data
