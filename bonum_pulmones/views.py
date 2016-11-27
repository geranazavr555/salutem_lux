import uuid

from django.shortcuts import render, redirect
from django.http import HttpResponseBadRequest
from django.contrib.auth import authenticate
from django.contrib.auth import login as _login
from django.contrib.auth import logout as _logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User as _User
from django.core.urlresolvers import reverse

from bonum_pulmones import forms, models
from bonum_pulmones import measurements_processing


def main(request):
    if request.user.is_authenticated():
        return redirect(reverse('history'))
    else:
        return redirect(reverse('login'))


def login(request):
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                _login(request, user)
                return redirect(reverse('main'))
            else:
                return render(request, 'login.html', {'form': form, 'disabled_login': True})
        else:
            return render(request, 'login.html', {'form': form, 'invalid_login': True})

    elif request.method == 'GET':
        if request.user.is_authenticated():
            return redirect(reverse('history'))
        else:
            return render(request, 'login.html', {'form': forms.LoginForm()})
    else:
        return HttpResponseBadRequest('Unsupported method')


def logout(request):
    _logout(request)
    return redirect(reverse('main'))


def register(request):
    if request.method == 'GET':
        return render(request, 'register.html', {'form': forms.RegisterForm})

    elif request.method == 'POST':
        form = forms.RegisterForm(request.POST)
        if form.is_valid():
            auth_user = _User(username=request.POST['username'],
                              first_name=request.POST['first_name'],
                              last_name=request.POST['last_name'])
            auth_user.set_password(request.POST['password'])
            auth_user.save()
            user = models.User(auth_user=auth_user)
            user.save()
            return redirect(reverse('main'))
        else:
            return render(request, 'register.html', {'form': form})
    else:
        return HttpResponseBadRequest('Unsupported method')


def _get_user_by_auth(auth_user):
    return models.User.objects.get(auth_user=auth_user)


@login_required
def submit(request):
    if request.method == 'GET':
        return render(request, 'submit.html', {'form': forms.SubmitForm})

    elif request.method == 'POST':
        form = forms.SubmitForm(request.POST, request.FILES)
        if form.is_valid():
            filename = str(uuid.uuid4())
            measurements_processing.handle_uploaded_file(request.FILES['file'], filename)

            user = _get_user_by_auth(request.user)

            file = models.MedicalData(filename=filename, owner=user)
            file.save()

            try:
                measurements_processing.process(filename)
            except NotImplementedError:
                pass

            return redirect(reverse('history'))
        else:
            return render(request, 'submit.html', form)

    else:
        return HttpResponseBadRequest('Unsupported method')


def _process_result(measurement):
    if measurement.result is None:
        return None
    return int(measurement.result * 100)


@login_required
def get_result(request, measurement_id):
    return render(request, 'result.html',
                  {'result': _process_result(models.MedicalData.objects.get(filename=measurement_id)),
                   'date': models.MedicalData.objects.get(filename=measurement_id).date})


@login_required
def history(request):
    return render(request, 'history.html',
                  {'history': models.MedicalData.objects.filter(owner=_get_user_by_auth(request.user))})
