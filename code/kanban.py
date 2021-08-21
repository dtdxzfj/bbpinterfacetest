from code.platformlogin import PlatformLogin
from common.crmrequest import CrmRequest


class MainTecherKanBan:
    update = 'https://lapi-smix2.t.blingabc.com/bms/user-api/bs/lesson/v1/save-lesson-teacher?ids='
    classid = 'https://lapi-smix2.t.blingabc.com/bms/user-api/classinfo/v1/classInfos'
    lessonid = 'https://lapi-smix2.t.blingabc.com/bms/admin-api/studentlesson/v1/stuclass/'

    @classmethod
    def classinfo(cls, classcode, num):
        """

        :param classcode: 比邻班级编码
        :param num: 需要处理的对应课次，从1 开始
        :return:
        """
        if classcode:
            data = {"maintainStatus": "1", "subjectCode": 10, "classCode": classcode, "ifNotGrouped": False,
                    "groupIds": [], "page": 1, "size": 10, "queryRequests": []}
            classinfos = CrmRequest(cls.classid).post(data)

            classids = classinfos['data']['list'][0]
            classid = str(classids['id'])
            lessoninfo = CrmRequest(cls.lessonid).get(str(classid))
            lessid = str(lessoninfo['data']['classLessonVOList'][num - 1]['classLessonId'])

            print(classcode, classid, lessid, num)
        else:
            print("班级数据不存在或者没有上架！")


if __name__ == "__main__":
    PlatformLogin.login_bbp()
    lists = ['21A11010L400031121A', '21A11010L400032121A']
    # OfficialMainTecher.classinfo('21P21090L100749221P'))
    for i in lists:
        MainTecherKanBan.classinfo(i, 1)
