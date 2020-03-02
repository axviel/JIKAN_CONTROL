from django.db import models
from datetime import datetime

class Exam(models.Model):
  event_type_id = models.IntegerField()
  description = models.TextField()
  predicted_study_hours = models.IntegerField()
  predicted_weeks = models.IntegerField()
  predicted_score = models.IntegerField()
  final_study_hours = models.IntegerField()
  final_weeks = models.IntegerField()
  final_score = models.IntegerField()
  created_date = models.DateTimeField(default=datetime.now)
  user_id = models.IntegerField()
  is_hidden = models.BooleanField(default=False)

  def __str__(self):
    return self.description