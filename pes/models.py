import datetime
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.db.utils import IntegrityError

class UserProfile(models.Model):
    class Meta:
        verbose_name = 'Dati utente'
        verbose_name_plural = 'Classifica'
    
    user = models.OneToOneField(User)
    ranking = models.FloatField(default=1600)

    def __unicode__(self):
        return '%s (%.3f)' % (self.user, self.ranking)

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        try:
            UserProfile.objects.create(user=instance)
        except IntegrityError:
            pass # bah, this is a workaround, because create_user_profile
                 # seems to be called twice

post_save.connect(create_user_profile, sender=User)


class Team(models.Model):

    class Meta:
        verbose_name = "Squadra"
        verbose_name_plural = "Squadre"

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
        return '%s (%.3f)' % (self.name, self.ranking())


class Match(models.Model):

    class Meta:
        verbose_name = "Partita"
        verbose_name_plural = "Partite"

    class Result:
        WIN = 1
        TIE = 0.5
        LOSE = 0

    date = models.DateField(default=datetime.date.today)
    userA = models.ForeignKey(User, related_name='+')
    teamA = models.ForeignKey(Team, related_name='+')
    userB = models.ForeignKey(User, related_name='+')
    teamB = models.ForeignKey(Team, related_name='+')
    goalA = models.IntegerField(blank=True, null=True)
    goalB = models.IntegerField(blank=True, null=True)
    deltaA = models.IntegerField(blank=True, null=True)
    deltaB = models.IntegerField(blank=True, null=True)

    def play(self):
        a, b = self.goalA, self.goalB
        if a > b:
            result = self.Result.WIN
        elif a == b:
            result = self.Result.TIE
        else:
            result = self.Result.LOSE
        #
        K = 30
        self._update_deltas(K, result)

    def _update_deltas(self, K, result):
        Ra = self.userA.get_profile().ranking
        Rb = self.userB.get_profile().ranking
        #
        Ea = expected(Ra, Rb, self.teamA, self.teamB)
        Eb = expected(Rb, Ra, self.teamB, self.teamA)
        #
        self.deltaA = calc_delta(K, Ea, result)
        self.deltaB = calc_delta(K, Eb, 1.0-result)
        self.save()

    def __str__(self):
        def fmtfloat(x):
            if x is None:
                return ''
            return '%.3f' % x
        return '%s - %s (%s - %s) %d - %d (%s, %s)' % (
            self.userA.username,
            self.userB.username,
            self.teamA.name,
            self.teamB.name,
            self.goalA,
            self.goalB,
            fmtfloat(self.deltaA),
            fmtfloat(self.deltaB))

    @classmethod
    def updateranking(cls):
        matches = list(cls.objects.filter(deltaA = None))
        import pdb;pdb.set_trace()
        for match in matches:
            match.play()

def calc_delta(K, exp_result, result):
    return K * (result-exp_result)

def expected(Ra, Rb, teamA, teamB):
    dr = Rb-Ra + (teamB.ranking() - teamA.ranking())*4
    return 1.0 / (1 + 10**(dr/400.0))
