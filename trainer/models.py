from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Profile(models.Model):
    # Main profile model which contains details of trainer
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    country = models.CharField(max_length=100, null=True)
    photo = models.FileField(null=True, default="default_user.png", blank=True)
    rating = models.FloatField(null=True, blank=True)
    phone = models.CharField(max_length=20, null=True)
    availability = models.CharField(max_length=20, null=True, blank=True)
    website = models.CharField(max_length=200, null=True, blank=True)
    address = models.CharField(max_length=500, null=True, blank=True)
    birth_date = models.DateField(null=True)
    gender = models.CharField(max_length=10, null=True)

#    def get_absolute_url(self):
#        return reverse('trainer:detail', kwargs={'pk': self.pk})

    # For Profile.objects.all() call it will return first name and last name
    def __str__(self):
        return self.user.first_name + " " + self.user.last_name


class Skill(models.Model):
    # Skill model which contains trainer's skill details
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    hours = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class Availability(models.Model):
    # Skill model which contains trainer's skill details
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    locations = models.CharField(max_length=2000)
    hours_per_week = models.IntegerField(default=0)

    def __str__(self):
        return self.locations + "|" + str(self.hours_per_week)


class Timeline(models.Model):
    # Timeline model which contains trainer's training history
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    organization = models.CharField(max_length=200, blank=False)
    technology = models.CharField(max_length=500, blank=False)
    from_date = models.DateField(blank=False)
    hours = models.CharField(max_length=10, blank=False)
    trainee_cnt = models.CharField(max_length=10, blank=False)

    def __str__(self):
        return self.organization                    

class Experience(models.Model):
    # Experience model which contains trainer's past work experience
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    organization = models.CharField(max_length=200)
    from_month = models.CharField(max_length=3)
    from_year = models.IntegerField()
    to_month = models.CharField(max_length=3)
    to_year = models.IntegerField()
    desc = models.CharField(max_length=2000)

    def __str__(self):
        return self.organization


class Message(models.Model):
    # Message model which contains messages sent to trainer by requester
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    message = models.CharField(max_length=1000)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    read = models.BooleanField()
    dttime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.phone + " " + str(self.email)
