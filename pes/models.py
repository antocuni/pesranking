import datetime
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    ranking = models.FloatField(default=1600)

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)


class Team(models.Model):

    class Meta:
        pass

    name = models.CharField(max_length=200)
    att = models.IntegerField()
    dif = models.IntegerField()
    fis = models.IntegerField()
    vel = models.IntegerField()
    tat = models.IntegerField()
    tec = models.IntegerField()

    def ranking(self):
        return float(self.att+
                     self.dif+
                     self.fis+
                     self.vel+
                     self.tat+
                     self.tec)/6

    def __unicode__(self):
        return '%s (%s)' % (self.name, self.ranking())


class Match(object):

    date = models.DateField(default=datetime.date.today)
    userA = models.ForeignKey(User)
    teamA = models.ForeignKey(Team)
    userB = models.ForeignKey(User)
    teamB = models.ForeignKey(Team)
    goalA = models.IntegerField(blank=True, null=True)
    goalB = models.IntegerField(blank=True, null=True)
    deltaA = models.IntegerField(blank=True, null=True)
    deltaB = models.IntegerField(blank=True, null=True)

    def play(self):
        a, b = self.goalA, self.goalB
        if a > b:
            result = Result.WIN
        elif a == b:
            result = Result.TIE
        else:
            result = Result.LOSE
        #
        K = 30
        self.calc(K, result)

    def calc(self, K, result):
        Ra = self.userA.get_profile().ranking
        Rb = self.userB.get_profile().ranking
        #
        Ea = expected(Ra, Rb, self.teamA, self.teamB)
        Eb = expected(Rb, Ra, self.teamB, self.teamA)
        #
        self.deltaA = calc_delta(K, Ea, result)
        self.deltaB = calc_delta(K, Eb, 1.0-result)

    def __str__(self):
        return '%s - %s (%s - %s) %d - %d (%.3f, %.3f)' % (
            self.userA.username,
            self.userB.username,
            self.teamA.username,
            self.teamB.username,
            self.goalA,
            self.goalB,
            self.deltaA,
            self.deltaB)


def calc_delta(K, exp_result, result):
    return K * (result-exp_result)

def expected(Ra, Rb, teamA, teamB):
    dr = Rb-Ra + (teamB.rating - teamA.rating)*4
    return 1.0 / (1 + 10**(dr/400.0))
