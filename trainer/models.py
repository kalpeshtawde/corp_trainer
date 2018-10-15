from django.db import models
from django.urls import reverse


class Profile(models.Model):
    # Main profile model which contains details of trainer
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    password = models.CharField(max_length=20)
    country = models.CharField(max_length=100, null=True)
    photo = models.FileField(null=True, default="default_user.png")
    rating = models.FloatField(null=True)
    email = models.CharField(max_length=200)
    phone = models.CharField(max_length=20, null=True)
    availability = models.CharField(max_length=20, null=True)
    website = models.CharField(max_length=200, null=True)
    address = models.CharField(max_length=500, null=True)
    birth_date = models.DateField(null=True)
    gender = models.CharField(max_length=10, null=True)

#    def get_absolute_url(self):
#        return reverse('trainer:detail', kwargs={'pk': self.pk})

    # For Profile.objects.all() call it will return first name and last name
    def __str__(self):
        return self.first_name + ' ' + self.last_name


class Skill(models.Model):
    # Skill model which contains trainer's skill details
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    hours = models.IntegerField()

    def __str__(self):
        return self.title


class Timeline(models.Model):
    # Timeline model which contains trainer's training history
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    organization = models.CharField(max_length=200)
    technology = models.CharField(max_length=500)
    from_date = models.DateField()
    to_date = models.DateField()
    hours = models.IntegerField()
    trainee_cnt = models.IntegerField()

    def __str__(self):
        return self.organization

class Experience(models.Model):
    # Experience model which contains trainer's past work experience
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    organization = models.CharField(max_length=200)
    from_date = models.DateField()
    to_date = models.DateField()
    desc = models.CharField(max_length=2000)

    def __str__(self):
        return self.organization




