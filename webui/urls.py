from django.conf.urls import include, url
# from django.contrib import admin
from webui import views
from webui.forms import LoginForm
# from info_api.models import List
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.views import login,logout

urlpatterns = [
    url(r'^$',views.index,name='index'),
    ### status
    url(r'^status/$',login_required(views.Status_ListViewSet.as_view()),name='status-list'),
    url(r'^status/update/(?P<pk>\d+)/$',login_required(views.Status_UpdateViewSet.as_view()),name='status-update'),
    url(r'^status/create/$',login_required(views.Status_CreateViewSet.as_view()),name='status-create'),

    ### project
    url(r'^project/$', login_required(views.Project_ListViewSet.as_view()), name='project-list'),
    url(r'^project/update/(?P<pk>\d+)/$', login_required(views.Project_UpdateViewSet.as_view()), name='project-update'),
    url(r'^project/create/$', login_required(views.Project_CreateViewSet.as_view()), name='project-create'),

    ### publish
    url(r'^mission/$', login_required(views.Mission_ListViewSet.as_view()), name='mission-list'),
    url(r'^mission/create/$', login_required(views.Mission_CreateViewSet.as_view()), name='mission-create'),

    ### version
    url(r'^version/$', login_required(views.Version_historyViewSet.as_view()), name='version-list'),
    # url(r'^progress/$', login_required(views.Progress_ViewSet.as_view()), name='progress-list'),
    #
    url(r'^run/(?P<job_id>\d+)/$', login_required(views.run_job), name='run-job'),

    url(r'^v1/mission/$', views.mission_run_view, name='mission-api'),
    url(r'^v1/version/$', views.versioin_console_view, name='version-api'),
    #
    url(r'^reset/(?P<job_id>\d+)/$', login_required(views.reset_job), name='reset-job'),

    url(r'^login/$',
        login,
        {
            'template_name': 'webui/login.html',
            'authentication_form': LoginForm,

        },
        name='login',),

    # Django Select2
    url(r'^select2/', include('django_select2.urls')),

    url(r'^logout/$',
        logout,
        {
            'next_page': '/',
        },
        name='logout'),]
