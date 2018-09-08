from django.db import models


class Profile(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    photo = models.CharField(max_length=1000)

    # For Profile.objects.all() call it will return first name and last name
    def __str__(self):
        return self.first_name + ' ' + self.last_name + ' (' + self.country + ')'


class Skill(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    skill_title = models.CharField(max_length=100)
    hours = models.IntegerField()

    def __str__(self):
        return self.skill_title + ' ' + self.hours
