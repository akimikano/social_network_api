from django.db import models


class Post(models.Model):

    user = models.ForeignKey('users.User', models.CASCADE, verbose_name='User', related_name='published_posts')
    title = models.CharField('Title', max_length=255)
    body = models.TextField('Body')
    created_at = models.DateTimeField('Created at', auto_now_add=True)
    is_archived = models.BooleanField('Archived', default=False)

    def __str__(self):
        return self.title


class Like(models.Model):

    user = models.ForeignKey('users.User', models.CASCADE, verbose_name='User')
    post = models.ForeignKey('Post', models.CASCADE, verbose_name='Post')
    created_at = models.DateTimeField('Created at', auto_now_add=True)
