# coding=utf8
from django.db.models import Q
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render,redirect
from api.models import *
from django.core.urlresolvers import reverse_lazy
import forms
from django.http import HttpResponse,HttpResponseBadRequest
import operator
import json
from tasks import MissionTask
from core.common import get_result,logger
from abstract.views import Base_CreateViewSet, Base_ListViewSet, Base_UpdateViewSet


def index(req):
    if req.user.is_authenticated():

        response = render(req,'webui/index.html',{"username":req.user.last_name,
                                                  "active":"index"
                                                  }
                          )
    else:
        response =redirect('login')
    return response

class Status_CreateViewSet(Base_CreateViewSet):
    model = Status
    form_class = forms.StatusForm
    template_name = 'api/status_form.html'
    success_url = reverse_lazy('status-list')

class Status_UpdateViewSet(Base_UpdateViewSet):
    model = Status
    form_class = forms.StatusForm
    template_name = 'api/status_form.html'
    success_url = reverse_lazy('status-list')

class Status_ListViewSet(Base_ListViewSet):
    Status.objects.all().count()
    model = Status
    template_name = 'api/status.html'
    paginate_by = 10

    def get_queryset(self):
        name = None
        try:
            name = self.request.GET['keyword']
        except:
            pass

        if name:
            return self.model.objects.filter(item__icontains=name)
        else:
            return self.model.objects.all()
#
class Project_CreateViewSet(Base_CreateViewSet):
    model = Project
    form_class = forms.ProjectForm
    template_name = 'api/project_form.html'
    success_url = reverse_lazy('project-list')

class Project_UpdateViewSet(Base_UpdateViewSet):
    model = Project
    form_class = forms.ProjectForm
    template_name = 'api/project_form.html'
    success_url = reverse_lazy('project-list')

class Project_ListViewSet(Base_ListViewSet):
    Project.objects.all().count()
    model = Project
    template_name = 'api/project.html'
    paginate_by = 10

    def get_queryset(self):
        name = None
        try:
            name = self.request.GET['keyword']
        except:
            pass

        if name:
            return self.model.objects.filter(name__icontains=name)
        else:
            return self.model.objects.all()

class Mission_CreateViewSet(Base_CreateViewSet):
    model = Mission
    form_class = forms.MissionFrom
    template_name = 'api/mission_form.html'
    success_url = reverse_lazy('mission-list')

class Mission_ListViewSet(Base_ListViewSet):
    Mission.objects.all().count()
    model = Mission
    template_name = 'api/mission.html'
    paginate_by = 10

    def get_queryset(self):
        name = None
        try:
            name = self.request.GET['keyword']
        except:
            pass

        if name:
            return self.model.objects.filter(project__name__icontains=name)
        else:
            return self.model.objects.all()

class Version_historyViewSet(Base_ListViewSet):
    Version_history.objects.all().count()
    model = Version_history
    template_name = 'api/version.html'
    paginate_by = 10

    def get_queryset(self):
        name = None
        try:
            name = self.request.GET['keyword']
        except:
            pass

        if name:
            return self.model.objects.filter(project__name__icontains=name)
        else:
            return self.model.objects.all()

# class Progress_ViewSet(Base_ListViewSet):
#     Progress.objects.all().count()
#     model = Progress
#     template_name = 'api/progress.html'
#     paginate_by = 10
#
#     def get_queryset(self):
#         name = None
#         try:
#             name = self.request.GET['keyword']
#         except:
#             pass
#
#         if name:
#             return self.model.objects.filter(mission__id=name)
#         else:
#             return self.model.objects.all()

def run_job(req,job_id):
    if req.user.is_authenticated():
        mission=Mission.objects.get(id=job_id)
        if mission.status.name=='undo':
            mission.status=Status.objects.get(name='in_queue')
            mission.save()
            MissionTask().apply_async(args=(job_id,)) ## 调用后台任务
            response = redirect('mission-list')
        else:
            response=HttpResponseBadRequest('this job is already done or processing')
    else:
        response =redirect('login')
    return response
#
def reset_job(req,job_id):
    if req.user.is_authenticated():
        mission=Mission.objects.get(id=job_id)
        mission.status=Status.objects.get(name='undo')
        mission.save()
        # Progress.objects.filter(mission=mission).update(status=Status.objects.get(name='undo'))
        response = redirect('mission-list')
    else:
        response =redirect('login')
    return response


@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
def mission_run_view(req):
    project_name = req.GET.get('project')
    version = req.GET.get('version')
    if Project.objects.filter(name=project_name).__len__() == 0:
        response = HttpResponseBadRequest(json.dumps(get_result(1, 'project not existed {0}'.format(project_name))))
    else:
        project=Project.objects.filter(name=project_name)[0]
        if Version_history.objects.filter(project=project,version=version).__len__()==0:
            response = HttpResponseBadRequest(json.dumps(get_result(1, 'not ready to publish: not existed {0}:{1} maybe do not pass the jenkins'.format(project_name,version))))
        else:
            mission_status = [x.status.name for x in Mission.objects.filter(project=project, version=version)]
            if 'processing' in mission_status or 'in_queue' in mission_status:
                response=HttpResponseBadRequest(json.dumps(get_result(1,'this job is already done or processing')))
            else:
                mission=Mission.objects.create(project=project,version=version,status=Status.objects.get(name='undo'))
                mission.status=Status.objects.get(name='in_queue')
                mission.save()
                MissionTask().apply_async(args=(mission.id,)) ## 调用后台任务
                response = HttpResponse(json.dumps(get_result(0,'add to queue')))
    return response


@api_view(['GET','POST' ])
@permission_classes([IsAuthenticated, ])
def versioin_console_view(req):
    if req.method=='GET':
        project_name = req.GET.get('project')
        if Project.objects.filter(name=project_name).__len__()==0:
            response=HttpResponseBadRequest(json.dumps(get_result(1, 'project not existed {0}'.format(project_name))))
        else:
            project=Project.objects.filter(name=project_name)[0]
            result = [{'project': project, "version": x.version, "status": x.status.name, } for x in
                      Version_history.objects.filter(project=Project.objects.get(name=project))]
            response = HttpResponse(json.dumps(result))
    elif req.method=='POST':
        project_name=req.POST.get('project')
        version=req.POST.get('version')
        if Project.objects.filter(name=project_name).__len__() == 0:
            response=HttpResponseBadRequest(json.dumps(get_result(1, 'project not existed {0}'.format(project_name))))
        else:
            project=Project.objects.filter(name=project_name)[0]
            if Version_history.objects.filter(project=project,version=version).__len__()==0:
                Version_history.objects.create(project=project,version=version,status=Status.objects.get(name='standby'))
                response=HttpResponse(json.dumps(get_result(0,'add to  version history')))
            else:
                response=HttpResponseBadRequest(json.dumps(get_result(2,'already add to version history')))
    else:
        response = HttpResponseBadRequest(json.dumps(get_result(1, 'not allowed')))
    return response
