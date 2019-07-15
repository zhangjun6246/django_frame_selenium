# -*- coding:utf-8 -*-
from django.db import models
from backend.core.models import ModelDateMixin, ModelUserMixin, ProjectManage, VersionManage, ModuleManage


# class ApiManage(ModelUserMixin, ModelDateMixin):
#     """ Api管理 """
#     name = models.CharField(max_length=50, verbose_name="接口名称")
#     project = models.ForeignKey(ProjectManage, null=True, on_delete=models.SET_NULL, verbose_name="项目名称")
#     env = models.ForeignKey(EnvManage, null=True, max_length=20, on_delete=models.SET_NULL, verbose_name="环境名称")
#     platform = models.CharField(max_length=20, blank=True, null=True, verbose_name='平台类型')

#     module = models.ForeignKey(ModuleManage, null=True, on_delete=models.SET_NULL, verbose_name="模块名称")
#     version = models.ForeignKey(VersionManage, null=True, on_delete=models.SET_NULL, verbose_name="版本名称")
#     urlDocAddr = models.CharField(max_length=100, null=True, verbose_name="接口文档地址")

#     url = models.CharField(max_length=100, null=True, verbose_name="接口地址")
#     method = models.CharField(max_length=10, verbose_name="方法名称")
#     header = models.TextField(null=True, verbose_name="请求头")
#     tests = models.TextField(null=True, verbose_name="接口测试集")

#     def __unicode__(self):
#         return self.name

#     class Meta:
#         unique_together = (("project", "name", "platform"),)
#         ordering = ('update_time',)
#         verbose_name = 'Api管理'
#         verbose_name_plural = verbose_name
