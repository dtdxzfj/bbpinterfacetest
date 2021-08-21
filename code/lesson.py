from common.crmrequest import CrmRequest
from common.crmurlconf import CrmUrls
from common.crmtoolconf import CrmTools
# from code.platformlogin import PlatformLogin
from tools.rwconfig import RWConfig
from tools.mylog import MyLog
import time

"""
课时管理接口
1、课时添加,lessonway为1是直播课，为2是ai课堂
2、课时ID查询
3、课时发布

"""


class Lesson:

    def __init__(self, lessonname):
        self.lessonname = lessonname

    def lesson_add(self, term, course_type,
                   level=RWConfig.read_config('default', 'level'),
                   remark=RWConfig.read_config('default', 'remark'),
                   lessonway=RWConfig.read_config('default', 'lessonway')):
        lessondata = {
            "name": self.lessonname,
            "isTestCourse": 0,
            "whenLong": RWConfig.read_config('default', 'whenLong'),
            "vocabulary": "",
            "term": CrmTools.crm_term[term],
            "level": CrmTools.crm_course_level[level],
            "courseType": CrmTools.crm_course_type[course_type],
            "remark": remark,
            "lessonWay": lessonway,
            "materialType": "10",
            "subjectName": RWConfig.read_config('default', 'subject'),
            "subjectCode": CrmTools.crm_subject[RWConfig.read_config('default', 'subject')],
            "coveUrl": "",
            "resources": []
        }
        req = CrmRequest(CrmUrls().lesson_add).post(lessondata)
        if 'msg' in req:
            MyLog.loginfo("课时名称:{n},创建状态:{s}".format(n=self.lessonname, s=req['msg']))
        else:
            MyLog.logwarning(req)

    def lesson_info(self):
        data = {
            "status": "1",
            "name": self.lessonname,
            "page": 1,
            "size": "50"
        }
        lesson_req = CrmRequest(CrmUrls().lesson_info).post(data)
        if 'data' in lesson_req:
            if 'list' in lesson_req['data']:
                lessonlist = lesson_req['data']['list']
                if lessonlist:
                    lessondict = {
                        'lessonName': lessonlist[0]['name'],
                        'lessonId': lessonlist[0]['id'],
                        'lessonWay': lessonlist[0]['lessonWay'],
                    }
                    # MyLog.loginfo('课时名称:{}，字典数据：{}'.format(self.lessonname, lessondict))
                    return lessondict
                else:
                    MyLog.logwarning("您查询的课时名称:{}不存在".format(self.lessonname))
            else:
                MyLog.logwarning("您查询的课时有误:{}".format(lesson_req['msg']))
        else:
            MyLog.logwarning("您查询的课时有误:{}".format(lesson_req['msg']))

    def lesson_state(self):
        lesssoninfo = self.lesson_info()
        if lesssoninfo:
            lessonid = lesssoninfo['lessonId']
            lessonstate = dict(id=lessonid, state=20)
            state = CrmRequest(CrmUrls().lesson_state).post(lessonstate)
            MyLog.loginfo(
                "课时名称:{name},id:{id},发布状态:{msg}".format(name=self.lessonname, id=lessonid, msg=state['msg']))
        else:
            MyLog.logwarning("课时名称：{}，发布出错".format(self.lessonname))

    # 课时撤销发布
    def lesson_offstate(self):
        lesssonid = self.lesson_info()['lessonId']
        lessonstate = dict(id=lesssonid)
        state = CrmRequest(CrmUrls().lesson_offstate).post(lessonstate)
        MyLog.loginfo(
            "课时名称:{name},课时id:{id},撤销发布:{msg}".format(name=self.lessonname, id=lesssonid, msg=state['msg']))

    # 课时废弃
    def lesson_batch(self):
        lesssonid = self.lesson_info()['lessonId']
        lessonstate = {"ids": [lesssonid], "status": 0}
        state = CrmRequest(CrmUrls().lesson_batch).post(lessonstate)
        MyLog.loginfo(
            "课时名称:{name},id:{id},课时废弃:{msg}".format(name=self.lessonname, id=lesssonid, msg=state['msg']))


# if __name__ == "__main__":
#     PlatformLogin.login_bbp()
#     le = Lesson('测试222h84')
#     #     le.lesson_add(term='春', level='L2', course_type='主课1V3')
#     #     le.lesson_info()
#     le.lesson_state()
#     le.lesson_offstate()
#     le.lesson_batch()

class LessonList:

    @classmethod
    def lessonlist(cls, lessonnamelist, term, coursetype):
        lessonlist = []
        for item in lessonnamelist:
            lesson = Lesson(item)
            time.sleep(2)
            lesson.lesson_add(term, coursetype)
            time.sleep(2)
            lesson.lesson_state()
            time.sleep(1)
            lessondict = lesson.lesson_info()
            lessonlist.append(lessondict)
        else:
            # MyLog.loginfo('课时list数据：{}'.format(lessonlist))
            return lessonlist
