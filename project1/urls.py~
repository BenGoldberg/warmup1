from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^users/login', 'loginCounter.views.login', name='login'),
    url(r'^users/add', 'loginCounter.views.add', name='add'),
    url(r'^TESTAPI/resetFixture', 'loginCounter.views.resetFixture', name='resetFixture'),
    url(r'^TESTAPI/unitTests', 'loginCounter.views.unitTests', name='unitTests'),
)
