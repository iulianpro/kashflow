from django.shortcuts import render
from django.utils.crypto import get_random_string

import environ

# Create your views here.


def home(request):
    env = environ.Env()
    response_type = 'code'
    client_id = env('KF_CLIENT_ID')
    redirect_uri = '/home-auth/'
    state_id = get_random_string(length=32)
    request.session['state_id'] = state_id

    context = {
        'response_type': response_type,
        'client_id': client_id,
        'redirect_uri': redirect_uri,
        'state_id': state_id,
    }

    return render(request, 'core/home.html', context)


def home_auth(request):

    return render(request, 'core/home-auth.html')
