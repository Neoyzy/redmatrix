from django.contrib import admin
from openwisp_users.multitenancy import (MultitenantAdminMixin,
                                         MultitenantOrgFilter,
                                         MultitenantRelatedOrgFilter)

from .models import Device, Consumer
from import_export import resources
from import_export.admin import ImportExportActionModelAdmin


class BaseAdmin(MultitenantAdminMixin, admin.ModelAdmin):
    pass


class DeviceResource(resources.ModelResource):

    class Meta:
        model = Device
        export_order = ('id', 'name', 'IP', 'MAC', 'is_active', 'organization', 'created', 'modified')


@admin.register(Device)
class DeviceAdmin(ImportExportActionModelAdmin):
    list_display = ('name', 'IP', 'MAC', 'organization', 'is_active', 'id')
    search_fields = ('is_active', 'organization')
    list_filter = [('organization', MultitenantOrgFilter)]
    date_hierarchy = 'created'
    resource_class = DeviceResource
# class DeviceAdmin(BaseAdmin):
#     list_display = ['name', 'IP', 'MAC', 'organization', 'is_active']
#     list_filter = [('organization', MultitenantOrgFilter)]
#     fields = ['name', 'organization', 'IP', 'MAC', 'created', 'modified', 'is_active']


class ConsumerAdmin(BaseAdmin):
    list_display = ['name', 'organization', 'device', 'created', 'modified', 'is_online']
    list_filter = [('organization', MultitenantOrgFilter),
                   ('device', MultitenantRelatedOrgFilter)]
    fields = ['name', 'organization', 'device', 'created', 'modified', 'is_online']
    multitenant_shared_relations = ['device']

    # def change_view(self, request, object_id, form_url='', extra_context=None):
    #     extra_context = extra_context or {}
    #     extra_context.update({
    #         'additional_buttons': [
    #             {
    #                 'type': 'button',
    #                 'url': 'dummy',
    #                 'class': 'BulkLoad',
    #                 'value': 'Bulk Load',
    #             }
    #         ]
    #     })
    #     return super(ConsumerAdmin, self).change_view(request, object_id, form_url, extra_context)


# admin.site.register(Device, DeviceAdmin)
admin.site.register(Consumer, ConsumerAdmin)
