from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _
from openwisp_users.mixins import OrgMixin, ShareableOrgMixin
from openwisp_utils.base import TimeStampedEditableModel


class Template(ShareableOrgMixin):
    name = models.CharField(max_length=16)


class Config(OrgMixin):
    name = models.CharField(max_length=16)
    template = models.ForeignKey(Template, blank=True, null=True,
                                 on_delete=models.CASCADE)

    def clean(self):
        self._validate_org_relation('template')


class Device(OrgMixin, TimeStampedEditableModel):
    name = models.CharField(_('name'), max_length=64)
    IP = models.CharField(_('IP Address'), max_length=64)
    MAC = models.CharField(_('MAC Address'), max_length=64)
    is_active = models.BooleanField(default=False,)

    def __str__(self):
        value = self.name
        if not self.is_active:
            value = '{0} ({1})'.format(value, _('disabled'))
        return value

    class Meta:
        abstract = False

    def clean(self):
        if self.name == "Intentional_Test_Fail":
            raise ValidationError('Intentional_Test_Fail')
        return self


class Consumer(OrgMixin, TimeStampedEditableModel):
    name = models.CharField(_('name'), max_length=64)
    is_online = models.BooleanField(default=False, )
    device = models.ForeignKey('testapp.Device', null=True, on_delete=models.CASCADE)

    def __str__(self):
        value = self.name
        if not self.is_online:
            value = '{0} ({1})'.format(value, _('disabled'))
        return value

    class Meta:
        abstract = False

