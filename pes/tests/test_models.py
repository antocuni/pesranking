import py
import os
import sys
from datetime import date
from decimal import Decimal
from django.core import management


def setup_module(mod):
    from pesranking import settings
    root = py.path.local(settings.__file__).dirpath()
    sys.path.insert(0, str(root))
    settings.DATABASES['default']['NAME'] = ':memory:'
    management.setup_environ(settings)
    management.execute_from_command_line(['manage.py', 'syncdb', '--noinput'])

def test_updateranking():
    from pesranking.pes.models import Team, Match, UserProfile
    from django.contrib.auth.models import User
    #
    pippo = User(username='pippo')
    pippo.save()
    pluto = User(username='pluto')
    pluto.save()
    assert pippo.get_profile().ranking == 1600
    #
    topolinia = Team(name='topolinia',
                att=10, dif=10, fis=10, vel=10, tat=10, tec=10)
    assert topolinia.ranking() == 10
    topolinia.save()
    #
    match1 = Match(userA=pippo, userB=pluto,
                   teamA=topolinia, teamB=topolinia,
                   goalA=3, goalB=0)
    match2 = Match(userA=pippo, userB=pluto,
                   teamA=topolinia, teamB=topolinia,
                   goalA=3, goalB=0)
    #
    match1.save()
    match2.save()
    Match.updateranking()
    # refresh the data
    match1 = Match.objects.get(pk=match1.id)
    match2 = Match.objects.get(pk=match2.id)
    # check the deltas for the first match
    delta = match1.deltaA
    assert delta > 0
    assert match1.deltaB == -delta
    #
    # the delta for the second match are the same
    assert match2.deltaA == delta
    assert match2.deltaB == -delta
    #
    # check that we updated the users
    for obj in (pippo, pluto):
        try:
            del obj._profile_cache
        except AttributeError:
            pass
    assert pippo.get_profile().ranking == 1600 + delta*2
    assert pluto.get_profile().ranking == 1600 - delta*2
    #
    # play another match
    match3 = Match(userA=pippo, userB=pluto,
                   teamA=topolinia, teamB=topolinia,
                   goalA=0, goalB=0)
    delta3 = match3.deltaA
    assert delta3 < 0 # because we expected pippo to beat pluto
