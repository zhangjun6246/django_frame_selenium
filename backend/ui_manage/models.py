# -*- coding:utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from backend.core.models import ModelDateMixin, ModelUserMixin, ProjectManage, VersionManage, ModuleManage, TaskManage


class PageManage(ModelUserMixin, ModelDateMixin):
    """ 公共表,页面管理 """
    version = models.ForeignKey(VersionManage, null=True, on_delete=models.SET_NULL, verbose_name="版本号")
    module = models.ForeignKey(ModuleManage, null=True, on_delete=models.SET_NULL, verbose_name="模块名称")
    platform = models.CharField(max_length=20, blank=True, null=True, verbose_name='平台类型')
    project = models.ForeignKey(ProjectManage, null=True, on_delete=models.SET_NULL, verbose_name="项目名称")
    name = models.CharField(max_length=50, verbose_name='页面名称')

    class Meta:
        unique_together = (("project", "version","module", "name"),)
        ordering = ('name', )
        verbose_name = '页面管理'
        verbose_name_plural = verbose_name

class ElementManage(models.Model):
    """ 公共表,元素管理 """
    page = models.ForeignKey(PageManage, null=True, on_delete=models.SET_NULL, verbose_name="页面名称")
    element = models.CharField(max_length=100, verbose_name='元素对象')
    find_type = models.CharField(max_length=30, default='id', verbose_name='查找方式')
    content = models.CharField(max_length=100, verbose_name="元素内容")
    comment = models.TextField(blank=True, null=True, verbose_name="元素备注")

    class Meta:
        unique_together = (("page", "element", "find_type"),)
        ordering = ('element', )
        verbose_name = '元素对象'
        verbose_name_plural = verbose_name

class SvnPath(models.Model):
    """ ui表,存储svn地址 """
    url = models.CharField(max_length=150, unique=True, verbose_name='url地址')
    project = models.ForeignKey(ModuleManage, null=True, on_delete=models.SET_NULL, verbose_name="项目名称")
    
class UICase(ModelUserMixin, ModelDateMixin):
    """ ui表,测试用例表 """
    xml_comment = models.CharField(max_length=100, verbose_name='xml描述')
    name = models.CharField(max_length=50, verbose_name='用例名称')
    testng_xml = models.CharField(max_length=50, verbose_name='导入的xml文件')
    jenkins_url = models.TextField(blank=True, null=True, verbose_name="jenkins的url")
    status = models.CharField(max_length=100, verbose_name='运行状态(运行中、编译失败等)')
    project = models.ForeignKey(ProjectManage, null=True, on_delete=models.SET_NULL, verbose_name="项目名称")
    task = models.ForeignKey(TaskManage, null=True, on_delete=models.SET_NULL, verbose_name="任务名称")

    class Meta:
        unique_together = (("project", "name", "task"),)
        ordering = ('name', )
        verbose_name = '用例名称'
        verbose_name_plural = verbose_name

class UITestResult(ModelDateMixin):
    """ ui表,测试结果表  """
    job_name = models.CharField(max_length=50, verbose_name='测试方法名称')
    case = models.ForeignKey(UICase, null=True, on_delete=models.SET_NULL, verbose_name="用例名称")
    module = models.ForeignKey(ModuleManage, null=True, on_delete=models.SET_NULL, verbose_name="模块名称")
    job = models.CharField(max_length=50, verbose_name='任务job名')
    excutor = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, verbose_name="执行人")
    start_time = models.DateTimeField(editable=True, null=True, verbose_name="开始时间")
    end_time = models.DateTimeField(editable=True, null=True, verbose_name="开始时间")
    result = models.CharField(max_length=20, verbose_name='用例运行结果')
    times = models.CharField(max_length=10, verbose_name='任务id(运行次数)')
    os = models.CharField(max_length=10, verbose_name='操作系统')
    excute_platform = models.CharField(max_length=20, verbose_name='运行平台')
    log_id = models.CharField(max_length=50, verbose_name='mongo日志id')

class UICaseStep(models.Model):
    """ ui表,测试用例步骤表  """
    test_result = models.ForeignKey(UITestResult, null=True, on_delete=models.SET_NULL, verbose_name="用例名称")
    name = models.CharField(max_length=50, verbose_name='用例名称')
    code = models.CharField(max_length=50, verbose_name='用例code')
    comment = models.TextField(blank=True, null=True, verbose_name="用例描述")
    step = models.TextField(blank=True, null=True, verbose_name="执行步骤")
    check_point = models.TextField(blank=True, null=True, verbose_name="检查点")

class UITestStepResult(models.Model):
    """ ui表,测试步骤结果表 """
    test_result = models.ForeignKey(UITestResult, null=True, on_delete=models.SET_NULL, verbose_name="测试结果id")
    img_path = models.TextField(blank=True, null=True, verbose_name="存储错误图片地址")
    video_path = models.TextField(blank=True, null=True, verbose_name="存储视频地址")
    log_id = models.CharField(max_length=50, verbose_name='mongo日志id')
    result = models.CharField(max_length=20, verbose_name='步骤运行结果') 

class DeviceManage(ModelDateMixin):
    """ app表,设备管理 """
    name = models.CharField(max_length=50, verbose_name='设备名称')
    device_id = models.CharField(max_length=30, unique=True, verbose_name='设备id')
    brand = models.CharField(max_length=20, verbose_name='设备品牌')
    phone_model = models.CharField(max_length=50, verbose_name='设备机型')
    phone_sys_ver = models.CharField(max_length=100, verbose_name='设备系统版本')
    cpu_info = models.CharField(max_length=30, verbose_name='设备cpu核数')
    mem_info = models.CharField(max_length=50, verbose_name='设备内存信息')
    image_link = models.CharField(max_length=100, verbose_name='设备图片地址')
    resolution_info = models.CharField(max_length=20, verbose_name='设备分辨率')
    wireless_ip = models.CharField(unique=True, max_length=30, verbose_name='ip地址')
    wireless_port = models.IntegerField(verbose_name='无线端口')
    status = models.CharField(max_length=20, default='Ready')
    run_info = models.CharField(max_length=50, blank=True, null=True, verbose_name='执行任务信息')
