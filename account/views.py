from django.shortcuts import render
from django.views.generic import View
from .forms import LoginForm, RegistrationForm, UpdateUserForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, JsonResponse
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.forms import model_to_dict


class LoginView(View):
    """авторизация"""

    # отрисовка
    def get(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        context = {'form': form}
        return render(request, 'account/auth/login.html', context)

    # отправка
    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            remember_me = form.cleaned_data['remember_me']
            user = authenticate(username=username, password=password)
            login(request, user)
            if not remember_me:
                request.session.set_expiry(0)
            return HttpResponseRedirect('/account/profile')

        context = {'form': form}
        return render(request, 'account/auth/login.html', context)


class RegistrationView(View):
    """Регистрация"""

    def get(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST or None)
        context = {
            'form': form,
        }
        return render(request, 'account/auth/registration.html', context)

    def post(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST or None)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.is_active = False
            new_user.username = form.cleaned_data['username']
            new_user.email = form.cleaned_data['email']
            new_user.first_name = form.cleaned_data['first_name']
            new_user.last_name = form.cleaned_data['last_name']
            new_user.save()
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            mail_subject = 'Ссылка для активации аккаунта'
            message = render_to_string('account/auth/acc_active_email.html', {
                'user': new_user,
                'domain': '127.0.0.1:8000',
                'uid': urlsafe_base64_encode(force_bytes(new_user.pk)),
                'token': account_activation_token.make_token(new_user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()

            messages.success(request, 'На ваш почтовый ящик отправлено сообщение для активации учетной записи.')
            return HttpResponseRedirect('/')
        context = {
            'form': form,
        }
        return render(request, 'account/auth/registration.html', context)


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Спасибо за подтверждение по электронной почте. '
                                  'Теперь вы можете войти в свою учетную запись.')
        return HttpResponseRedirect('/login')
    else:
        messages.success(request, 'Ссылка для активации недействительна!')
        return HttpResponseRedirect('/')


@login_required
def profile(request):
    user_form = UpdateUserForm()
    user = request.user
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        if user_form.is_valid():
            instance = user_form.save(commit=False)
            instance.save()
            return JsonResponse(model_to_dict(instance, fields=['username']), status=201)
        else:
            return JsonResponse(user_form.errors, safe=False, status=200)
    else:
        user_form = UpdateUserForm(instance=request.user)

    return render(request, 'account/profile.html', {'user_form': user_form})
