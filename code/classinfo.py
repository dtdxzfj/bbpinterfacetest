import time
import random
from common.crmrequest import CrmRequest
from common.crmurlconf import CrmUrls
from common.crmtoolconf import CrmTools
from tools.rwconfig import RWConfig

from tools.mylog import MyLog

from code.platformlogin import PlatformLogin

"""
班级管理接口：
1、查询班级信息,使用班级名称查询
2、发布班级
3、更改班级渠道
4、更新班级开课时间
5、安外教老师
6、查询班级报班的学生信息，学生报班关系，班级课时信息，等待更新

附加功能，更新班级日期为时间戳

注： 班级名称，模板名称，课程名称，一般情况下是一样的，后续可以借助这个简化查询

"""


class ClassInfo:

    # 班级时间处理，静态方法，独立于其他方法，传入格式化日期，格式：2021-04-23,转换成毫秒时间戳
    @staticmethod
    def class_editdate(classdate):
        datetuple = time.strftime("{d} 00:00:00".format(d=classdate))
        timestmap = time.strptime(datetuple, "%Y-%m-%d %H:%M:%S")  # 格式化当前元组,先传日期类型字符串，后传格式参数
        return str(int(time.mktime(timestmap))) + '000'

    # 查询并返回对应班级的可用外教老师id信息,查询数据只显示前10个
    @staticmethod
    def class_foreigntecherlist(classid):
        data = {
            "page": 1,
            "size": 10,
            "classId": classid
        }
        foreignteachers = CrmRequest(CrmUrls().class_foreignteacher).post(data)
        teacherlist = foreignteachers['data']['list']
        teacherlistsum = foreignteachers['data']['total']
        MyLog.loginfo(f'查询可用外教数量:{teacherlistsum}')
        if teacherlist:
            foreign_list = [item['id'] for item in teacherlist]
            return foreign_list
        else:
            MyLog.logwarning("查询可用外教老师出现异常，{}".format(foreignteachers['msg']))

    # 查询并返回对应班级的中教老师id信息,查询数据只显示前20个
    @staticmethod
    def class_chinesecherlist():
        data = {"page": 1, "size": 20, "jobStatus": 1, "teacherRole": ""}
        chineseteachers = CrmRequest(CrmUrls().class_chinesetecher).post(data)
        teacherlist = chineseteachers['data']['list']
        if teacherlist:
            chineseteacherlist = []
            for item in teacherlist:
                chineseteacherlist.append(item['id'])
            else:
                return chineseteacherlist

    # 使用班级名称或者班级编码查询班级信息
    @classmethod
    def classinfo(cls, classcode=None, classname=None, tempid=None):
        if classcode:
            cls.data = {"maintainStatus": "1",
                        "subjectCode": CrmTools.crm_subject[RWConfig.read_config('default', 'subject')],
                        "classCode": classcode, "ifNotGrouped": False,
                        "groupIds": [], "page": 1, "size": 10, "queryRequests": []}
        elif classname:
            cls.data = {
                "maintainStatus": "",
                "subjectCode": CrmTools.crm_subject[RWConfig.read_config('default', 'subject')],
                "ifNotGrouped": False,
                "groupIds": [],
                "page": 0,
                "size": 10,
                "queryRequests": [
                    {
                        "uncode": "2",
                        "sign": "equal",
                        "val": classname
                    }
                ]
            }
        elif tempid:
            cls.data = {
                "maintainStatus": "1",
                "subjectCode": CrmTools.crm_subject[RWConfig.read_config('default', 'subject')],
                "ifNotGrouped": None,
                "groupIds": [],
                "page": 1,
                "size": 10,
                "queryRequests": [
                    {
                        "uncode": "39",
                        "sign": "equal",
                        "val": tempid
                    }
                ]
            }
        else:
            MyLog.logwarning("请输入班级名称或者班级编码、模板编码")
        classinfos = CrmRequest(CrmUrls().class_info).post(cls.data)['data']
        if 'list' in classinfos:
            classinfolist = []
            for item in classinfos['list']:
                classitem = {'id': item['id'], 'classname': item['className'],
                             'classcode': item['classCode'], 'classtemplateid': item['templateId']}
                classinfolist.append(classitem)
            # MyLog.loginfo('班级信息列表：{}'.format(classinfolist))
            return classinfolist
        else:
            MyLog.logwarning("您查询的班级信息不存在")

    @classmethod
    def class_state(cls, classcode=None, classid=None):
        if classid:
            cls.classid = classid
        else:
            cls.classid = cls.classinfo(classcode=classcode)[0]['id']
        req = CrmRequest(url=CrmUrls().class_state + str(cls.classid)).post()
        time.sleep(1)
        MyLog.loginfo("班级发布状态：{}".format(req['msg']))

    @classmethod
    def class_updatechannel(cls, classid, channel):
        data = {
            "id": classid,
            "courseChannelCode": CrmTools.crm_course_channel[channel]
        }
        req = CrmRequest(CrmUrls().class_channel).post(data)
        MyLog.loginfo("班级渠道更新：{}".format(req['msg']))

    # 班级安上课时间
    # 上课时间要以2021-03-29格式,schoolTimeStatus为0代表周期上课时间，为1代表指定课时上课时间
    @classmethod
    def class_updatetime(cls, classid, schooltimeid, startdate, stage=10):
        data = {
            "classId": classid,
            "schoolTimeStatus": 0,
            "stage": stage,
            "schoolTimeId": schooltimeid,
            "classStartDate": cls.class_editdate(startdate),
            "hasParentClass": 0
        }
        req = CrmRequest(CrmUrls().class_time).post(data)
        MyLog.loginfo("班级按上课时间：{}".format(req['msg']))

    # 班級按外教老师，第一个默认为215空外教
    @classmethod
    def class_foreigntecher(cls, classid, foreignteacherid=None):
        if foreignteacherid:
            cls.foreignteacherid = foreignteacherid
        else:
            foreignteacherlist = cls.class_foreigntecherlist(classid)
            if len(foreignteacherlist) > 1:
                cls.foreignteacherid = foreignteacherlist[random.randint(1, len(foreignteacherlist))]
                data = {
                    "classId": classid,
                    "classType": 1,
                    "foreignTeacherId": foreignteacherid
                }
                req = CrmRequest(CrmUrls().class_editteacher).post(data)
                MyLog.loginfo("班级按外教老师：{}，老师id：{}".format(req['msg'], cls.foreignteacherid))
            else:
                MyLog.logwarning("无法安排外教，可用老师为空")

    # 班级按中教老师
    @classmethod
    def class_chinesetecher(cls, classid, chineseteacherid=None):
        if chineseteacherid:
            cls.chineseteacherid = chineseteacherid
        else:
            chineseteacherlist = cls.class_chinesecherlist()
            cls.chineseteacherid = chineseteacherlist[random.randint(0, len(chineseteacherlist))]
            data = {
                "classId": classid,
                "classType": 1,
                "chineseTeacherId": chineseteacherid
            }
            req = CrmRequest(CrmUrls().class_editteacher).post(data)
            MyLog.loginfo("班级按中教老师：{}，老师id：{}".format(req['msg'], cls.chineseteacherid))

    @classmethod
    def class_offstate(cls, classcode=None, classid=None):
        if classid:
            cls.classid = classid
        else:
            cls.classid = cls.classinfo(classcode=classcode)[0]['id']
        url = CrmUrls().class_offstate + str(cls.classid) + '&foreignAvailableTimeState=1'
        req = CrmRequest(url=url).post()
        time.sleep(1)
        MyLog.loginfo("班级下架：{}".format(req['msg']))

    # 班级废弃接口
    @classmethod
    def class_abandon(cls, classcode=None, classid=None):
        if classid:
            classid = classid
        else:
            classid = cls.classinfo(classcode=classcode)[0]['id']
        req = CrmRequest(CrmUrls().class_abandon).post([classid])
        print(req)
        time.sleep(1)
        MyLog.loginfo("班级废弃：{}".format(req['msg']))


if __name__ == "__main__":
    PlatformLogin.login_bbp()
    #     ClassInfo.class_abandon(classid='457017')
    #     tech_list  = ClassInfo.class_foreigntecherlist('428383')
    #     print(tech_list)
    #     if '32742' in tech_list:
    #         print('yes')
