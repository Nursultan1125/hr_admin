from django.db import models

# Create your models here.
from django.utils.timezone import localtime, now
from django.utils.translation import ugettext_lazy as _
from six import python_2_unicode_compatible


class ExtraFieldType(models.Model):
    """
    Model to create custom information holders.

    :name: Name of the attribute.
    :description: Description of the attribute.
    :model: Can be set in order to allow the use of only one model.
    :fixed_values: Can transform related exta fields into choices.

    """
    name = models.CharField(
        max_length=100,
        verbose_name=_('Name'),
    )

    description = models.CharField(
        max_length=100,
        blank=True, null=True,
        verbose_name=_('Description'),
    )

    model = models.CharField(
        max_length=10,
        choices=(
            ('Employee', 'Employee'),
            ('Payment', 'Payment'),
            ('Company', 'Company'),
        ),
        verbose_name=_('Model'),
        blank=True, null=True,
    )

    fixed_values = models.BooleanField(
        default=False,
        verbose_name=_('Fixed values'),
    )

    class Meta:
        ordering = ['name', ]

    def __str__(self):
        return '{0}'.format(self.name)


@python_2_unicode_compatible
class ExtraField(models.Model):
    """
    Model to create custom fields.

    :field_type: Connection to the field type.
    :value: Current value of this extra field.

    """
    field_type = models.ForeignKey(
        'payment.ExtraFieldType',
        verbose_name=_('Field type'),
        related_name='extra_fields',
        help_text=_('Only field types with fixed values can be chosen to add'
                    ' global values.'),
        on_delete=models.DO_NOTHING
    )

    value = models.CharField(
        max_length=200,
        verbose_name=_('Value'),
    )

    class Meta:
        ordering = ['field_type__name', ]

    def __str__(self):
        return '{0} ({1}) - {2}'.format(
            self.field_type, self.field_type.get_model_display() or 'general',
            self.value)


@python_2_unicode_compatible
class PaymentType(models.Model):
    """
    Model to create payment types.

    :name: Name of the type.
    :rrule: Recurring rule setting.
    :description: Description of the type.

    """
    name = models.CharField(
        max_length=100,
        verbose_name=_('Name'),
    )

    rrule = models.CharField(
        max_length=10,
        verbose_name=_('Recurring rule'),
        blank=True,
        choices=(
            ('MONTHLY', _('Monthly')),
            ('YEARLY', _('Yearly')),
        )
    )

    description = models.CharField(
        max_length=100,
        blank=True, null=True,
        verbose_name=_('Description'),
    )

    class Meta:
        ordering = ['name', ]

    def __str__(self):
        if self.rrule:
            return '{0} ({1})'.format(self.name, self.get_rrule_display())
        return '{0}'.format(self.name)


@python_2_unicode_compatible
class Payment(models.Model):
    """
    Model, which represents one single payment.

    :payment_type: Type of the payment.
    :employee: Connection to the payment receiver.
    :amount: Current amount of the payment.
    :date: Date the payment should accrue.
    :end_date: Optional end date, if payment type has a rrule.
    :extra_fields: Custom fields like e.g. quantity, bonus.

    """
    payment_type = models.ForeignKey(
        'payment.PaymentType',
        verbose_name=_('Payment type'),
        related_name='payments',
        on_delete=models.DO_NOTHING,
    )

    employee = models.ForeignKey(
        "core.EStaffProfile",
        verbose_name=_('Employee'),
        related_name='payments',
        on_delete=models.DO_NOTHING,
    )

    amount = models.DecimalField(
        decimal_places=2,
        max_digits=10,
        verbose_name=_('Amount'),
    )

    date = models.DateTimeField(
        verbose_name=_('Date'),
        default=now().today(),
    )

    end_date = models.DateTimeField(
        verbose_name=_('End of recurring period'),
        blank=True, null=True,
        help_text=_('This field is only considered, if the payment type has a'
                    ' recurring rule.'),
    )

    extra_fields = models.ManyToManyField(
        'payment.ExtraField',
        verbose_name=_('Extra fields'),
        blank=True,
    )

    description = models.CharField(
        max_length=100,
        blank=True, null=True,
        verbose_name=_('Description'),
    )

    class Meta:
        ordering = ['employee__user__first_name', '-date', ]

    def __str__(self):
        return '{0} - {1} ({2})'.format(self.payment_type, self.amount,
                                        self.employee)

    def get_date_without_tz(self):
        return localtime(self.date).replace(tzinfo=None)

    def get_end_date_without_tz(self):
        return localtime(self.end_date).replace(tzinfo=None)

    @property
    def is_recurring(self):
        return self.payment_type.rrule
