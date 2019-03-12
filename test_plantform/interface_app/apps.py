from django.apps import AppConfig
from test_plantform.settings import BASE_DIR

class InterfaceAppConfig(AppConfig):
    name = 'interface_app'

# 配置目录
TASK_PATH = BASE_DIR.replace("\\","/") + "/resource/tasks/"
# 运行目录
RUN_TASK_FILE = BASE_DIR.replace("\\","/") + "/interface_app/extend/run_task.py"