from django.db import models
from datetime import datetime

class Event(models.Model):
  event_type_id = models.IntegerField()
  repeat_type_id = models.IntegerField()
  title = models.CharField(max_length=200)
  description = models.TextField(null=True)
  start_time = models.TimeField()
  end_time = models.TimeField()
  start_date = models.DateTimeField(default=datetime.now)
  end_date = models.DateTimeField(null=True)
  user_id = models.IntegerField()
  is_hidden = models.BooleanField(default=False)

  def __str__(self):
    return self.title