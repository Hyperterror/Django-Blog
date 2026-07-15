from django.db import models as mod
from django.utils import timezone
import datetime
from django.contrib import admin

# Create your models here.

class Question(mod.Model):
  question_text=mod.CharField(max_length=200)
  pub_date=mod.DateField("Date Published")
  def __str__(self):
    return self.question_text
  @admin.display(
      boolean=True,
      ordering="pub_date",
      description="Published recently?"
  )


  def was_published_recently(self):
    return timezone.now().date() - datetime.timedelta(days=1) <= self.pub_date <= timezone.now().date()

class Choice(mod.Model):
  question=mod.ForeignKey(Question,on_delete=mod.CASCADE)
  choice_text=mod.CharField(max_length=200)
  votes=mod.IntegerField(default=0)
  def __str__(self):
    return self.choice_text