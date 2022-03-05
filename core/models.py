from django.db import models

# Create your models here.
from small_small_hr import models as hr_models


class EmployeeRole(hr_models.Role):
    ...


class EStaffProfile(hr_models.StaffProfile):
    ...
