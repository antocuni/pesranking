from django.http import HttpResponseRedirect
from pes import models


def updateranking(request):
    models.Match.updateranking()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

