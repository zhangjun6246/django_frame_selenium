# -*- coding:utf-8 -*-
from __future__ import print_function



from jenkinsapi.jenkins import Jenkins
from jenkinsapi.utils.crumb_requester import CrumbRequester
import subprocess
import sys
import os
import pymysql.cursors




jenkins_url = 'http://10.40.2.192:9018/jenkins/'
jenkins_user = 'admin'
jenkins_password = '123'

get_xmlname=[]
project_manage_result={}
class jenkinsCreateJob(object):
    '''
    def __init__(self, projectid, xmlid):
        self.projectid = projectid
        self.xmlid = xmlid
    '''
    def connet_jenkinsjob(self):   #连接Jenkins的job
        jenkins = Jenkins(jenkins_url, username=jenkins_user, password=jenkins_user,
                          requester=CrumbRequester(username=jenkins_user, password=jenkins_password,
                                                   baseurl=jenkins_url))
        return jenkins

    def connet_mysql(self ):#获取xml文件，把他转换成map
     """
        '''
       global  project_manage_result
       global  get_xmlname
       cf = ConfigParser.ConfigParser()
       cf.read(os.path.dirname(os.path.dirname(__file__)) + "/dbconfig.ini")
       print("地址111:", (os.path.dirname(os.path.dirname(__file__)) + "/dbconfig.ini"))
       connection = pymysql.connect(host=cf.get('mysql', "host"), port=int(cf.get('mysql', "port")),
                                    user=cf.get('mysql', "user"), passwd=cf.get('mysql', "passwd"),
                                    db=cf.get('mysql', "db"),
                                    charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor);
       # 通过cursor创建游标
       cursor = connection.cursor()
       # 查询类型和项目名
       sql = "SELECT  project_name, client  from auto_projectManage  where id = '"+self.projectid+"'"
       print(sql)
       cursor.execute(sql)
       project_manage_result = cursor.fetchone()
       print (u"查询xml文件")
       sql="SELECT id,testngXml_file from auto_caseList  where project_id = '"+self.projectid+"'"
       print(u"执行语句",sql)
       cursor.execute(sql)
       # 查询数据库多条数据
       result = cursor.fetchall()
       print(result)
       #判断xml文件是否还存在 '''

       project_name = project_manage_result['project_name'].encode('utf-8')
       client = project_manage_result['client'].encode('utf-8')
       testnglist = self.svn_list(client, project_name)
       for data in result:
           for xmlid in self.xmlid:
               if data['id']==xmlid: #判断id和传入的id是否相同
                    if data['testngXml_file'] in testnglist:
                        get_xmlname.append(str(data['testngXml_file']))

"""

    def svn_list(self, client, projectname):
           # 新建svn目录
           url = "svn list  http://svn.egomsl.com/svn/repos/autotest.globalegrow.com/projectScript/uitest/" + client.lower() + "/" + projectname + "/testng"
           urlxml = subprocess.check_output(url, shell=True)
           return urlxml

    def create_jenkinsjob(self,project_name,type,xml_name):
        '''
        创建一个Jenkins的job
        :param
        :return:
        '''
        jenkins = self.connet_jenkinsjob()
        copy_job_name = 'demo'
        xml = jenkins[copy_job_name].get_config()
        for i in xml_name: #创建的job名称为：项目名+pc类型+xml文件，保证不重名
            jobname = project_name+ "_" +type.lower() + "_" + str(i)

            if (jenkins.has_job(jobname)):
                print(u"job已经创建不用在创建")
            else:
                print(u"创建job", jobname)
                jenkins.create_job(jobname, xml)

                xmlold = '<defaultValue>testng_prd_login2.xml</defaultValue>'
                xmlnew = '<defaultValue>' + str(i) + '</defaultValue>'

                svnold = '<remote>http://svn.egomsl.com/svn/repos/autotest.globalegrow.com/projectScript/uitest/demogrid</remote>'
                svnnew = '<remote>http://svn.egomsl.com/svn/repos/autotest.globalegrow.com/projectScript/uitest/' + type + '/' + project_name + '</remote>'
                htmlold = '<reportDir>test-output/html-report/rosewholesale/</reportDir>'
                htmlnew = '<reportDir>test-output/html-report/' + project_name + '/</reportDir>'

                j.updateconfig(jobname, xmlold, xmlnew)  # 更新xml文件
                j.updateconfig(jobname, svnold, svnnew)
                j.updateconfig(jobname, htmlold, htmlnew)

    def updateconfig(self,jobname,old,new):
        print("updateconfig", jobname)
        myJob = self.connet_jenkinsjob().get_job(jobname)
        myConfig = myJob.get_config()
        newfile = myConfig.replace(old,new)
        myJob.update_config(newfile)


if __name__ == '__main__':
    j=jenkinsCreateJob()
    #j = jenkinsCreateJob("dc20336857c8e91592185f6dd5beeb65",["9902c8a6-0e34-11e8-9422-1866dae8daf8","99030e1a-0e34-11e8-9422-1866dae8daf8"]) #1:类型，pc还是m 2;项目名称 3:xml文件
    #j.connet_mysql()
    j.crete_jenkinsjob()



