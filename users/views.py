from allauth.account.views import SignupView
from .forms import CustomSignupForm

# Create your views here.


class CustomSignupView(SignupView):
    form_class = CustomSignupForm

    def get_initial(self):
        initial = super().get_initial()
        email = self.request.GET.get("email")
        if email:
            initial["email"] = email
        return initial
