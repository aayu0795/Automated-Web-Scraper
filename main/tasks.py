from celery import shared_task, task
from .scrapper import scrape


@task
def scrape_dev_to():
    url = "https://dev.to/search?q=django"
    scrape(url)
    return
