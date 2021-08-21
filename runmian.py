from code.platformlogin import PlatformLogin
from code.lesson import Lesson
from code.lesson import LessonList
from code.course import Course
from code.template import TempLate
from code.classinfo import ClassInfo
from code.student import Student
from code.resubmitclass import ResubmitClass
from code.yearclass import YearClass
import time

"""
1、主程序脚本
2、环境配置，如果改用其他环境请到配置文件中修改即可
支持环境：[t,alpha,smix2,smix1,official]
"""


class RunMain:

    # 课时课程模板流程，返回模板id
    @classmethod
    def createtemplate(cls, test_name, class_year, class_term, course_type, lessonsum=1):
        lessonname_list = []
        lesson_list = []
        if lessonsum == 1:  # 根据课时总数，批量创建课时
            lessonname = '测试{}年{}课({})zfj'.format(class_year, test_name, class_term)
            lesson = Lesson(lessonname)
            lesson.lesson_add(class_term, course_type)
            time.sleep(2)
            ldict = lesson.lesson_info()
            lesson.lesson_state()
            lesson_list.append(ldict)
        else:
            for i in range(1, lessonsum + 1):
                lessonname = '测试{}年{}课{}({})zfj'.format(class_year, test_name, i, class_term)
                lessonname_list.append(lessonname)
            lesson_list = LessonList.lessonlist(lessonname_list, class_term, course_type)
        course_name = '测试{}年{}班({})zfj'.format(class_year, test_name, class_term)
        course = Course(course_name)
        # print(lesson_list)
        course.course_add(class_year, class_term, course_type, lesson_list)
        time.sleep(3)
        course_id = course.course_info()['courseid']
        course.course_state()
        return TempLate.temp_add(course_id)

    # 模板开班
    @classmethod
    def class_info(cls, temp_id, schooltime_id, class_date, foreignteacherid=None):
        TempLate.temp_open(temp_id)
        classlist = ClassInfo.classinfo(tempid=temp_id)
        classid = classlist[0]['id']
        classcode = classlist[0]['classcode']
        ClassInfo.class_state(classid=classid)
        ClassInfo.class_updatetime(classid, schooltime_id, class_date)
        # ClassInfo.class_foreigntecher(classid, foreignteacherid)
        # ClassInfo.class_updatechannel(classid, '虚拟班')
        return classid, classcode

    @classmethod
    def yearclass(cls, class_year, course_type, class_date, schooltime_id, test_name, termsum, class_term, lesson_sum):
        classid_list, classcode_list = YearClass.yearclass(class_year, course_type, class_date, schooltime_id,
                                                           test_name, termsum,
                                                           class_term, lesson_sum)
        return classid_list, classcode_list

    # 续班查看和生成流程
    @classmethod
    def resubmitclass(cls, lastterm_year, last_term, course_type, next_tempid):
        resubmitclasslist = ResubmitClass.resubmitinfo(lastterm_year, last_term, course_type)
        ResubmitClass.resubmitclass(lastterm_year, last_term, course_type, next_tempid)
        return resubmitclasslist

    @classmethod
    def resubmittimeinfo(cls, course_type):
        return ResubmitClass.resubmittimeinfo(course_type)

    # 学员报班下单审核流程
    @classmethod
    def student(cls, classcodelist=None, studentnum=None):
        stu = Student()
        # if studentnum:
        #     studentnum = stu.studentinfo(parentmobile=parentmobile, studentname=studentname)
        ordercode = stu.order_create(studentnum, classcodelist)
        time.sleep(2)
        stu.order_check(ordercode=ordercode)
        # stu.stuclassif(stunum, ordercode)

    @classmethod
    def class_end(self, classcodelist):
        for item in classcodelist:
            ClassInfo.class_state(classcode=item)
            ClassInfo.class_abandon(classcode=item)


if __name__ == '__main__':
    # PlatformLogin.login_bbp()  # 支持不同环境登录操作，包含线上环境
    # 数据配置，部分配置已经写到配置文件，可以根据需求更改配置
    year = 2021  # 学年，支持逢寒升学年
    lesson_sum = 2  # 每个课程中的课时数，默认为1
    term_sum = 2  # 需要开的续班个数
    date = '2021-09-06'  # 原班上课日期
    term = '秋'  # 原班学季
    schooltimeid = 55679  # 第一学季对应的变周期id
    coursetype = '藤校国际班'  # 主课1V3,自然拼读课,藤校国际班,小班课,口语课、文化课、中教课 等
    testname = f'{coursetype}30分钟排外教用'  # 填写的测试名称，课时和班级上使用的名称
    # 模板脚本，班级脚本
    # templateid = RunMain.createtemplate(testname, year, term, coursetype, lesson_sum)
    # classid, classcode = RunMain.class_info(templateid, schooltimeid, date)
    # print(classid, classcode)
    # RunMain.student(classcodelist=[classcode], studentnum='143769563')
    # print(classid, classcode)
    # 查询当前环境上课周期数据,续班班级数据
    # print(RunMain.resubmittimeinfo(coursetype))
    # 一键开全年班
    # RunMain.yearclass(year, coursetype, date, schooltimeid, testname, term_sum, term, lesson_sum)
    # 测试数据处理,班级下架与废弃
    # RunMain.class_end(classcode)
