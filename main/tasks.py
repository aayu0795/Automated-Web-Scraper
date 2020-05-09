from celery import shared_task, task
from .scrapper import scrape

url = "https://dev.to/search?q=django"


@task
def scrape_dev_to():
    scrape(url)
    return


@shared_task
def scrape_async():
    scrape(url)
    return
