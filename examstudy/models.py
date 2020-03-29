from django.db import models
from datetime import datetime

from events.models import Event
from exams.models import Exam

class ExamStudy(models.Model):
  event = models.ForeignKey(Event, on_delete=models.CASCADE)
  exam = models.ForeignKey(Exam, on_delete=models.DO_NOTHING)
  created_date = models.DateTimeField(default=datetime.now)
  is_hidden = models.BooleanField()

  def __str__(self):
    return self.title