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
    list_display = ['users', 'teams', 'goals', 'deltaA', 'deltaB']
    list_display_links = list_display
    
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

    def users(self, obj):
        return u'%s - %s' % (obj.userA.username, obj.userB.username)
    users.short_description = 'Utenti'

    def teams(self, obj):
        return u'%s - %s' % (obj.teamA.name, obj.teamB.name)
    teams.short_description = 'Squadre'

    def goals(self, obj):
        return u'%s - %s' % (obj.goalA, obj.goalB)
    goals.short_description = 'Risultato'

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
