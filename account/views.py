from django.shortcuts import redirect, render
from account.forms import RegistrationForm
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes

from account.token import account_activation_token


def account_register(request):
    # if request.user.is_authenticated:
    #     return redirect('/')
    if request.method == "POST":
        register_form = RegistrationForm(request.POST)
        if register_form.is_valid():
            user = register_form.save(commit=False)
            user.email = register_form.cleaned_data['email']
            user.set_password(register_form.cleaned_data['password'])
            user.is_active = False
            user.save()
            # set up email
            current_site = get_current_site(request)
            subject = "Activate your account"
            email_template_lication = '/account/registration/account_activation_email.html'
            message = render_to_string(email_template_lication,
                                       {'user': user,
                                        'domain': current_site.domain,
                                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                                        'token': account_activation_token.make_token(user),
                                        })
            user.email_user(subject=subject, message=message)
    else:
        register_form = RegistrationForm()
    return render(request, 'account/registration/register.html', {'form': register_form})