from allauth.account.forms import SignupForm


class CustomSignupForm(SignupForm):
    def __init__(self, *args, **kwargs):
        initial_email = kwargs.get("initial", {}).get("email")
        super().__init__(*args, **kwargs)

        if initial_email:
            self.fields["email"].initial = initial_email
            self.fields["email2"].initial = initial_email
