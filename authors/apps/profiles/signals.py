from django.db.models.signals import m2m_changed
from django.dispatch import Signal, receiver

from authors.apps.profiles.models import Profile

# custom signal we shall send when a new follow action happens
# the rationale for this custom signal is discussed in the articles app
followers_updated_signal = Signal(
    providing_args=["who_was_followed", "who_followed"])


class ProfilesSignalSender:
    pass


@receiver(m2m_changed, sender=Profile.follows.through)
def on_new_follower_added(sender, **kwargs):
    """called when someone is followed"""
    if kwargs['action'] is "post_add":
        for person_i_have_followed in kwargs['pk_set']:
            followers_updated_signal.send(sender=ProfilesSignalSender,
                                          who_was_followed=Profile.objects.get(
                                              pk=person_i_have_followed),
                                          who_followed=kwargs['instance'])
