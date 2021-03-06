from django.db import models
from datetime import datetime

class Course(models.Model):
  title = models.CharField(max_length=200)
  description = models.TextField()
  created_date = models.DateTimeField(default=datetime.now)
  user_id = models.IntegerField()
  is_hidden = models.BooleanField(default=False)

  def __str__(self):
    return self.title