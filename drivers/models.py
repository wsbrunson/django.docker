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

    def __str__(self) -> str:
        return self.given_name + ' ' + self.family_name
    
     
    