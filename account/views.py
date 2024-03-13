from django.shortcuts import render, redirect
from account.forms import RegistrationForm
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login

from account.token import account_activation_token
from account.models import UserBase


@login_required()
def dashboard(request):
    return render(request, 'account/user/dashboard.html')


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
            email_template_location = '/account/registration/account_activation_email.html'
            message = render_to_string(email_template_location,
                                       {'user': user,
                                        'domain': current_site.domain,
                                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                                        'token': account_activation_token.make_token(user),
                                        })
            user.email_user(subject=subject, message=message)
    else:
        register_form = RegistrationForm()
    return render(request, 'account/registration/register.html', {'form': register_form})


def account_activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = UserBase.objects.get(pk=uid)
        if user and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            return redirect("account:dashboard")
        else:
            return render(request, 'account/registration.activation_invalid.html')
    except Exception as e:
        print(e)
