from django.contrib import admin

from core.models import EmployeeRole, EStaffProfile, EStaffDocument, ELeave, EOverTime, EFreeDay


@admin.register(EmployeeRole)
class EmployeeRoleAdmin(admin.ModelAdmin):
    ...


@admin.register(EStaffProfile)
class EStaffProfileAdmin(admin.ModelAdmin):
    ...


@admin.register(EStaffDocument)
class EStaffDocumentAdmin(admin.ModelAdmin):
    ...


@admin.register(ELeave)
class ELeaveAdmin(admin.ModelAdmin):
    ...


@admin.register(EOverTime)
class EOverTimeAdmin(admin.ModelAdmin):
    ...


@admin.register(EFreeDay)
class EFreeDayAdmin(admin.ModelAdmin):
    ...
