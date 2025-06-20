from django.db import models

# Create your models here.

class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"(PK: {self.pk}) {self.name}"

class Project(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return f"(PK: {self.pk}) {self.name}"

class CV(models.Model):
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    bio = models.TextField()
    contacts = models.JSONField(default=dict)
    skills = models.ManyToManyField(Skill, related_name='cvs')
    projects = models.ManyToManyField(Project, related_name='cvs')

    def __str__(self):
        return f"(PK: {self.pk}) {self.firstname} {self.lastname}"
    
class RequestLog(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    method = models.CharField(max_length=10)
    path = models.CharField(max_length=255)
    ip_address = models.GenericIPAddressField()

    def __str__(self):
        return f"(PK: {self.pk}) {self.timestamp} - {self.method} {self.path}"