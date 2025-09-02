from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

# create your models here.
class Note(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    slug = models.SlugField(max_length=200, blank=True)

    class Meta:
        unique_together = (('title', 'owner'), ('slug', 'owner'))

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Note, self).save(*args, **kwargs)

    def __str__(self):
        return self.title
    
    def name_snippet(self):
        return self.title if len(self.title) <= 10 else self.title[:7] + "..."
    
    def snippet(self):
        return self.content[:50] + "..." if len(self.content) > 50 else self.content
    
