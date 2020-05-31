from .models import NewsItem, ScrapeRecord

import datetime
from dateutil.relativedelta import relativedelta

from django.utils import timezone

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def scrape(url):
    # setting up selenium
    options = webdriver.ChromeOptions()

    # changing mode to incognito
    options.add_argument(" - incognito")

    # giving path of the chrome driver
    browser = webdriver.Chrome(
        executable_path='./chromedriver', chrome_options=options)

    # same as request.get
    browser.get(url)

    # request timeout after  10 sec
    timeout = 10

    try:
        # wait till the content of the article is loaded completely
        WebDriverWait(browser, timeout).until(
            EC.visibility_of_element_located(
                (By.XPATH,
                 "//article[@class='crayons-story']")
            )
        )
    except TimeoutException:
        print("Time out waiting for page to load")
        raise TimeoutException
        browser.quit()

    # find all the element with this class --> crayons-story
    article_elements = browser.find_elements_by_xpath(
        "//article[@class='crayons-story']"
    )

    try:    # just to check if we get any errors

        # record scrape start time
        record = ScrapeRecord.objects.create(
            finish_time=timezone.now()
        )

        for article in article_elements:

            # check if div not a user
            if (article.find_element_by_xpath(".//button")).text != "+ FOLLOW":

                # try get the h2 tag
                result = article.find_element_by_xpath(
                    ".//h2[@class='crayons-story__title']"
                )

                # try get title
                news_item_link = result.find_element_by_xpath(
                    ".//a").get_attribute('href')
                news_item_title = result.text

                # try get body
                body_pr = article.find_element_by_xpath(
                    ".//div[@class='crayons-story__snippet mb-1']").text

                two_years_ago = datetime.date.today() - relativedelta(years=2)

                # try get timestamp
                timestamp_result = article.find_element_by_tag_name('time')
                news_item_time = timestamp_result.text

                # convert the news_item_time into python date object
                if "'" in news_item_time:
                    # parse the year
                    new_item_date = datetime.datetime.strptime(
                        news_item_time, "%b %d '%y").date()

                else:
                    # this year is the current year
                    new_item_date = datetime.datetime.strptime(
                        news_item_time, "%b %d")
                    today = datetime.date.today()
                    new_item_date = new_item_date.replace(
                        year=today.year).date()

                # Save posts which are posted in last 2 years from now
                if new_item_date > two_years_ago:
                    NewsItem.objects.get_or_create(
                        source='Dev.to',
                        title=news_item_title + body_pr,
                        link=news_item_link,
                        publish_date=new_item_date
                    )

        # scrape end time
        record.finish_time = timezone.now()
        record.finished = True
        record.save()
        browser.quit()

    except Exception as e:
        # send ourself an email regarding the error
        raise e
        print(e)
