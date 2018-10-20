from django.db import models
from django.contrib.auth.models import User

# number of mentees that a mentor can have at once
MENTEE_LIMIT = 3

class Language(models.Model):
    language_name = models.CharField(max_length=50)

    def __str__(self):
        return self.language_name

class CommunicationPlatform(models.Model):
    communication_platform = models.CharField(max_length=50)

    def __str__(self):
        return self.communication_platform

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    province_state_region = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    timezone = models.CharField(max_length=50)
    communication_platforms = models.ManyToManyField(CommunicationPlatform)
    sponsor_stage = models.CharField(max_length=50)
    languages = models.ManyToManyField(Language)
    faith = models.CharField(max_length=50)
    refugee_type = models.CharField(max_length=50)
    refugee_region = models.CharField(max_length=50)
    years_of_exp = models.IntegerField()

    def years_of_exp_default(self):
        return 0

    # from form.html
    # no need to save after
    @classmethod
    def createFromForm(cls, req):
        p = req.POST

        print(p['city'])

        prof = cls(user=req.user, first_name=p['first_name'], last_name=p['last_name'], phone_number=p['phone_number'],
                   city=p['city'], province_state_region=p['province_state_region'], country=p['country'], timezone=p['timezone'],
                   sponsor_stage=p['sponsor_stage'], faith=p['faith'], refugee_type=p['refugee_type'], refugee_region=p['refugee_region'],
                   years_of_exp=p['years_of_exp'])

        prof.save()

        # now to add comm platforms,  languages, and components

        languages = p['languages'].split(',')

        for lan in p['languages']:
            lan = lan.strip()

            if len(Language.objects.filter(language_name=lan)) == 0:
                Language.objects.create(language_name=lan)

            prof.languages.add(Language.objects.filter(language_name=lan)[0])

        for c in p['comm']:
            if len(CommunicationPlatform.objects.filter(communication_platform=c)) == 0:
                CommunicationPlatform.objects.create(communication_platform=c)

            prof.communication_platforms.add(CommunicationPlatform.objects.filter(communication_platform=c)[0])

        prof.save()

        return prof

    def requestMentorship(mentor):
        m = Mentorship(mentee = self.user.id, mentor = mentor.id)

        m.save()

    def isEligible(self):
        return len(self.getActiveMentees()) < MENTEE_LIMIT and years_of_exp >= 2

    def getActiveRelationships(self):
        return self.mentees.filter(is_active=True) + self.mentors.filter(is_active=True)

    def getActiveMentees(self):
        return self.mentees.filter(is_pending=False, is_active=True)

    def getPendingMentees(self):
        return self.mentees.filter(is_pending=True)

    def deactiveRelationship(self, other):
        if other in set(self.getActiveRelationships()):
            deact = Mentorship.objects.get(mentor_id=self.user.id, mentee_id=other.id)

            if deact is None:
                deact = Mentorship.objects.get(mentee_id=other.id, mentor_id=self.user.id)

            deact.deactivate()

    def rejectMentee(self, mentee):
        if mentee in set(self.getPendingMentees()):
            toReject = Mentorship.objects.get(mentor_id=self.user.id, mentee_id=mentee.id)
            toReject.noLongerPending()

    def acceptMentee(self, mentee):
        if mentee in set(self.getPendingMentees()):
            toAccept = Mentorship.objects.get(mentor_id=self.user.id, mentee_id=mentee.id)
            toAccept.activate()
            toAccept.noLongerPending()

    def scoreAgainst(self, mentor):
        # return the value of this potential pairing - self to mentor
        mentor = mentor.profile

        score = 1

        if self.timezone == mentor.timezone:
            score += 3

        langCounter = 0
        other = set(mentor.languages)
        for l in self.languages:
            if l in other:
                langCounter = 3 if langCounter == 0 else langCounter + 5

        score += langCounter

        if self.province_state_region == mentor.province_state_region:
            score += 2

        if self.country == mentor.country:
            score += 1

        if self.faith == mentor.faith:
            score += 2

        if mentor.years_of_exp > 5:
            score += 2

        if mentor.refugee_type == self.refugee_type:
            score += 1

        if self.refugee_region == mentor.refugee_region:
            score += 1

        commCount = 0
        other = set(mentor.communication_platforms)
        for c in self.communication_platforms:
            if c in other:
                commCount = 1 if commCount == 0 else commCount + 3

        if commCount == 0:
            score -= 5
        else:
            score += commCount

        return score

    def getNewMentor(self):
        eligible = [x for x in Profile.objects.all() if x.isEligible() and x != self]

        bestMentor = None
        topScore = None

        for e in eligible:
            newScore = self.scoreAgainst(e)

            if bestMentor is None or topScore < newScore:
                topScore = newScore
                bestMentor = e

        print(bestMentor)

        return bestMentor

class Mentorship(models.Model):
    mentee = models.ForeignKey(User, on_delete=models.CASCADE, related_name="mentees")
    mentor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="mentors")
    is_active = models.BooleanField()
    is_pending = models.BooleanField()

    def is_active_default(self):
        return False

    def is_pending_default(self):
        return True

    def deactivate(self):
        self.is_active = False

        self.save()

    def activate(self):
        self.is_active = True

        self.save()

    def noLongerPending(self):
        self.is_pending = False

        self.save()
