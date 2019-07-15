# -*- coding:utf-8 -*-

"""
 * @Description:   ui自动化平台前端视图
 * @author:        lujun
 * @version:       V1.0
 * @Date:          2018/04/19
"""
from rest_framework.views import APIView
from backend.ui_manage.apis.serializers import SvnPathSerializer
from backend.ui_manage.models import SvnPath
from backend.core.models import ProjectManage
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import detail_route, list_route
from backend.ui_manage.models import  UICase
from backend.ui_manage.libs.pc_wap.jenkins_create import jenkinsCreateJob

__all__ = {'SvnPathViewSet',
           'jenkinsCreateViewSet'}


class SvnPathViewSet(viewsets.ModelViewSet):
    """SVN 存储表视图"""
    queryset = SvnPath.objects.all()
    serializer_class = SvnPathSerializer
    permission_classes = ()

    @list_route(methods=['get'])
    def get_svnurl(self, request, pk=None):
        """ 根据 project_name 字段查询对应的 SVN 信息 """
        if request.GET.get('project_name'):
            param_projectname = request.GET.get('project_name')
            # 项目管理表查询项目是否已创建
            project_exist = ProjectManage.objects.filter(name=param_projectname)
            if len(project_exist) == 0:
                return Response({'status': True, 'code': 1001, 'data': u'项目不存在,请先创建项目!'})
            # 查询项目SVN地址是否已创建
            svn = SvnPath.objects.filter(project__name=param_projectname)
            # 项目svn地址不存在
            if len(svn) == 0:
                return Response({'status': True, 'code': 1001, 'data': u'现在创建!'})
            # 项目svn地址已存在 
            url_list = []
            if len(svn) != 0:
                for p in svn:
                    item = {'project_url':p.url}
                    url_list.append(item)
                return Response({'status': True, 'code': 1000, 'data': url_list})
        return Response({'status': False, 'code': 1003, 'data': u'传入参数有误!'})

class jenkinsCreateViewSet(viewsets.ModelViewSet):

    serializer_class = SvnPathSerializer

    @list_route(methods=['get'])
    def get(self, request, format=None):
        name=request.GET.get('name')
        platform_set=request.GET.get('platform_set')
        id=ProjectManage.objects.get(name=name,platform_set=platform_set).id
        print("显示为:",id)
        user = request.GET.get('user')
        testng_xml = request.GET.get('testng_xml')
        #判断testng是否已存再数据库中
        character=","
        job_list=character in testng_xml
        jenkins_create=jenkinsCreateJob()
        global get_xmlname
        #处理多个xml
        if job_list==True:
            get_jobname=job_list.split(character)
            print(get_jobname)
            for data in get_jobname:
                testng_xml = UICase.objects.get(project=id, testng_xml=data).testng_xml
                if len(testng_xml)==0:#文件不存在
                    jenkins_create.svn_list('platform_set','name')
                    get_xmlname.append(testng_xml)
            jenkins_create.create_jenkinsjob(name,platform_set,get_xmlname)
        else:
            jenkins_create.create_jenkinsjob(name,platform_set,testng_xml)









    

    
