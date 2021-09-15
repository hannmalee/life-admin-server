from lifeadminapi.models.household_user import HouseholdUser
from django.db import models

class Category(models.Model): 
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    creator = models.ForeignKey(HouseholdUser, on_delete=models.DO_NOTHING)