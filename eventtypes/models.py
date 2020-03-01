from django.db import models

class EventType(models.Model):
  title = models.CharField(max_length=200)
  description = models.TextField(null=True)
  is_hidden = models.BooleanField()

  def __str__(self):
    return self.title