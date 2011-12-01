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

class MatchAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {
                'classes': ('fixed-columns',),
                'fields': ['date',
                           ('userA', 'userB'),
                           ('teamA', 'teamB'),
                           ('goalA', 'goalB'),
                           ('deltaA', 'deltaB'),
                           ]
                })
        ]
    readonly_fields = ['deltaA', 'deltaB']

class TeamAdmin(admin.ModelAdmin):
    list_display = ['__unicode__', 'att', 'dif', 'tat', 'vel', 'tec', 'fis']

admin.site.register(models.Team, TeamAdmin)
admin.site.register(models.Match, MatchAdmin)
admin.site.register(models.UserProfile, UserProfileAdmin)
