# -*- encoding: utf-8 -*-
from django.contrib import admin
from django.contrib.admin.util import flatten_fieldsets
from pes import models

admin.site.register(models.Team)
admin.site.register(models.Match)
