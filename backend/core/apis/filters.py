# coding -*- utf-8 -*-
"""
 * @Description:   公共组件模块过滤.
 * @author:        wuzechuan
 * @version:       V1.0
 * @Date:          2018/04/13
"""

import django_filters

from backend.core.models import ProjectManage, VersionManage, ModuleManage

class ProjectManageFilter(django_filters.rest_framework.FilterSet):
    """ 项目管理模块过滤  """
    name = django_filters.CharFilter(name='name')

    class Meta:
        model = ProjectManage
        fields = ['name']

class VersionManageFilter(django_filters.rest_framework.FilterSet):
    """ 版本管理模块过滤  """
    project_id = django_filters.NumberFilter(name='project_id')
    platform = django_filters.CharFilter(name='platform')

    class Meta:
        model = VersionManage
        fields = ['name', 'platform']

class ModuleManageFilter(django_filters.rest_framework.FilterSet):
    """ 模块管理模块过滤  """
    project_id = django_filters.NumberFilter(name='project_id')
    platform = django_filters.CharFilter(name='platform')

    class Meta:
        model = ModuleManage
        fields = ['name', 'platform']
