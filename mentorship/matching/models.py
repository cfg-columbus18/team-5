from django.db import models
from django.contrib.auth.models import User

# number of mentees that a mentor can have at once
MENTEE_LIMIT = 3

class Language(models.Model):
    language_name = models.CharField(max_length=50)

    def __str__(self):
        return self.language_name

class SponsorComponent(models.Model):
    sponsor_component = models.CharField(max_length=50)

    def __str__(self):
        return self.sponsor_component

class CommunicationPlatform(models.Model):
    communication_platform = models.CharField(max_length=50)

    def __str__(self):
        return self.communication_platform

class Profile(models.Model):
    # profile -> user ~foreignkey
    profile = models.ForeignKey(User, on_delete=models.CASCADE)
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
    sponsor_components = models.ManyToManyField(SponsorComponent)
    faith = models.CharField(max_length=50)
    sponsor_type = models.CharField(max_length=50)
    refugee_region = models.CharField(max_length=50)
    years_of_exp = models.IntegerField()

    def requestMentorship(mentor):
        m = Mentorship(mentee = self.user.id, mentor = mentor.id)

        m.save()

    def isEligible(self):
        return len(getActiveMentees) < MENTEE_LIMIT and years_of_exp >= 2

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
        pass

    def getNewMentor(self):
        eligible = [x for x in Profile.objects.all() if x.isEligible() and x != self]

        bestMentor = None
        topScore = None

        for e in eligible:
            newScore = self.scoreAgainst(e)

            if bestMentor is None or topScore < newScore:
                topScore = newScore
                bestMentor = e

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
