from django.db import models

# Create your models here.
from small_small_hr import models as hr_models


class EmployeeRole(hr_models.Role):
    ...


class EStaffProfile(hr_models.StaffProfile):
    ...


class EStaffDocument(hr_models.StaffDocument):
    ...


class ELeave(hr_models.Leave):
    ...


class EOverTime(hr_models.OverTime):
    ...


class EAnnualLeave(hr_models.AnnualLeave):
    ...


class EFreeDay(hr_models.FreeDay):
    ...

