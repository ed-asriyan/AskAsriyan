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

    def get_comments(self):
        return Comment.objects.filter(comment_article_id=self.id)

    def get_url(self):
        return '/article{article_id}/'.format(article_id=self.id)


class Comment(models.Model):
    class Meta:
        db_table = "comment"

    comment_author = models.ForeignKey(User)
    comment_body = models.TextField()
    comment_date = models.DateField()
    comment_is_correct = models.BooleanField(default=False)
    comment_rating = models.IntegerField(default=0)
    comment_article = models.ForeignKey('Article')

    def get_url(self):
        return self.comment_article.get_url()
