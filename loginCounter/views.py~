from django.http import HttpResponse
from django.utils import simplejson as json
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from loginCounter.models import Users
import StringIO
import unittest

SUCCESS               =   1  # : a success
ERR_BAD_CREDENTIALS   =  -1  # : (for login only) cannot find the user/password pair in the database
ERR_USER_EXISTS       =  -2  # : (for add only) trying to add a user that already exists
ERR_BAD_USERNAME      =  -3  # : (for add only) invalid user name (empty string and longer than 128 characters is invalid)
ERR_BAD_PASSWORD      =  -4  # : (for add only) invalid password (longer than 128 characters is invalid)

@csrf_exempt
def login(request):
    POSTdata = json.loads(request.body)
    user = POSTdata['user']
    password = POSTdata['password']
    response_data = {}

    try:
        dbData = Users.objects.get(user=user)
        dbDict = model_to_dict(dbData)
    except Users.DoesNotExist:
        dbDict = {'password': None}

    if dbDict['password'] == password:
        response_data['errCode'] = SUCCESS 
        dbData.count += 1
        dbData.save()
        response_data['count'] = dbData.count
    else:
        response_data['errCode'] = ERR_BAD_CREDENTIALS

    return HttpResponse(json.dumps(response_data), content_type="application/json")

@csrf_exempt
def add(request):

    POSTdata = json.loads(request.body)
    user = POSTdata['user']
    password = POSTdata['password']
    response_data = {}

    try:
        dbData = model_to_dict(Users.objects.get(user=user))
    except Users.DoesNotExist:
        dbData = {'user': None}

    if dbData['user'] == user:
        response_data['errCode'] = ERR_USER_EXISTS
    elif user == '' or len(user) > 128:
        response_data['errCode'] = ERR_BAD_USERNAME
    elif len(password) > 128:
        response_data['errCode'] = ERR_BAD_PASSWORD
    else:
        newEntry = Users(user=user, password=password, count=1)
        newEntry.save()
        response_data['errCode'] = SUCCESS
        response_data['count'] = 1

    return HttpResponse(json.dumps(response_data), content_type="application/json")

@csrf_exempt
def resetFixture(request):

    Users.objects.all().delete()
    response_data = {'errCode': SUCCESS}

    return HttpResponse(json.dumps(response_data), content_type="application/json")

@csrf_exempt
def unitTests(request):

    buffer = StringIO.StringIO()
    suite = unittest.TestLoader().loadTestsFromTestCase(loginCounter.tests)
    result = unittest.TextTestRunner(stream = buffer, verbosity = 2).run(suite)

    rv = {"totalTests": result.testsRun, "nrFailed": len(result.failures), "output": buffer.getvalue()}
    return HttpResponse(json.dumps(rv), content_type = "application/json")

