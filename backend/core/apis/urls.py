# -*- coding: utf-8 -*-

from django.urls import path, include, re_path
from rest_framework import routers
from rest_framework_swagger.views import get_swagger_view

from backend.core.apis.views import *
from backend.ui_manage.apis.views.pc_wap import *

schema_view = get_swagger_view(title='GATP API')

router = routers.DefaultRouter()
router.register(r'projects', ProjectManageViewSet)
router.register(r'modules', ModuleManageViewSet)
router.register(r'versions', VersionManageViewSet)
router.register(r'svnmange', SvnPathViewSet)
router.register(r'jenkinscreate',jenkinsCreateViewSet)
urlpatterns = {
    path('api-token-auth/', ObtainAuthToken.as_view()),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    re_path('^', include(router.urls)),
    path('api/docs/', schema_view, name='swagger')
}
