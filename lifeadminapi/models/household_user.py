from django.db import models
from django.contrib.auth.models import User
from lifeadminapi.models.household import Household

class HouseholdUser(models.Model): 
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING)
    household = models.ForeignKey(Household, on_delete=models.DO_NOTHING)