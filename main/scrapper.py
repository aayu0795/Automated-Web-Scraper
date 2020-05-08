from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


def scrape(url):
    # setting up selenium
    options = webdriver.ChromeOptions()
    options.add_argument(" - incognito")    # changing mode to incognito

    browser = webdriver.Chrome(
        executable_path='./chromedriver', chrome_options=options)

    browser.get(url)    # same as request.get

    timeout = 10    # request timeout after  10 sec

    try:
        WebDriverWait(browser, timeout).until(
            EC.visibility_of_element_located(
                (By.XPATH,
                 "//div[@class='single-article single-article-small-pic']")
            )
        )
    except TimeoutException:
        print("Time out waiting for page to load")
        browser.quit()

    # find all the element with this class --> single-article single-article-small-pic
    article_elements = browser.find_elements_by_xpath(
        "//div[@class='single-article single-article-small-pic']"
    )

    for article in article_elements:

        # check if div not a user
        if (article.find_element_by_xpath(".//button")).text != "+ FOLLOW":

            # try get the anchor tag and href
            result = article.find_element_by_xpath(
                ".//a[@class='small-pic-link-wrapper index-article-link']"
            )

            news_item_link = result.get_attribute('href')
            news_item_title = result.text   # try get title

            #  or we can do same things by title_result = article.find_element_by_tag_name('h3')

            # try get timestamp
            timestamp_result = article.find_element_by_tag_name('time')
            news_item_timestamp = timestamp_result.text
            print(news_item_timestamp)
