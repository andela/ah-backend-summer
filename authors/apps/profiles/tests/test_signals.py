from unittest.mock import patch

from authors.apps.authentication.tests.base_class import BaseTest
from authors.apps.profiles.signals import ProfilesSignalSender


class SignalTests(BaseTest):
    """
    Test that expected signals are emitted when events take place
    """
    def test_followers_updated_signal_properly_sent(self):
        # mock this method, so we can track how it is called
        signal = 'authors.apps.profiles.signals.followers_updated_signal.send'
        with patch(signal) as followers_updated_signal_mock:
            # it hasn't been called yet
            followers_updated_signal_mock.assert_not_called()
            user = self.activated_user()
            user2 = self.create_another_user_in_db()
            # following a user should trigger this
            user.profile.follow(user2.profile)
            # it should have been called
            followers_updated_signal_mock.assert_called_once_with(
                sender=ProfilesSignalSender, who_was_followed=user2.profile,
                who_followed=user.profile)
