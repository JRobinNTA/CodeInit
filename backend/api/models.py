from django.db import models
from django.contrib.auth.models import User

class Skill(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class UserPortfolio(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=150, blank=True)
    year = models.CharField(max_length=10)
    branch = models.CharField(max_length=100)
    skills = models.ManyToManyField(Skill)

    def save(self, *args, **kwargs):  # Add this method
        self.username = self.user.username
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user}'s Portfolio"
