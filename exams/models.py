from django.db import models
from datetime import datetime

from events.models import Event
from courses.models import Course

class Exam(models.Model):
  event = models.ForeignKey(Event, on_delete=models.DO_NOTHING)
  course = models.ForeignKey(Course, on_delete=models.DO_NOTHING)
  title = models.CharField(max_length=200)
  description = models.TextField()
  predicted_study_hours = models.IntegerField()
  predicted_weeks = models.IntegerField()
  predicted_score = models.IntegerField()
  final_study_hours = models.IntegerField()
  final_weeks = models.IntegerField()
  final_score = models.IntegerField()
  created_date = models.DateTimeField(default=datetime.now)
  user_id = models.IntegerField()
  exam_number = models.IntegerField(default=0)
  is_hidden = models.BooleanField(default=False)

  def __str__(self):
    return self.title