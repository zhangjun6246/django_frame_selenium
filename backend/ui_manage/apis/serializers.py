# -*- coding:utf-8 -*-
"""
 * @Description:   ui平台序列化
 * @author:        lujun
 * @version:       V1.0
 * @Date:          2018/04/10
"""

from rest_framework import serializers
from backend.ui_manage.models import SvnPath,UICase

__all__ = [
    'SvnPathSerializer',
    'JenkinsCreateSerializer'
]

class SvnPathSerializer(serializers.ModelSerializer):
    """SVN 地址存储表序列化"""

    class Meta:
        model = SvnPath
        fields = ('id', 'url', 'project')

class  JenkinsCreateSerializer(serializers.ModelSerializer):
    """jenkinsjob创建"""
    class Meta:
        module=UICase
        fields = ('id', 'xml_comment ', 'name','testng_xml','jenkins_url','status','project','task')
