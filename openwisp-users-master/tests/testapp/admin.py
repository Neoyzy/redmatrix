from django.contrib import admin
from django import template
from openwisp_users.multitenancy import (MultitenantAdminMixin,
                                         MultitenantOrgFilter,
                                         MultitenantRelatedOrgFilter)

from .models import Device, Consumer


class BaseAdmin(MultitenantAdminMixin, admin.ModelAdmin):
    pass


class DeviceAdmin(BaseAdmin):
    list_display = ['name', 'IP', 'MAC', 'organization', 'is_active']
    list_filter = [('organization', MultitenantOrgFilter)]
    fields = ['name', 'organization', 'IP', 'MAC', 'created', 'modified', 'is_active']


class ConsumerAdmin(BaseAdmin):
    list_display = ['name', 'organization', 'device', 'created', 'modified', 'is_online']
    list_filter = [('organization', MultitenantOrgFilter),
                   ('device', MultitenantRelatedOrgFilter)]
    fields = ['name', 'organization', 'device', 'created', 'modified', 'is_online']
    multitenant_shared_relations = ['device']

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context.update({
            'additional_buttons': [
                {
                    'type': 'button',
                    'url': 'dummy',
                    'class': 'BulkLoad',
                    'value': 'Bulk Load',
                }
            ]
        })
        return super(ConsumerAdmin, self).change_view(request, object_id, form_url, extra_context)


admin.site.register(Device, DeviceAdmin)
admin.site.register(Consumer, ConsumerAdmin)
