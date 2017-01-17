from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from AskAsriyan.models import Article
from random import choice, randint
from faker import Factory


class Command(BaseCommand):
    help = 'Fill questions'

    def add_arguments(self, parser):
        parser.add_argument('--number',
                            action='store',
                            dest='number',
                            default=7,
                            help='Number of questions to add'
                            )

    def handle(self, *args, **options):
        fake_factory = Factory.create('en_US')
        number = int(options['number'])
        users = User.objects.all()[1:] # except admin

        for i in range(number):
            article = Article()

            article.article_title = fake_factory.sentence(nb_words=randint(2, 4), variable_nb_words=True)
            article.article_body = fake_factory.text(max_nb_chars=500)
            article.article_author = choice(users)
            article.article_date = fake_factory.date()
            article.save()
            self.stdout.write('added question [%d]' % (article.id))

