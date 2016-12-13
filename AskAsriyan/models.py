from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum


class Profile(models.Model):
    profile_user = models.ForeignKey(User)


class Article(models.Model):
    class Meta():
        db_table = "article"

    article_title = models.CharField(max_length=200)
    article_body = models.TextField()
    article_date = models.DateTimeField()
    article_rating = models.IntegerField(default=0)
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
    comment_date = models.DateTimeField()
    comment_is_correct = models.BooleanField(default=False)
    comment_rating = models.IntegerField(default=0)
    comment_article = models.ForeignKey('Article')

    def get_url(self):
        return self.comment_article.get_url()


class ArticleLikeManager(models.Manager):
    def get_question_likes(self, question):
        return self.filter(question=question)

    def sum_for_question(self, question):
        return self.get_question_likes(question).aggregate(sum=Sum('value'))['sum']

    def add_or_update(self, author, question, value):
        obj, new = self.update_or_create(
            article_like_author=author,
            article_like_question=question,
            article_like_defaults={'value': value}
        )

        question.likes = self.sum_for_question(question)
        question.save()
        return new


class ArticleLike(models.Model):
    UP = 1
    DOWN = -1

    article_like_question = models.ForeignKey('Article')
    article_like_author = models.ForeignKey(User)
    article_like_value = models.SmallIntegerField(default=1)

    objects = ArticleLikeManager()
