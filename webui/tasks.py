#coding=utf-8
from celery import Task as T
from core.common import logger,ANSRunner
from api.models import Mission,Version_history,Status
import time

class BaseTask(T):
    error_info = None
    logger = logger

    def init(self, *args, **kwargs):
        pass

    def run(self, *args, **kwargs):
        pass

class MissionTask(BaseTask):
    error_info = None
    success_info = None
    exec_id, todo_mission = None, None
    mission = None

    def init(self, exec_id):
        self.exec_id = exec_id
        self.mission = Mission.objects.get(id=exec_id)
        self.mission.status = Status.objects.get(name='processing')
        self.mission.save()
        super(MissionTask, self).init()

    def run(self, exec_id):
        self.init(exec_id=exec_id)
        if self.mission.project.type=='php':
            playbook_path='/home/admin/scripts/t.yml'
        else:
            playbook_path = '/home/admin/scripts/t.yml'
        resource = [{"hostname": x.name,"username": "admin", "password": "admin@eju"} for x in self.mission.project.host_list.all()]
        rbt = ANSRunner(resource)
        rbt.run_playbook(
            playbook_path=playbook_path,
            extra_vars={
                "host": [x.name for x in self.mission.project.host_list.all()],
                "project": self.mission.project.name,
                "version": self.mission.version
            }
        )
        result_data = rbt.get_playbook_result()
        logger.info({"resource":resource,"result":result_data,"exec_id":exec_id})
        publish_status=True
        if result_data.get('failed'):
            publish_status=False
        if result_data.get('skipped'):
            publish_status = False
        if result_data.get('unreachable'):
            publish_status = False

        if publish_status:
            self.mission.status=Status.objects.get(name='done')
            self.mission.save()
            Version_history.objects.filter(project=self.mission.project,status=Status.objects.get(name='current')).update(status=Status.objects.get(name='release'))
            change_version=Version_history.objects.get(project=self.mission.project,version=self.mission.version)
            change_version.status=Status.objects.get(name='current')
            change_version.save()
        else:
            logger.error(result_data)
            self.mission.status=Status.objects.get(name='failed')
            self.mission.result=result_data
            self.mission.save()

# {'status': {'10.120.180.3': {'unreachable': 0, 'skipped': 0, 'changed': 1, 'ok': 4, 'failed': 0}, '10.120.180.2': {'unreachable': 0, 'skipped': 0, 'changed': 1, 'ok': 4, 'failed': 0}},
#  'failed': {},
#  'skipped': {},
#  'ok': {'10.120.180.3': {'_ansible_no_log': False, 'stdout': u'ln: failed to create symbolic link \u2018/home/admin/app-run/dc.17shihui.com\u2019: Permission denied\r\ndone\r\n', 'changed': True, 'stderr': u'Shared connection to 10.120.180.3 closed.\r\n', 'rc': 0, 'stdout_lines': [u'ln: failed to create symbolic link \u2018/home/admin/app-run/dc.17shihui.com\u2019: Permission denied', u'done']}, '10.120.180.2': {'_ansible_no_log': False, 'stdout': u'done\r\n', 'changed': True, 'stderr': u'Shared connection to 10.120.180.2 closed.\r\n', 'rc': 0, 'stdout_lines': [u'done']}},
#  'unreachable': {}}