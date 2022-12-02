from applications.models import Application
from applications.utils import generate_roll_no
from django.core.management.base import BaseCommand

from call_applications.models import CallForApplication


class Command(BaseCommand):
    help = 'Loads Applicants information from google sheet'

    def handle(self, *args, **options):

        open_applications = CallForApplication.objects.all()
        
        options = {i: open_applications[i].title for i in range(len(open_applications))}
        print(options)
        choice = input("Select season to Regenerate Roll No. only integer number: ")
        try:
            open_application = open_applications[int(choice)]
        except:
            print("Something went wrong")
            return
        
        applications = Application.objects.filter(call_for_application=open_application).order_by('roll_no')
        latest_roll = '0'
        for application in applications:
            roll = generate_roll_no(open_application, latest_roll)
            application.roll_no = roll
            application.save()
            
            latest_roll = roll
        

