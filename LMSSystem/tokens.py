from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six
from six import text_type

class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.profile.Account_Confirmed)
        )

account_activation_token = AccountActivationTokenGenerator()