from celery import shared_task, task
import time


@shared_task
def send_mass_emails(recipient):
    """
    Shared task allow you to call this function asynchronously
    """
    print("sleeping")
    print(recipient)
    time.sleep(5)
    print("waking up")
    return


@task
def send_schedule_emails():
    """
    task alow you to run a task based on schedule
    """
    # Our bussiness logic
    pass
    # inorder to run the task we have to make some setting.py changes
