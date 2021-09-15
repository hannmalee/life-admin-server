from lifeadminapi.models.household_user import HouseholdUser
from lifeadminapi.models.category import Category
from django.db import models

class Task(models.Model): 
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    is_completed = models.BooleanField(default=False)
    created_on = models.DateField(default="0000-00-00")
    due_date = models.DateField(default="0000-00-00")
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    assigned_to = models.ForeignKey(HouseholdUser, on_delete=models.DO_NOTHING, related_name="assignedto")
    created_by = models.ForeignKey(HouseholdUser, on_delete=models.DO_NOTHING, related_name="createdby")