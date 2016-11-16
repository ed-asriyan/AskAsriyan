from django.contrib.auth.models import User
from django.db import models


class Article(models.Model):
    class Meta():
        db_table = "article"

    article_title = models.CharField(max_length=200)
    article_body = models.TextField()
    article_date = models.DateTimeField()
    article_rating = models.IntegerField()
    article_author = models.ForeignKey(User)

    def get_url(self):
        return '/article{article_id}'.format(article_id=self.id)
