from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.crypto import get_random_string
from django.contrib import messages

from .models import AuthVarsControl

import environ
import requests


def get_env(var):

    env = environ.Env()
    return env(var)


def home(request):

    response_type = 'code'
    client_id = get_env('KF_CLIENT_ID')

    if settings.DEBUG:
        base_uri = 'http://localhost:8000/'
    else:
        base_uri = request.build_absolute_uri()

    redirect_uri = base_uri + 'home-validate/'
    state_id = get_random_string(length=32)
    AuthVarsControl.objects.create(
        state=state_id,
    )

    context = {
        'response_type': response_type,
        'client_id': client_id,
        'redirect_uri': redirect_uri,
        'state_id': state_id,
    }

    return render(request, 'core/home.html', context)


def home_validate(request):

    # collect code and state vars from url
    auth_code = request.GET.get('code')
    received_state_id = request.GET.get('state')
    print('Auth code: ' + auth_code)
    print('Received State ID: ' + received_state_id)

    # check if received state var string is the same with the initial state var string
    auth_vars_control = AuthVarsControl.objects.last()
    state_id = auth_vars_control.state
    if state_id == received_state_id:
        print('State var matched')
        auth_vars_control.delete()
        print('Stored state var deleted')

        # get client id and secret from environ
        client_id = get_env('KF_CLIENT_ID')
        print('ENV Client ID: ' + client_id)
        client_secret = get_env('KF_CLIENT_SECRET')
        print('ENV Secret: ' + client_secret)

        # convert them into authorisation header
        encoded_auth_header = get_env('ENCODED_CLIENT_ID_SECRET')
        print('Encoded Auth Header: ' + encoded_auth_header)

        # define rest of the vars
        auth_code = auth_code
        if settings.DEBUG:
            base_uri = 'http://localhost:8000/'
        else:
            base_uri = request.build_absolute_uri()
        redirect_uri = base_uri + 'home-validate/'
        post_url = 'https://api.iris.co.uk/oauth2/v1/token'
        headers = {
            'Authorization': 'Basic ' + encoded_auth_header,
            'Content-Type': 'x-www-form-urlencoded',
        }
        data = {
            'grant_type': 'authorization_code',
            'code': auth_code,
            'redirect_uri': redirect_uri,
        }

        # making the post request to kashflow
        response = requests.post(post_url, headers=headers, data=data)
        print('POST Request URL: ' + str(response.request.url))
        print('POST Request Body: ' + str(response.request.body))
        print('POST Request Headers: ' + str(response.request.headers))
        return HttpResponse(response.text, response.reason, response.status_code)

    else:
        print('Path 1')
        messages.error(
            request, 'Your validation data doesn\'t match. Plese connect to the API again')
        return redirect('home')


def home_authenticated(request):
    if 'json_response' in request.session:
        json_response = request.session.get('json_response')
        context = {'json_response': json_response}
    else:
        context = {'json_response': 'Nothing is json_response'}

    return render(request, 'core/home-authenticated.html', context)
