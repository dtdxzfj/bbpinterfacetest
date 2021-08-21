from common.crmrequest import CrmRequest
from common.crmurlconf import CrmUrls
from common.crmtoolconf import CrmTools
from tools.mylog import MyLog
from tools.rwconfig import RWConfig

from code.platformlogin import PlatformLogin

"""
模板管理接口：
1、创建模板
2、查询模板id
3、模板开班
注： 模板查询不支持使用模板名称查询

"""


class TempLate:

    @classmethod
    def temp_add(cls, courseid, coursechannel=RWConfig.read_config('default', 'channel'),
                 livetemplateid=RWConfig.read_config('default', 'thirdpartytemplateid')):
        lesson_req = CrmRequest(CrmUrls().course_lesson).get(courseid)
        lessoninfo = lesson_req['data']['courseLessonList']
        lessonlist = []
        for item in lessoninfo:
            lessondict = {
                "lessonId": item['lessonId'],
                "name": item['lessonName'],
                "price": RWConfig.read_config('default', 'price'),
                "showPrice": RWConfig.read_config('default', 'showPrice'),
                "contractPrice": RWConfig.read_config('default', 'contractPrice'),
                "teacherRole": item['teacherRole']
            }
            lessonlist.append(lessondict)
        else:
            tempdata = {
                "channelGrade": "3",
                "courseChannelCode": CrmTools.crm_course_channel[coursechannel],
                "syncStatus": 0,
                "stage": "",
                "classStartDate": None,
                "sendMaterial": 0,
                "courseId": courseid,
                "templateTimes": [
                    {
                        "schoolTimeId": "",
                        "openClassNum": ""
                    }
                ],
                "schoolTimeStatus": 0,
                "templateLessonList": lessonlist,
                "liveContain": 3,
                "commentStatus": 1,
                "freeLesson": 0,
                "thirdPartyTemplateId": livetemplateid
            }
            req = CrmRequest(CrmUrls().temp_add).post(tempdata)
            if req['code'] != 10000:
                MyLog.logwarning(req['msg'])
            else:
                MyLog.loginfo('模板创建：{}，模板id：{}'.format(req['msg'], req['data']))
                return req['data']

    # 对外用于查询模板信息,默认返回前十个模板数据
    @classmethod
    def template_info(cls, year=None, term=None, coursetype=None, channel=None, temp_id=None):
        if temp_id:
            cls.data = {
                "maintainStatus": "1",
                "id": temp_id,
                "page": 1,
                "size": 10,
                "queryRequests": [{"uncode": "2", "sign": "equal", "val": channel}]
            }
        else:
            cls.data = {
                "termList": [CrmTools.crm_term[term]],
                "courseType": CrmTools.crm_course_type[coursetype],
                "level": None,
                "maintainStatus": "1",
                "year": year,
                "id": None,
                "page": 1,
                "size": 10,
                "queryRequests": [{"uncode": "2", "sign": "equal", "val": channel}]
            }
        templist = CrmRequest(CrmUrls().temp_info).post(cls.data)['data']['list']
        if templist:
            tempinfolist = []
            for item in templist:
                tempdict = {
                    'tempid': item['id'],
                    'tempname': item['course']['courseName'],
                    'courseid': item['course']['id']
                }
                tempinfolist.append(tempdict)
            else:
                MyLog.loginfo(f'模板查询总数：{len(templist)}')
                MyLog.loginfo(f"模板信息：{tempinfolist}")
                return tempinfolist
        else:
            MyLog.logwarning("您查询的模板数据为空！")

    @classmethod
    def temp_open(cls, tempid, quantity=1):
        data = {
            "templateId": tempid,
            "quantity": quantity
        }
        req = CrmRequest(CrmUrls().temp_openclass).post(data)
        MyLog.loginfo("模板ID：{a},开班情况：{b}".format(a=tempid, b=req['msg']))

    @classmethod
    def temp_abandon(cls, tempid):
        data = [tempid]
        temp_req = CrmRequest(CrmUrls().temp_abandon).post(data)
        MyLog.loginfo("模板废弃：{}".format(temp_req['msg']))


# if __name__ == "__main__":
#     PlatformLogin.login_bbp()
#     print(TempLate.temp_add('7838'))
    # print(TempLate.template_info(temp_id='5177'))
#     print(t)
#     TempLate.temp_open('7111')
