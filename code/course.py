from common.crmrequest import CrmRequest
from common.crmurlconf import CrmUrls
from common.crmtoolconf import CrmTools
from tools.rwconfig import RWConfig
from tools.mylog import MyLog

"""
课程管理接口：
1、课程添加，其中少一些非必要数据，后续完善添加
2、课程id查询
3、课程发布
4、课程详情查询课时列表数据
"""


class Course:

    def __init__(self, coursename):
        self.coursename = coursename

    def course_add(self, year, term, coursetype, lessonlist,
                   classway=eval(RWConfig.read_config('default', 'classway')),
                   level=RWConfig.read_config('default', 'level'),
                   channel=RWConfig.read_config('default', 'channel'),
                   experiencetype=RWConfig.read_config('default', 'experiencetype'),
                   remark=RWConfig.read_config('default', 'remark')):  # 组课接口
        """
        :param experiencetype: 学龄标签
        :param term: 课程学季
        :param level: 课程水平
        :param coursetype: 课程类型，主课1v3等等
        :param year: 学年
        :param lessonlist:课时列表，包含id，name，lessonway，需要用到lesson_info函数，入参之后进行判断添加teacherRole字段
        :param channel: 课程渠道，默认测试渠道,：75，各个环境通用
        :param remark: 备注
        :param classway: 课程上课类型 ，1为直播，2为中外混合直播，3为录播
        :return:
        """
        course_type = CrmTools.crm_course_type[coursetype]
        for item in lessonlist:
            if int(course_type) == 80:
                item['teacherRole'] = 2
            elif int(course_type) in [98, 99]:
                item['teacherRole'] = 3
            else:
                if classway == 1:
                    item['lessonWay'] = 1
                    item['teacherRole'] = 1
                elif classway == 3:
                    item['lessonWay'] = 2
                    item['teacherRole'] = 0
                elif classway == 5:
                    item['lessonWay'] = 1
                    item['teacherRole'] = int(input("请选择授课角色：1：外教课，2： 中教课："))

        else:
            coursedata = {
                "term": CrmTools.crm_term[term],
                "level": CrmTools.crm_course_level[level],
                "courseType": CrmTools.crm_course_type[coursetype],
                "year": year,
                "courseChannel": CrmTools.crm_course_channel[channel],
                "classStyle": 4,
                "remark": remark,
                "classWay": classway,
                "courseName": self.coursename,
                "courseDescribe": "课程接口测试数据zfj",
                "subjectCode": CrmTools.crm_subject[RWConfig.read_config('default', 'subject')],
                "projectCode": "10",
                "teachingContent": "201",
                "experienceType": experiencetype,
                "coveUrl": None,
                "courseLessonList": lessonlist,
                "subjectName": RWConfig.read_config('default', 'subject'),
            }

            coursereq = CrmRequest(CrmUrls().course_add).post(coursedata)
            MyLog.loginfo("课程名称:{n},创建状态:{s}".format(n=self.coursename, s=coursereq['msg']))
            # return coursereq['data']

    def course_info(self):
        data = {
            "status": "1",
            "name": self.coursename,
            "page": 1,
            "size": 10
        }
        courselist = CrmRequest(CrmUrls().course_info).post(data)
        if 'data' in courselist:
            if 'list' in courselist['data']:
                listid = courselist['data']['list']
                course_dict = {'courseid': listid[0]['id'], 'name': listid[0]['courseName'], 'year': listid[0]['year']}
                return course_dict
            else:
                MyLog.logwarning("您查询的课程名称不存在，请检查后再试")
        else:
            MyLog.logwarning("您查询的课程名称有误:{}".format(courselist['msg']))

    def course_state(self):
        coursedict = self.course_info()
        courseid = coursedict['courseid']
        name = coursedict['name']
        year = coursedict['year']
        data = dict(id=courseid, courseName=name, year=year, state=20)
        msg = CrmRequest(CrmUrls().course_state).post(data)
        MyLog.loginfo('课程名字：{},课程id:{},课程发布：{}'.format(name, courseid, msg['msg']))

    def course_batch(self):
        coursedict = self.course_info()
        courseid = coursedict['courseid']
        data = {"ids": [courseid], "status": 0}
        batch_req = CrmRequest(CrmUrls().course_batch).post(data)
        MyLog.loginfo('课程id:{}，课程废弃：{},'.format(courseid, batch_req['msg']))

# if __name__ == "__main__":
#     print(Course('测试05251700').course_info())
#     # print(ReadConfig.read_config('default', 'experiencetype'),)
#     Course("测试周期导入中教").course_add(2021,'春上', '主课1V3', [{'lessonName': '全年班春下课时', 'lessonId': 2983, 'lessonWay': 1}])
