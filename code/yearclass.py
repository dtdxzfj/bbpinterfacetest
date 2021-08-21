# from code.platformlogin import PlatformLogin
from common.crmtoolconf import CrmTools
from code.lesson import LessonList
from code.course import Course
from code.template import TempLate
from code.classinfo import ClassInfo
from code.resubmitclass import ResubmitClass
from tools.mylog import MyLog
import time

"""
全年班脚本
1、获取学年学季列表
2、创建模板
3、一键开全年班
4、续班生成

"""


class YearClass:

    @classmethod
    def gettermlist(cls, course_type, firstterm, termsum):
        coursetype6 = CrmTools.coursetype6  # 学季配置为六季的课程类型
        coursetype4 = CrmTools.coursetype4  # 学季配置为四季的课程类型
        termlist6 = CrmTools.termlist6
        termlist4 = CrmTools.termlist4
        if course_type in coursetype6:
            if firstterm in termlist6:
                ii6 = termlist6.index(firstterm)
                if int(ii6 + termsum) <= 6:
                    return termlist6[ii6:ii6 + termsum]
                else:
                    return termlist6[ii6:6] + termlist6[:termsum - (6 - ii6)]
            else:
                MyLog.logwarning("当前课程类型不存在该学季")
        elif course_type in coursetype4:
            if firstterm in termlist4:
                ii4 = termlist4.index(firstterm)
                if int(ii4 + termsum) <= 4:
                    return termlist4[ii4:ii4 + termsum]
                else:
                    return termlist4[ii4:4] + termlist4[:termsum - (4 - ii4)]
            else:
                MyLog.logwarning("当前课程类型不存在该学季")
        else:
            MyLog.logwarning("当前课程类型不存在续报学季")

    @classmethod
    def createtemplate(cls, lessonname_list, course_name, year, term, course_type):
        lessonlist = LessonList.lessonlist(lessonname_list, term, course_type)
        course = Course(course_name)
        course.course_add(year, term, course_type, lessonlist)
        time.sleep(2)
        course_id = course.course_info()['courseid']
        course.course_state()
        return TempLate.temp_add(course_id)

    # 模板开班
    @classmethod
    def class_info(cls, temp_id, schooltime_id, date):
        TempLate.temp_open(temp_id)
        classlist = ClassInfo.classinfo(tempid=temp_id)
        classid, classcode = classlist[0]['id'], classlist[0]['classcode']
        ClassInfo.class_state(classid=classid)
        ClassInfo.class_updatetime(classid, schooltime_id, date)
        # ClassInfo.class_updatechannel(classid, '虚拟班')
        return classid, classcode

    # 一键开全年班
    @classmethod
    def yearclass(cls, year, coursetype, date, schooltimeid, testname, termsum, term='暑', lessonsum=1):
        # a = time.time()
        year_list = [int(year), int(year) + 1]
        classcode_list = []
        if cls.gettermlist(coursetype, term, termsum):
            term_list = cls.gettermlist(coursetype, term, termsum)
            for index, item in enumerate(term_list):
                lessonnamelist = []
                if '寒' in term_list:
                    if index > term_list.index('寒') - 1:
                        year = year_list[1]  # 逢寒升学年，班级名字，学年匹配
                if lessonsum == 1:  # 根据课时总数，批量创建课时
                    lessonname = '测试{}年{}课({})zfj'.format(year, testname, item)
                    lessonnamelist.append(lessonname)
                else:
                    for i in range(1, lessonsum + 1):
                        lessonname = '测试{}年{}课{}({})zfj'.format(year, testname, i, item)
                        lessonnamelist.append(lessonname)
                coursename = '测试{}年{}班({})zfj'.format(year, testname, item)
                temp_id = cls.createtemplate(lessonnamelist, coursename, year, item, coursetype)
                if index == 0:
                    # print(coursename)
                    classid, classcode = cls.class_info(temp_id, schooltimeid, date)
                    MyLog.loginfo(f'原班id：{classid}，原班编码：{classcode}')
                    classcode_list.append(classcode)
                else:
                    if '寒' in term_list:
                        if index == term_list.index('寒'):
                            year = year_list[0]  # 续班查询上一学季时学年仍为上一年
                    # print(coursename)
                    resubitclasslist = cls.resubmitclass(year, term_list[index - 1], coursetype, temp_id)
                    for resubitclass in resubitclasslist:
                        if classcode_list[index - 1] in resubitclass.values():
                            classcode_list.append(resubitclass['resubmitclasscode'])
            else:
                classid_list = []
                for item in classcode_list:
                    classid = ClassInfo.classinfo(classcode=item)
                    classid_list.append(classid[0]['id'])
                    time.sleep(1)
                else:
                    MyLog.loginfo(f'全年班班级id数据：{classid_list},全年班班级编码数据：{classcode_list}')
                    # b = time.time()
                    # MyLog.loginfo(f'运行时长：{b-a}')
                    return classid_list, classcode_list
        else:
            MyLog.logwarning('当前课程类型获取的学季配置为空')

    # 续班查看和生成流程
    @classmethod
    def resubmitclass(cls, lastterm_year, lastterm, course_type, next_tempid):
        resubmitclasslist = ResubmitClass.resubmitinfo(lastterm_year, lastterm, course_type)
        ResubmitClass.resubmitclass(lastterm_year, lastterm, course_type, next_tempid)
        return resubmitclasslist


if __name__ == '__main__':
    pass
    # PlatformLogin.login_bbp()
    # YearClass.createtemplate()
    # c = '小班课'
    # c = '自然拼读课'
    # # termlist = ['暑', '秋上', '秋下', '寒', '春上', '春下']
    # termlist = ['暑', '秋', '寒', '春']
    # for items in termlist:
    #     for ii in range(1,len(termlist)+1):
    #         print(ii)
    #         YearClass.yearclass('2021', c, None, None, f'{c}', ii, term=items)
    #         print()
    #     print()
