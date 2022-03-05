from django.contrib import admin

# Register your models here.
from payment.models import ExtraFieldType, ExtraField, PaymentType, Payment


@admin.register(ExtraFieldType)
class ExtraFieldTypeAdmin(admin.ModelAdmin):
    ...


@admin.register(ExtraField)
class ExtraFieldAdmin(admin.ModelAdmin):
    ...


@admin.register(PaymentType)
class PaymentTypeAdmin(admin.ModelAdmin):
    ...

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    ...