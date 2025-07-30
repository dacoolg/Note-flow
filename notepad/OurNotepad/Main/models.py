from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

# create your models here.
class Note(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True)


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Note, self).save(*args, **kwargs)

    def __str__(self):
        return self.title
    
    def snippet(self):
        return self.content[:50] + "..." if len(self.content) > 50 else self.content