from common.crmrequest import CrmRequest
from common.crmurlconf import CrmUrls
from common.crmtoolconf import CrmTools
from code.platformlogin import PlatformLogin
from tools.mylog import MyLog
import time

"""
续班操作
1、查询带续班班级信息
2、续班
3、续班排班
3、联报用户转班
4、查询续班是否已经开办成功

"""


class ResubmitClass:
    """
    续班多功能筛选项
    "title": "班级渠道","uncode": "1","title": "当前班容","uncode": "2",
    "title": "班级班容","uncode": "3","title": "期","uncode": "4",
    "title": "上一季原班的期","uncode": "5","title": "班级名称","uncode": "6",
    "title": "新班/续班","uncode": "8","title": "等级","uncode": "11",
    """
    queryqequests = [
        {
            "uncode": "1",
            "sign": "equal",
            "val": 75
        },
        {
            "uncode": "3",
            "sign": "equal",
            "val": None
        }
    ]

    # 查询测试渠道1,当前班容2为None下对应的待排班班级信息,后续查询其他筛选项
    @classmethod
    def resubmitinfo(cls, year, term, coursetype):
        data = {
            "page": 1,
            "size": 20,
            "term": CrmTools.crm_term[term],
            "year": year,
            "courseType": CrmTools.crm_course_type[coursetype],
            "queryRequests": cls.queryqequests
        }
        resubmitreq = CrmRequest(CrmUrls().resubmit_info).post(data)
        if 'data' in resubmitreq:
            resubmisum = resubmitreq['data']['total']
            resubmitclasslist = []
            if resubmisum == 0:
                MyLog.logwarning("您查询的续班班级数据为空！")
            else:
                MyLog.loginfo('续班总数为：{}'.format(resubmisum))
                resubmitlist = resubmitreq['data']['list']
                for item in resubmitlist:
                    resubmitdict = {'classcode': item['classCode'], 'classid': item['classId'],
                                    'termname': item['termName'], 'stagename': item['stageName'],
                                    'resubmitclasscode': item['resubmitClassCode']}
                    resubmitclasslist.append(resubmitdict)
                else:
                    MyLog.loginfo(f'续班班级数据：{resubmitclasslist}')
                    return resubmitclasslist
        else:
            MyLog.logwarning(resubmitreq['msg'])

    # 一键开续班,默认使用测试渠道的数据
    @classmethod
    def resubmitclass(cls, year, term, coursetype, templateid, scheduletimetype=2):
        """

        :param year: 学年
        :param term: 学季
        :param coursetype:
        :param templateid: 模板id，由于是测试数据，所以每个等级的模板id相同
        :param scheduletimetype: 排课方式，1为切齐排课（需要填写每期上课时间），2为连续排课
        :return:
        """
        startdate = {}
        if scheduletimetype == 1:
            startdate['10'] = str(input("请输入一期上课时间（格式：2021-04-21）："))
            startdate['20'] = str(input("请输入二期上课时间（格式：2021-04-21）："))
            startdate['30'] = str(input("请输入三期上课时间（格式：2021-04-21）："))
            startdate['40'] = str(input("请输入四期上课时间（格式：2021-04-21）："))
        else:
            startdate = None
        data = {
            "term": CrmTools.crm_term[term],
            "year": year,
            "stage": None,
            "nextStage": {
                "10": 10,
                "20": 10,
                "30": 10,
                "40": 10
            },
            "levelTemplate": {
                "10": templateid,
                "20": templateid,
                "30": templateid,
                "40": templateid,
                "50": templateid
            },
            "courseType": CrmTools.crm_course_type[coursetype],
            "scheduleTimeType": scheduletimetype,
            "startDate": startdate,
            "queryRequests": cls.queryqequests
        }
        resubmitreq = CrmRequest(CrmUrls().resubmit_class).post(data)
        time.sleep(3)
        if 'data' in resubmitreq:
            resubmitinfo = CrmRequest(CrmUrls().resubmit_class_info).get(resubmitreq['data'])
            if 'data' in resubmitinfo:
                if 'data' in resubmitinfo['data']:
                    if resubmitinfo['data']:
                        resubmitinfolist = resubmitinfo['data']['data']
                        if isinstance(resubmitinfolist, list):  # 判断是否是列表属性
                            for item in resubmitinfolist:
                                MyLog.logwarning('续班情况：{}，提示消息：{}'.format(item['resubmitClass'], item['remark']))
                        else:
                            MyLog.logwarning(resubmitinfolist)
                    else:
                        MyLog.loginfo("班级续班成功！")
                else:
                    MyLog.loginfo("班级续班成功！")
            else:
                MyLog.logwarning('续班班级操作：{}'.format(resubmitinfo['msg']))
        else:
            MyLog.logwarning('续班出现异常：{}'.format(resubmitreq['msg']))

    # 续班变周期规则数据添加
    @classmethod
    def resubmittime(cls, coursetype, wintertimeid, springfirsttimeid):
        termsix = CrmTools.coursetype6  # 学季配置为六季的课程类型
        termfour = CrmTools.coursetype4  # 学季配置为四季的课程类型
        if coursetype in termsix:
            cls.data = dict(courseType=CrmTools.crm_course_type[coursetype], winterTime=wintertimeid,
                            springFirstTime=springfirsttimeid, springSecondTime=springfirsttimeid, springTime=None,
                            summerTime=wintertimeid, autumnFirstTime=springfirsttimeid,
                            autumnSecondTime=springfirsttimeid, autumnTime=None)
            req = CrmRequest(CrmUrls().resubmit_time).post(cls.data)
            MyLog.loginfo('续班时间新建：{}'.format(req['msg']))
        elif coursetype in termfour:
            cls.data = {"courseType": CrmTools.crm_course_type[coursetype], "winterTime": wintertimeid,
                        "springTime": springfirsttimeid, "summerTime": wintertimeid, "autumnTime": springfirsttimeid}
            req = CrmRequest(CrmUrls().resubmit_time).post(cls.data)
            MyLog.loginfo('续班时间新建：{}'.format(req['msg']))
        else:
            MyLog.logwarning("课程类型不支持续班变周期配置")

    # 获取课程类型对应的上课周期数据
    @classmethod
    def resubmittimeinfo(cls, coursetype):
        data = {"page": 1, "size": 10, "courseType": CrmTools.crm_course_type[coursetype]}
        timereq = CrmRequest(CrmUrls().resubmit_time_info).post(data)
        if timereq['data']['list']:
            timeinfolist = []
            timelist = timereq['data']['list']
            for item in timelist:
                timedict = dict(暑ID=item['summerTime'], 暑周期=item['summerTimetext'], 秋上ID=item['autumnFirstTime'],
                                秋上周期=item['autumnFirstTimetext'], 秋ID=item['autumnTime'], 秋周期=item['autumnTimetext'])
                timeinfolist.append(timedict)
            else:
                # MyLog.loginfo(f"{coursetype}的续班周期数据：{timeinfolist}")
                return f"{coursetype}：{timeinfolist}"
        else:
            MyLog.logwarning("查询的续班周期为空")


# if __name__ == "__main__":
#     PlatformLogin.login_bbp()
# #     print(ResubmitClass.resubmittimeinfo('主课1V3'))
#     # ResubmitClass.resubmittime('主课1V3', 55680, 55675)
# #     # time.sleep(1)
#     ResubmitClass.resubmitinfo('2021', '秋', '自然拼读课')
#     ResubmitClass.resubmitclass('2021', '春下', '小班课', 762933)
