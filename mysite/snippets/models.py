from django.db import models
import datetime

# class Poll(models.Model):
#     question = models.CharField(max_length=200)
#     pub_date = models.DateTimeField('date published')
#     def __unicode__(self):
#         return self.question 
#     def was_published_today(self):
#         return self.pub_date.date() == datetime.date.today()
#     was_published_today.short_description = 'Published today?'

# class Choice(models.Model):
#     poll = models.ForeignKey(Poll)
#     choice = models.CharField(max_length=200)
#     votes = models.IntegerField()
#     def __unicode__(self):
#         return self.choice

class Snippet(models.Model):
    def __unicode__(self):
        return self.title 

    MEDIA_TYPES = (
        ('0', 'Image'),
        ('1', 'Gif'),
        ('2', 'Youtube'),
    )

    title = models.CharField(max_length=100, blank=True)
    url = models.CharField(max_length=100, blank=True)
    text = models.TextField(max_length=1000, blank=True)
    media = models.CharField(max_length=100, blank=True)
    mediaType = models.CharField(max_length=1, choices=MEDIA_TYPES)
    date_added = models.DateTimeField('date added')
    last_viewed = models.DateTimeField('last viewed')
    width = models.CharField(max_length=2, blank=True)
    height = models.DecimalField(max_digits=5, decimal_places=0, blank=True)

class Keyword(models.Model):
    keyword = models.CharField(max_length=100)

class SnippetKeywordLink(models.Model):
    snippet = models.ForeignKey(Snippet)
    keyword = models.ForeignKey(Keyword)