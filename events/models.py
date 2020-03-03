from django.db import models
from datetime import datetime

from eventtypes.models import EventType
from repeattypes.models import RepeatType

class Event(models.Model):
  event_type = models.ForeignKey(EventType, on_delete=models.DO_NOTHING)
  repeat_type = models.ForeignKey(RepeatType, on_delete=models.DO_NOTHING)
  title = models.CharField(max_length=200)
  description = models.TextField(blank=True, null=True)
  start_time = models.TimeField()
  end_time = models.TimeField()
  start_date = models.DateTimeField(default=datetime.now, blank=True)
  end_date = models.DateTimeField(null=True)
  user_id = models.IntegerField()
  # user_id = models.ForeignKey()
  is_hidden = models.BooleanField(default=False)

  def __str__(self):
    # Main field that's display in admin page
    return self.title