from django.db import models

class Order(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    adress = models.TextField()
    total_sum = models.PositiveSmallIntegerField()
