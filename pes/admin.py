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

from django.contrib.admin.views.main import ChangeList

class UnorderedChangeList(ChangeList):
    def get_ordering(self):
        return '', ''

class TeamAdmin(admin.ModelAdmin):
    list_display = ['__unicode__', 'att', 'dif', 'tat', 'vel', 'tec', 'fis']
    ordering = None

    def queryset(self, request):
        qs = self.model._default_manager.get_query_set()
        qs = qs.extra(select={
                'total': 'att+dif+tat+vel+tec+fis'
                })
        qs = qs.order_by('-total')
        return qs

    def get_changelist(self, request, **kwargs):
        return UnorderedChangeList


admin.site.register(models.Team, TeamAdmin)
admin.site.register(models.Match, MatchAdmin)
admin.site.register(models.UserProfile, UserProfileAdmin)
