from django.db import models
from django.contrib.auth.models import User
# the post is going to be associated with a user
# so we're going to use user model
from django.utils import timezone


# tbales in a database
class Category (models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Post (models.Model):

    class PostObjects(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(status='published')
        # only return 'published' post

    options = (
        ('draft', 'Draft'),
        ('published', 'Published')
    )
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, default=1)
    title = models.CharField(max_length=250)
    description = models.TextField()

    blogImg = models.ImageField(
        upload_to='images/', default='')
    slug = models.SlugField(max_length=250, unique_for_date='published')
    published = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='blog_posts'
    )
    status = models.CharField(
        max_length=10, choices=options, default='published'
    )

    objects = models.Manager()  # default model manager
    postobjects = PostObjects()  # custom model manager

    class Meta:
        ordering = ('-published',)

    def __str__(self):
        return self.title
