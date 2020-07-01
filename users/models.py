from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

class CardClass(models.Model):
    name = models.CharField(max_length=64)
    cardClass = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name}"

class Status(models.Model):
    status = models.CharField(max_length=64)
    cardClass = models.ForeignKey('CardClass', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.status}"

class Tag(models.Model):
    tag = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.tag}"

class RequestStatus(models.Model):
    status = models.CharField(max_length=64)
    cardClass = models.ForeignKey('CardClass', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.status}"

#Will have to decide how to limit many to many
# Create your models here.
class Project(models.Model):
    name = models.CharField(max_length=64)
    manager = models.ForeignKey(User, on_delete=models.PROTECT, related_name='manager')
    status = models.ForeignKey('Status', on_delete=models.PROTECT,)
    contributors = models.ManyToManyField(User, related_name='contributor', blank=True,)
    description = models.TextField()
    tags = models.ManyToManyField(Tag, blank=True,)

    def __str__(self):
        return f"{self.name} by {self.manager}"

class Request(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='project')
    status = models.ForeignKey('RequestStatus', on_delete=models.PROTECT)
    note = models.TextField(max_length = 300)

    def __str__(self):
        return f"{self.sender}'s request for {self.project}: {self.status}"
