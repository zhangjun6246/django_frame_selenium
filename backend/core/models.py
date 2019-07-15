# -*- coding:utf-8 -*-
from django.db import models
from django.contrib.auth.models import User, Group


class ModelUserMixin(models.Model):
    """ User field mixin. """
    creator = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL,
                related_name='creator_%(class)s', editable=False)
    modifier = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL,
                related_name='modifier_%(class)s', editable=False)

    class Meta:
        abstract = True

class ModelDateMixin(models.Model):
    """ Data time field mixin. """
    create_time = models.DateTimeField(editable=False, auto_now_add=True)
    update_time = models.DateTimeField(editable=False, auto_now=True)

    class Meta:
        abstract = True

class ProjectManage(models.Model):
    """ 项目管理 """
    name = models.CharField(max_length=50, unique=True, verbose_name='项目名称')
    platform_set = models.CharField(max_length=50, verbose_name='平台类型集合')

    class Meta:
        ordering = ('name',)
        verbose_name = '项目管理'
        verbose_name_plural = verbose_name

class UserProfile(models.Model):
    """ 基于User表补充的用户信息 """
    phone = models.CharField(max_length=50, blank=True, null=True, verbose_name='电话')
    rtx_id = models.CharField(max_length=50, blank=True, verbose_name='rtxID')
    project_set = models.TextField(blank=True, null=True, verbose_name="项目id集合")
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)

class VersionManage(models.Model):
    """ 版本管理 """
    name = models.CharField(max_length=20, verbose_name='版本名称')
    project = models.ForeignKey(ProjectManage, null=True, on_delete=models.SET_NULL, related_name='versions')
    platform = models.CharField(max_length=20, blank=True, null=True, verbose_name='平台类型')
    comment = models.CharField(max_length=200, blank=True, null=True, verbose_name="版本备注")

    class Meta:
        unique_together = (("project", "name", "platform"),)
        ordering = ('name',)
        verbose_name = '版本管理'
        verbose_name_plural = verbose_name

class ModuleManage(models.Model):
    """ 模块管理 """
    name = models.CharField(max_length=100)
    project = models.ForeignKey(ProjectManage, null=True, on_delete=models.SET_NULL, related_name='modules')
    platform = models.CharField(max_length=20, blank=True, null=True, verbose_name='平台类型')

    class Meta:
        unique_together = (("project", "name", "platform"),)
        ordering = ('name',)
        verbose_name = '模块管理'
        verbose_name_plural = verbose_name

class DataTemplateManage(ModelUserMixin, ModelDateMixin):
    """ 数据模版管理 """
    project = models.ForeignKey(ProjectManage, null=True, on_delete=models.SET_NULL, verbose_name="项目名称")
    name = models.CharField(max_length=50, verbose_name="数据模版名称")
    platform = models.CharField(max_length=20, blank=True, null=True, verbose_name='平台类型')
    env = models.CharField(max_length=50, default='test', verbose_name="环境名称")
    is_enable = models.BooleanField(default=True, verbose_name="是否启用")

    class Meta:
        unique_together = (("project", "name", "env", "platform", "creator"),)
        ordering = ('name', )
        verbose_name = '数据模版名称'
        verbose_name_plural = verbose_name

class DataDetail(models.Model):
    """ 数据详情 """
    dt = models.ForeignKey(DataTemplateManage, null=True, on_delete=models.SET_NULL, verbose_name="数据模版名称")
    module = models.ForeignKey(ModuleManage, null=True, on_delete=models.SET_NULL, verbose_name="模块名称")
    name = models.CharField(max_length=50, verbose_name="数据名称")
    data_type = models.CharField(max_length=20, verbose_name="数据类型")
    value = models.TextField(verbose_name="数据对应的值")
    comment = models.CharField(max_length=200, blank=True, null=True, verbose_name="数据备注")

    class Meta:
        unique_together = (("dt", "module", "name"),)

class TaskManage(ModelUserMixin, ModelDateMixin):
    """ 任务管理 """
    project = models.ForeignKey(ProjectManage, null=True, on_delete=models.SET_NULL, verbose_name="项目名称")
    platform = models.CharField(max_length=20, blank=True, null=True, verbose_name='平台类型')
    version = models.ForeignKey(VersionManage, blank=True, null=True, on_delete=models.SET_NULL, verbose_name="版本号")
    push_grp = models.TextField(null=True, blank=True, verbose_name="推送组集合")
    case_set = models.TextField(null=True, blank=True,verbose_name="用例集合")
    name = models.CharField(max_length=50, verbose_name="任务名称")
    is_enable = models.BooleanField(default=True, verbose_name="是否启用")
    status = models.CharField(max_length=20, default='Ready', verbose_name="任务运行状态")

    class Meta:
        unique_together = (("project", "name", "platform"),)
        ordering = ('name',)
        verbose_name = '任务管理'
        verbose_name_plural = verbose_name

class PushManage(models.Model):
    """ 推送管理 """
    name = models.CharField(max_length=50, verbose_name="推送组名称")
    selected_type = models.CharField(max_length=50, verbose_name="推送类型")
    project = models.ForeignKey(ProjectManage, null=True, on_delete=models.SET_NULL, verbose_name="项目名称")
    platform = models.CharField(max_length=20, blank=True, null=True, verbose_name='平台类型')

    class Meta:
        unique_together = (("project", "name", "platform"),)
        ordering = ('name',)
        verbose_name = '推送组名称'
        verbose_name_plural = verbose_name

class PushMember(models.Model):
    """ 推送组成员 """
    push_grp = models.ForeignKey(PushManage, blank=True, null=True, on_delete=models.CASCADE, verbose_name="推送组")
    user_set = models.TextField(blank=True, null=True, verbose_name="用户id集合")

class EnvManage(models.Model):
    """ 环境管理 """
    name = models.CharField(max_length=50, verbose_name="环境名称")
    host = models.CharField(max_length=50, verbose_name="域名/IP地址")
    project = models.ForeignKey(ProjectManage, null=True, on_delete=models.SET_NULL, verbose_name="项目名称")
    platform = models.CharField(max_length=20, blank=True, null=True, verbose_name='平台类型')

    class Meta:
        unique_together = (("project", "name", "platform"),)
        ordering = ('name',)
        verbose_name = '环境名称'
        verbose_name_plural = verbose_name
