# -*- coding:utf-8 -*-
"""
 * @Description:   公共组件接口序列化.
 * @author:        wuzechuan
 * @version:       V1.0
 * @Date:          2018/04/13
"""

import time

from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import User, Group
from rest_framework import serializers

from backend.core.models import ProjectManage, VersionManage, ModuleManage, UserProfile

__all__ = [
    'UserSerializer',
    'ProjectManageSerializer',
    'ModuleManageSerializer',
    'VersionManageSerializer'
]


class UserSerializer(serializers.ModelSerializer):
    """ 用户表序列化, User表与UserProfile表关联 """
    phone = serializers.CharField(source='userprofile.phone', allow_blank=True, required=False)
    rtx_id = serializers.CharField(source='userprofile.rtx_id', required=True)
    project_set = serializers.CharField(source='userprofile.project_set', required=True)
    password = serializers.CharField(write_only=True, required=False)
    username = serializers.CharField(required=False)

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.first_name = validated_data['first_name']
        # 邮箱 = 用户名 + settings.EMAIL_SUFFIX, eg. admin@globalegrow.com
        user.email = validated_data['username'] + settings.EMAIL_SUFFIX
        userprofile = UserProfile.objects.create(user=user, rtx_id=validated_data.get('userprofile').get('rtxId'),
                                                 project_set=validated_data.get('userprofile').get('projectset'))
        user.save()
        return user

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.email = validated_data.get('email', instance.email)
        instance.userprofile.phone = validated_data.get('userprofile').get('phone')
        instance.userprofile.rtx_id = validated_data.get('userprofile').get('rtx_id')
        instance.userprofile.project_set = validated_data.get('userprofile').get('project_set')
        instance.date_joined = timezone.now()
        instance.save()
        instance.userprofile.save()
        return instance
    
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'email', 'phone', 'rtx_id', 'password', 'project_set')

class ProjectManageSerializer(serializers.ModelSerializer):
    """ 项目管理序列化 """

    class Meta:
        model = ProjectManage
        fields = ('id', 'name', 'platform_set')

class ModuleManageSerializer(serializers.ModelSerializer):
    """ 模块管理序列化 """

    class Meta:
        model = ModuleManage
        fields = ('id', 'name', 'project', 'platform')

class VersionManageSerializer(serializers.ModelSerializer):
    """ 版本管理序列化 """
    
    class Meta:
        model = VersionManage
        fields = ('id', 'name', 'project', 'platform')
