from django.db import models


class Driver(models.Model):
    id = models.CharField(max_length=200, primary_key=True)
    position = models.CharField(max_length=10)
    points = models.CharField(max_length=10)
    wins = models.CharField(max_length=10)
    code = models.CharField(max_length=10)
    given_name = models.CharField(max_length=200)
    family_name = models.CharField(max_length=200)
    driver_number = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    twitter_username = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.given_name + " " + self.family_name


class DriverTwitterMetrics(models.Model):
    driver_id = models.ForeignKey("Driver", on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    followers_count = models.BigIntegerField()
    following_count = models.BigIntegerField()
    listed_count = models.BigIntegerField()
    tweet_count = models.BigIntegerField()
