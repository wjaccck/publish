#coding=utf-8
from __future__ import unicode_literals

from django.db import models
from abstract.models import CommonModel,UniqueNameDescModel,ITEM_BASE,PUBLISH_BASE


class Ipv4Address(UniqueNameDescModel):

    class Meta:
        ordering = ['name', ]

class Ipv4Network(UniqueNameDescModel):
    gateway = models.CharField(max_length=18, null=True)

    class Meta:
        ordering = ['name', ]


class Status(CommonModel,PUBLISH_BASE):
    name=models.CharField(max_length=25,unique=True)

    def __unicode__(self):
        return self.name
    @staticmethod
    def verbose():
        return u'状态'

class Project(CommonModel,PUBLISH_BASE):
    name=models.CharField(max_length=50,unique=True)
    build_name=models.CharField(max_length=50,unique=True)
    type=models.CharField(max_length=50)
    host_list=models.ManyToManyField(Ipv4Address,related_name='project_host')

    @staticmethod
    def verbose():
        return u'项目信息'
    def __unicode__(self):
        return self.name

class Mission(CommonModel,PUBLISH_BASE):
    project=models.ForeignKey(Project,verbose_name=u'发布项目',related_name='project_mission')
    version=models.CharField(max_length=100,default='default')
    status=models.ForeignKey(Status)
    result=models.TextField(blank=True)
    @staticmethod
    def verbose():
        return u'发布任务'
    def __unicode__(self):
        return "{0}-{1}".format(self.project.name,self.version)

# class Progress(CommonModel,PUBLISH_BASE):
#     mission=models.ForeignKey(Mission)
#     host=models.ForeignKey(Ipv4Address)
#     status=models.ForeignKey(Status)
#     result=models.TextField(blank=True)
#     @staticmethod
#     def verbose():
#         return u'发布任务单条'

class Version_history(CommonModel, PUBLISH_BASE):
    project = models.ForeignKey(Project, related_name='project_version')
    version = models.CharField(max_length=10,default='default')
    file_name = models.CharField(max_length=50)
    file_md5 = models.CharField(max_length=50)
    status = models.ForeignKey(Status)
    commit_id = models.CharField(max_length=100)
    download_url = models.CharField(max_length=100)

    @staticmethod
    def verbose():
        return u'版本历史'