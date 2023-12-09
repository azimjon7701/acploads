from django.core.management import BaseCommand

from account.models import Profile


class Command(BaseCommand):

    def handle(self, *args, **options):
        print("Generating customer ids...")
        profiles = Profile.objects.all()
        for profile in profiles:
            profile.generate_customer_id()
        print("Customer ids generated")

