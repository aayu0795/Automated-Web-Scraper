import datetime
from dateutil.relativedelta import relativedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from django.utils import timezone

from .models import NewsItem, ScrapeRecord


def scrape(url):
    # setting up selenium
    options = webdriver.ChromeOptions()
    options.add_argument(" - incognito")    # changing mode to incognito

    browser = webdriver.Chrome(
        executable_path='./chromedriver', chrome_options=options)

    browser.get(url)    # same as request.get

    timeout = 10    # request timeout after  10 sec

    try:
        # wait till the content of the div is loaded completely
        WebDriverWait(browser, timeout).until(
            EC.visibility_of_element_located(
                (By.XPATH,
                 "//div[@class='single-article single-article-small-pic']")
            )
        )
    except TimeoutException:
        print("Time out waiting for page to load")
        raise TimeoutException
        browser.quit()

    # find all the element with this class --> single-article single-article-small-pic
    article_elements = browser.find_elements_by_xpath(
        "//div[@class='single-article single-article-small-pic']"
    )

    try:    # if we get any errors

        record = ScrapeRecord.objects.create(   # scrape start time
            finish_time=timezone.now()
        )

        for article in article_elements:

            # check if div not a user
            if (article.find_element_by_xpath(".//button")).text != "+ FOLLOW":

                # try get the anchor tag and href
                result = article.find_element_by_xpath(
                    ".//a[@class='small-pic-link-wrapper index-article-link']"
                )

                news_item_link = result.get_attribute('href')
                news_item_title = result.text   # try get title …

                #  or we can do same things by
                # title_result = article.find_element_by_tag_name('h3')

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
                        title=news_item_title,
                        link=news_item_link,
                        publish_date=new_item_date
                    )

        record.finish_time = timezone.now()  # scrape end time
        record.finished = True
        record.save()

    except Exception as e:
        # send ourself an email regarding the error
        raise e
        pass
