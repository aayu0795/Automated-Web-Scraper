from django.shortcuts import render
from .tasks import send_mass_emails


def mass_email_view(request):
    recipient = "aayush@gamil.com"
    print("in views.py")
    send_mass_emails.delay(recipient)
    return render(request, "index.html")
