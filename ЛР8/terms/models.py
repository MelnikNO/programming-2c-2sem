from django.db import models

# Create your models here.


class Tag(models.Model):
    # question = models.ForeignKey(Question, on_delete=models.CASCADE)
    tag_name = models.CharField(max_length=30)
    date_added = models.DateTimeField("date added")
    # choice_text = models.CharField(max_length=200)
    # votes = models.IntegerField(default=0)


class Termin(models.Model):
    termin_name = models.CharField(max_length=50)
    termin_description = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")
    tags = models.ManyToManyField(Tag)

