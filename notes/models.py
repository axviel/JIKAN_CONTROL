from django.db import models
from datetime import datetime

from events.models import Event

class Note(models.Model):
  events = models.ForeignKey(Event, on_delete=models.DO_NOTHING)
  title = models.CharField(max_length=200)
  description = models.TextField()
  created_date = models.DateTimeField(default=datetime.now, blank=True)
  user_id = models.IntegerField()
  is_hidden = models.BooleanField(default=False)

  def __str__(self):
    return self.title
