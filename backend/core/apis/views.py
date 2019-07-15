# -*- coding:UTF-8 -*-
"""
 * @Description:   公共组件业务视图逻辑.
 * @author:        wuzechuan
 * @version:       V1.0
 * @Date:          2018/04/13
"""

import time

from django.conf import settings
from django.http import StreamingHttpResponse, HttpResponse
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import parsers, renderers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework.generics import GenericAPIView
from rest_framework.filters import SearchFilter
from rest_framework.decorators import permission_classes
from rest_framework.decorators import detail_route, list_route
from rest_framework.authtoken.models import Token

from backend.core.apis.pagination import ChildPagination
from backend.core.models import ProjectManage, VersionManage, ModuleManage, UserProfile
from backend.core.apis.filters import ProjectManageFilter, VersionManageFilter, ModuleManageFilter
from backend.core.apis.serializers import (UserSerializer, ProjectManageSerializer, ModuleManageSerializer,
                                            VersionManageSerializer)

__all__ = [
    'ObtainAuthToken',
    'ProjectManageViewSet',
    'ModuleManageViewSet',
    'VersionManageViewSet'
]


class ObtainAuthToken(APIView):
    """ 获取登录token  """
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)

    def post(self, request, *args, **kwargs):
        username = request.data.get('username').strip()
        password = request.data.get('password')
        # newPassword = Utils().encryption(password)
        user = authenticate(username=username, password=password)
        if username != 'admin':
            projects = UserProfile.objects.get(user__username=username).projectset
            projects = ProjectManage.objects.filter(id__in=list(map(int, projects.split(','))))
            projectset = []
            for p in projects:
                projectset.append(p.name)
            userId = UserProfile.objects.get(user__username=username).user_id
        else:
            projectset = []
            userId = ''
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'status': True, 'token': token.key, 'username': username,
                            'projectset': projectset, 'userId': str(userId)})
        else:
            return Response({'status': False, 'message': 'Unable to log in with provided credentials'})

class ProjectManageViewSet(viewsets.ModelViewSet):
    """ 项目管理视图 """
    permission_classes = ()
    queryset = ProjectManage.objects.all().order_by('id')
    serializer_class = ProjectManageSerializer
    filter_backends = (SearchFilter, DjangoFilterBackend)
    filter_class = ProjectManageFilter

    def create(self, request, *args, **kwargs):
        # 将platform_set列表转化为字符串
        platform_set = ",".join(list(map(str, request.data.get('platform_set'))))
        request.data['platform_set'] = platform_set
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        platform_set = ",".join(list(map(str, request.data.get('platform_set'))))
        request.data['platform_set'] = platform_set
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    @list_route(methods=['get'], permission_classes=(permissions.IsAuthenticatedOrReadOnly,))
    def get_project_list(self, request, pk=None):
        """ 根据是否有project_name字段返回相应的项目列表 """
        if request.GET.get('project_name'):
            if ',' in request.GET.get('project_name'):
                project_name = request.GET.get('project_name').split(',')
                projects = ProjectManage.objects.filter(name__in=project_name)
            else:
                projects = ProjectManage.objects.filter(name=request.GET.get('project_name'))
        else:
            projects = ProjectManage.objects.all().order_by('id')
        project_list = []
        for p in projects:
            item = {'id': p.id, 'name': p.name}
            projectList.append(item)
        return Response({'status': True, 'data': project_list})

    def list(self, request, *args, **kwargs):
        projects = ProjectManage.objects.all().order_by('id')
        project_list = []
        for p in projects:
            # 将平台类型从字符串切割为列表形式
            item = {'id': p.id, 'name': p.name, 'platform_set': p.platform_set.split(',')}
            project_list.append(item)
        data = self.paginate_queryset(project_list)
        if data is not None:
            return self.get_paginated_response(data) 
        return Response({'status': False, 'msg': 'Nothing can matches.'})

class VersionManageViewSet(viewsets.ModelViewSet):
    """ 版本管理接口 """
    permission_classes = ()
    queryset = VersionManage.objects.all().order_by('-id')
    serializer_class = VersionManageSerializer
    pagination_class = ChildPagination
    filter_class = VersionManageFilter

    @list_route(methods=['get'])
    def get_all_version(self, request):
        """ 获取当前项目所有版本 """
        project_id = request.GET.get('project_id')
        versions = VersionManage.objects.filter(project=project_id).order_by('id')

        version_list = []
        for v in versions:
            item = {'id': v.id, 'name': v.name}
            version_list.append(item)
        return Response({'status': False, 'results': version_list})

    def destroy(self, request, *args, **kwargs):
        """ 删除版本过程中监测是否被其他功能模块占用  """
        instance = self.get_object()
        case = case_manage.objects.filter(version=instance.id)
        flow = flow_manage.objects.filter(version=instance.id)
        task = task_manage.objects.filter(version=instance.id)
        if len(case) > 0 or len(flow) > 0 or len(case) > 0:
            return Response({'status': False, 'message': '该版本有在相关功能模块使用中,无法删除!'})
        else:
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)

class ModuleManageViewSet(viewsets.ModelViewSet):
    """ 模块管理接口 """
    permission_classes = ()
    queryset = ModuleManage.objects.all().order_by('-id')
    serializer_class = ModuleManageSerializer
    pagination_class = ChildPagination
    filter_class = ModuleManageFilter
        
    @list_route(methods=['get'])
    def get_all_module(self, request):
        """ 获取当前项目所有模块 """
        project_id = request.GET.get('project_id')
        modules = ModuleManage.objects.filter(project=project_id).order_by('id')

        module_list = []
        for m in modules:
            item = {'id': m.id, 'name': m.name}
            module_list.append(item)
        return Response({'status': False, 'results': module_list})

    def destroy(self, request, *args, **kwargs):
        """ 删除模块过程中监测是否被其他功能模块占用  """
        instance = self.get_object()
        case = case_manage.objects.filter(module=instance.id)
        flow = flow_manage.objects.filter(module=instance.id)
        if len(case) > 0 or len(flow) > 0:
            return Response({'status': False, 'message': '该版本有在相关功能模块使用中,无法删除!'})
        else:
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
