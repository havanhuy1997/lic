from django.db import models
from django.contrib.auth.models import User

class SearchBox(models.Model):
    search = models.CharField(max_length=100)

class reviewData(models.Model):
    rating = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    reviews = models.TextField()

    def __str__(self):
        return self.name

class LoginData(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    dob = models.CharField(max_length=100)

    def __str__(self):
        return self.username

class OtpData(models.Model):
    username = models.CharField(max_length=100)
    otp = models.CharField(max_length=100)

    def __str__(self):
        return self.otp
