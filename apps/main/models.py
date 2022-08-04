from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_delete
from django.utils import timezone


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


class Analytic(models.Model):

    post = models.ForeignKey('Post', models.CASCADE, verbose_name='Post')
    date = models.DateField('Date')
    likes_count = models.PositiveIntegerField('Likes count', default=0)


@receiver(post_save, sender=Post)
def create_analytic(sender, created, instance, **kwargs):
    if created:
        Analytic.objects.create(post=instance, date=timezone.now())


@receiver(post_save, sender=Like)
def increment_likes_count(sender, created, instance, **kwargs):
    if created:
        analytic, created = Analytic.objects.get_or_create(post=instance.post, date=timezone.now())
        analytic.likes_count += 1
        analytic.save()


@receiver(pre_delete, sender=Like)
def decrement_likes_count(instance, **kwargs):
    analytic, created = Analytic.objects.get_or_create(post=instance.post, date=timezone.now())
    if not created:
        analytic.likes_count -= 1
    analytic.save()
