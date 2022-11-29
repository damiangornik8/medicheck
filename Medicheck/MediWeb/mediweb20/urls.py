"""mediweb20 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from . import views
from mediweb20 import views

from django.conf.urls import url 
from django.views.generic.base import TemplateView
from django.conf.urls import include

app_name= 'accounts'

urlpatterns = [
    path('admin/', admin.site.urls),
    
    url(r'^patient-risk-profiles/$', views.patientRiskProfiles, name="patient-risk-profiles"),
    url(r'^alzheimer-risk-profiles-run/$', views.alzheimerRiskProfilesRun, name="alzheimer-risk-profiles-run"),
    url(r'^logout/$', views.logout, name="logout"),
    url(r'^signup-post/$', views.signup_post, name="signup-post"),

    url(r'^dashboard/$', views.dashboard, name="dashboard"),
    url(r'^signin/$', views.signin, name="signin"),
    url(r'^signup/$', views.signup, name="signup"),


    url(r'^update-patient-details/$', views.updatePatientDetails, name="update-patient-details"),


    url(r'^patient-details/$', views.seePatientDetails, name="patient-details"),

    url(r'^patients/$', views.patients, name="patients"),
    url(r'^risk-profiles/$', views.riskProfiles, name="risk-profiles"),
    url(r'^user-profiling/$', views.userProfiling, name="user-profiling"),
    url(r'^data-aggregator/$', views.dataAggregator, name="data-aggregator"),

    url(r'^data-aggregator-post/$', views.dataAggregatorPost, name="data-aggregator-post"),


    url(r'^$', views.welcome, name="welcome"),
]






