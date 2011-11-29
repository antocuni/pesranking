# -*- encoding: utf-8 -*-
from django.contrib import admin
from django.contrib.admin.util import flatten_fieldsets
from pes import models

class UserProfileAdmin(admin.ModelAdmin):
    model = models.UserProfile
    list_display = ['user', 'ranking']
    fields = ['user', 'ranking']
    readonly_fields = fields
    ordering = ['-ranking']


admin.site.register(models.Team)
admin.site.register(models.Match)
admin.site.register(models.UserProfile, UserProfileAdmin)
