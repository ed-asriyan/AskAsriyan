from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password # hashing
from AskAsriyan.models import Profile
from faker import Factory


class Command(BaseCommand):
    help = 'Fill users'

    def add_arguments(self, parser):
        parser.add_argument('--number',
                            action='store',
                            dest='number',
                            default=10,
                            help='Number of users to add'
                            )

    def handle(self, *args, **options):
        fake_factory = Factory.create('en_US')  # Initializes fake factory
        number = int(options['number'])  # Number of users to generate

        for i in range(number):
            # Returns dictionary with fake data
            profile = fake_factory.simple_profile()

            user = User.objects.create_user(profile['username'], profile['mail'], make_password('qwerty'))
            user.first_name = fake_factory.first_name()
            user.last_name = fake_factory.last_name()
            user.is_active = True
            user.is_superuser = False
            user.save()

            user_profile = Profile()
            user_profile.profile_user = user
            user_profile.save()

            self.stdout.write('[%d] added user %s' % (user.id, user.username))
