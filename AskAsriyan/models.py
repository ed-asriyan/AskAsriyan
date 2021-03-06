from random import choice

from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum, Count


class Profile(models.Model):
    class Meta:
        db_table = "profile"

    profile_user = models.ForeignKey(User)
    profile_avatar = models.ImageField()


class ArticleManager(models.Manager):
    def get_by_tag(self, tag):
        if tag is None:
            return []

        return Article.objects.all().filter(article_tags__tag_title=tag)

    def get_newest(self):
        return self.all().order_by('-article_date')

    def get_popular(self):
        return self.all().order_by('-article_rating')


class Article(models.Model):
    class Meta:
        db_table = "article"

    article_title = models.CharField(max_length=200)
    article_body = models.TextField()
    article_date = models.DateTimeField()
    article_rating = models.IntegerField(default=0)
    article_author = models.ForeignKey(User)
    article_tags = models.ManyToManyField('Tag')

    objects = ArticleManager()

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
    def get_question_likes(self, article):
        return self.filter(question=article)

    def sum_for_question(self, article):
        return self.get_question_likes(article).aggregate(sum=Sum('value'))['sum']

    def add_or_update(self, author, article, value):
        obj, new = self.update_or_create(
            article_like_author=author,
            article_like_question=article,
            defaults={'value': value}
        )

        article.likes = self.sum_for_question(article)
        article.save()
        return new


class ArticleLike(models.Model):
    UP = 1
    DOWN = -1

    article_like_question = models.ForeignKey('Article')
    article_like_author = models.ForeignKey(User)
    article_like_value = models.SmallIntegerField(default=1)

    objects = ArticleLikeManager()


class AnswerLikeManager(models.Manager):
    def has_answer(self, comment):
        return self.filter(answer=comment)

    def sum_for_answer(self, comment):
        return self.has_answer(comment).aggregate(sum=Sum('value'))['sum']

    def add_or_update(self, author, comment, value):
        obj, new = self.update_or_create(
            comment_like_author=author,
            comment_like_answer=comment,
            defaults={'value': value}
        )

        comment.likes = self.sum_for_answer(comment)
        comment.save()
        return new


class AnswerLike(models.Model):
    UP = 1
    DOWN = -1

    comment_like_answer = models.ForeignKey('Comment')
    comment_like_author = models.ForeignKey(User)
    comment_like_value = models.SmallIntegerField(default=1)

    objects = AnswerLikeManager()


class TagManager(models.Manager):
    def with_articles_count(self):
        return self.annotate(article_count=Count('article'))

    def order_by_article_count(self):
        return self.with_articles_count().order_by('-article_count')

    def get_by_title(self, title):
        return self.get(tag_title=title)

    def get_or_create(self, title):
        try:
            tag = self.get_by_title(title)
        except Tag.DoesNotExist:
            tag = self.create(tag_title=title, tag_color=choice(Tag.COLORS)[0])
        return tag

    def get_popular(self):
        return self.order_by_article_count().all()[:20]


class Tag(models.Model):
    COLORS = (
        ('Y', 'yellow'),
        ('O', 'orange'),
        ('R', 'red'),
        ('G', 'green'),
        ('B', 'blue'),
    )

    tag_title = models.CharField(max_length=30)
    tag_color = models.CharField(max_length=2, choices=COLORS, default='B')

    objects = TagManager()

    def get_articles_count(self):
        return len(self.get_articles())

    def get_articles(self):
        return Article.objects.all().filter(article_tags__tag_title=self.tag_title)

    def get_url(self):
        return '/articles?tag=' + self.tag_title + '&page=1'
