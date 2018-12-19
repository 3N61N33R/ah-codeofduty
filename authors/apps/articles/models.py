"""articles/models.py"""
from django.db import models

from django.db.models.signals import post_save
from notifications.signals import notify

from django.contrib.postgres.fields import ArrayField
from authors.apps.authentication.models import User
from django.utils.text import slugify

from authors.apps.authentication.models import User
from authors.apps.profiles.models import Profile

from rest_framework.reverse import reverse as api_reverse
from authors.apps.core.models import TimeStamp


class Article(models.Model):
    """Model representing articles"""
    title = models.CharField(db_index=True, max_length=255)
    body = models.TextField()
    images = ArrayField(models.TextField(), default=None,
                        blank=True, null=True)
    description = models.CharField(max_length=255)
    slug = models.SlugField(max_length=1000, unique=True)
    tags = models.ManyToManyField('articles.Tag', related_name='articles')
    time_to_read = models.IntegerField()
    # auto_now_add automatically sets the field to now when the object is first created.
    time_created = models.DateTimeField(auto_now_add=True, db_index=True)
    # auto_now will update every time you save the model.
    time_updated = models.DateTimeField(auto_now=True, db_index=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="articles")
    average_rating = models.IntegerField(default=0)

    likes = models.ManyToManyField(
        User, blank=True, related_name='LikesDislikes.user+')
    dislikes = models.ManyToManyField(
        User, blank=True, related_name='LikesDislikes.user+')

    class Meta():
        """Meta class defining order"""
        ordering = ('time_created', 'time_updated',)

    def save(self, *args, **kwargs):
        """override save from super"""
        super(Article, self).save(*args, **kwargs)

    def __str__(self):
        """return string representation of object"""
        return self.title
    # ...............................................................

    def api_url(self, request=None):
        return api_reverse('articles:articles_detail', kwargs={'slug': self.slug}, request=request)
    # ...............................................................


class Comment(models.Model):
    """
    This class implement a database table.
    This table has  seven fields one is automatically generated by django
    The relationship between articles and comments is one to many
    The relationship between comment and reply is one to many.
    the relationship between Author and comments is one to many
    """
    parent = models.ForeignKey(
        'self', null=True, blank=False, on_delete=models.CASCADE, related_name='thread')
    article = models.ForeignKey(
        Article, blank=True, null=True, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(
        User, blank=True, null=True, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(
        User, related_name='comment_likes', blank=True)

    def __str__(self):
        return self.body


class CommentHistory(models.Model):
    """
     implements comment edit history table
    """
    comment = models.TextField()
    parent_comment = models.ForeignKey(Comment,
                                       on_delete=models.CASCADE,
                                       db_column='parent_comment')
    date_created = models.DateTimeField(auto_now=True)


class Highlight(models.Model):
    """
    Table representing highlights and comments made on articles
    """
    article = models.ForeignKey(Article, on_delete=models.CASCADE,
                                related_name="highlights")
    highlighter = models.ForeignKey(User, on_delete=models.CASCADE,
                                    related_name="highlights")
    index_start = models.IntegerField(default=0)
    index_stop = models.IntegerField()
    highlighted_article_piece = models.CharField(blank=True, max_length=200)
    comment = models.CharField(blank=True, max_length=200)
    time_created = models.DateTimeField(auto_now_add=True, db_index=True)
    time_updated = models.DateTimeField(auto_now=True, db_index=True)

    class Meta():
        '''Meta class defining order'''
        ordering = ('time_updated',)

    def __str__(self):
        return self.comment


class Report(models.Model):
    """Reporting an article model"""
    body = models.TextField()
    reporter = models.ForeignKey(
        'authentication.User', on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.body


def article_handler(sender, instance, created, **kwargs):
    """
    Notifications handler to notify all the followers
    of an author that he has published a new article
     :params: sender: the actor (author) who is doing the action of
       posting an article
    :params: instance: the author instance
    :params: created: timestamp when the action happened
    """
    try:
        author = instance.author
        # get all users following the user
        my_followers = author.profile.get_my_followers()
        # notify each follower that the user has published an article
        for followers in my_followers:
            followers = User.objects.filter(username=followers)
            notify.send(
                instance,
                recipient=followers,
                verb='{} published a new article'.format(author.username))
    except Exception:
        "author not found"


def favorite_comment_handler(sender, instance, created, **kwargs):
    """
    Comment handler to notify the favouriters of a certain article
    that it has received a comment
    :params: sender: the actor (commenter) who is doing the action of
       posting commenting on my article
    :params: instance: the comment
    :params: created: timestamp when the action happened
    """
    try:
        # initialize the author of the comment
        author = instance.author
        # initialize the author of the article
        article_author = [instance.article.author]
        article_slug = instance.article.slug
        articles_instance = Article.objects.get(slug=article_slug)
        favouriters = articles_instance.favorited_by.values()
        for user_id in articles_instance.favorited_by.values():
            favouriters_name = User.objects.get(id=user_id['user_id'])
            # notify each favouriter of an article
            notify.send(
                instance,
                recipient=favouriters_name,
                verb='{} commented on an article you have favorited'.format(author.username))
    except:
        "article not found"


post_save.connect(article_handler, sender=Article)
post_save.connect(favorite_comment_handler, sender=Comment)


class LikesDislikes(models.Model):
    article = models.ForeignKey(
        Article, related_name='like', on_delete=models.CASCADE)
    reader = models.ForeignKey(
        User, related_name='like', on_delete=models.CASCADE)
    likes = models.BooleanField()

    class Meta:
        unique_together = ('article', 'reader')


class Tag(TimeStamp):
    tag = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.tag
