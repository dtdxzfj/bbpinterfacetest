from common.crmrequest import CrmRequest
from common.crmurlconf import CrmUrls
from common.crmtoolconf import CrmTools
from tools.mylog import MyLog
from code.platformlogin import PlatformLogin
import time
from tools.rwconfig import RWConfig

"""
1、学生信息查询，（家长信息查询）
2、学生下单
3、订单审核
4、查询学生入班信息
学员退班，审核，退班成功，金额为0
学员转班，可以做，先获取转班列表，然后转班，审核

"""


class Student:

    # 内部方法，用于下单时使用班级编码查询对应班级id
    @classmethod
    def classinfo(cls, classcode):
        data = {"maintainStatus": "1", "subjectCode": CrmTools.crm_subject[RWConfig.read_config('default', 'subject')],
                "classCode": classcode, "ifNotGrouped": False,
                "groupIds": [], "page": 1, "size": 10, "queryRequests": []}
        classinfos = CrmRequest(CrmUrls().class_info).post(data)['data']['list']
        if classinfos:
            return classinfos[0]['id']
        else:
            MyLog.logwarning("班级数据不存在或者没有上架！")

    # 类方法，查询订单编码对应的订单id以及订单学生编号和学生姓名
    @classmethod
    def order_id(cls, ordercode):
        orderreq = CrmRequest(CrmUrls().order_id).get(ordercode)['data']['list']
        if orderreq:
            return orderreq[0]['id']
        else:
            MyLog.logwarning("订单号有误或者订单号不存在")

    # 查询家长手机号对应的学员信息,如果输入学生名字则返回学号，如果为空则返回学生信息列表
    @classmethod
    def studentinfo(cls, parentmobile, studentname=None):
        parentreq = CrmRequest(CrmUrls().parent).get(parentmobile)
        if 'data' in parentreq:  # 判断字典中是否存在该键
            parentdata = parentreq['data']
            parentinfo = {'name': parentdata['name'], 'mobile': parentdata['mobile'],
                          'parentNum': parentdata['parentNum']}
            studentreq = CrmRequest(CrmUrls().student).get(parentinfo['parentNum'])
            if 'data' in studentreq:
                studentlist = []
                for item in studentreq['data']:
                    studentinfo = {'name': item['name'], 'stuNum': item['stuNum'], 'parentNum': item['parentNum'],
                                   'parentMobile': item['parentMobile'], 'xdfCode': item['xdfCode']}
                    studentlist.append(studentinfo)
                if studentname:
                    for item in studentlist:
                        if item['name'] == studentname:
                            return item['stuNum']
                    else:
                        MyLog.logwarning("当前手机号下不存在该学员")
                else:
                    return studentlist
        else:
            MyLog.logwarning("您查询的手机号不存在！")

    # 学员下单，创建订单，默认使用测试渠道（78），使用登录账号下单
    @classmethod
    def order_create(cls, studentnum, classcodelist):
        classlist = []
        userinfoid = RWConfig.read_logininfo('userid')
        userinfoaccount = RWConfig.read_logininfo('username')
        for item in classcodelist:
            classdict = {"id": cls.classinfo(item), "classCode": item}
            classlist.append(classdict)
            time.sleep(1)
        else:
            data = {
                "orderChannel": RWConfig.read_config('default', 'orderchannel'),
                "classList": classlist,
                "createId": userinfoid,
                "stuNum": studentnum,
                "userCode": userinfoaccount,
                "discountId": "",
                "useCouponCode": [],
                "sendCouponCodes": [],
                "courseFavorableState": 1,
                "remark": "接口下单测试",
                "isFreePayment": 0,
                "orderTotalPrice": 0,
                "orderMaterialsPrice": 0,
                "checkFlage": 1,
                "couponList": []
            }
            orderreq = CrmRequest(CrmUrls().order_create).post(data)
            if 'data' in orderreq:
                MyLog.loginfo('学员号:{},购买班级:{},订单号:{}'.format(studentnum, classcodelist, orderreq['data']))
                return orderreq['data']
            else:
                MyLog.logwarning(f'下单失败：{orderreq["msg"]}')

    # 获取订单优惠信息,待完善
    @classmethod
    def order_favourable(cls, studentnum, classcodelist):
        data = {"classList": classcodelist, "orderChannel": RWConfig.read_config('default', 'orderchannel'),
                "courseFavorableState": 1,
                "stuNum": studentnum}
        CrmRequest(CrmUrls().order_favourable).post(data)

    # 默认使用管理员审核，如果下单人是管理员，则使用其他账号审核,1为审核，2为驳回
    @classmethod
    def order_check(cls, ordercode=None, parentmobile=None, check_status=1):
        if ordercode:
            cls.checkreq = CrmRequest(CrmUrls().order_info).get(f'&orderCode={ordercode}')['data']
        elif parentmobile:
            cls.checkreq = CrmRequest(CrmUrls().order_info).get(f'&parentMobile={parentmobile}')['data']
            # print(cls.checkreq)
        if cls.checkreq['list']:
            MyLog.loginfo("待审核订单数量为：{}".format(cls.checkreq['total']))
            userinfoid = RWConfig.read_logininfo('userid')
            userinfo_name = RWConfig.read_logininfo('name')
            for item in cls.checkreq['list']:
                if int(item['createId']) == 20:
                    data = dict(ids=[item['id']], checkStatus=check_status, checkUserId=userinfoid)
                    checkreq = CrmRequest(CrmUrls().order_check).post(data)
                    time.sleep(4)
                    MyLog.loginfo(
                        "学员姓名:{}，学员号:{}，审核人:{},审核状态:{}".format(item['name'],
                                                               item['stuNum'], userinfo_name, checkreq['msg']))
                else:
                    data = dict(ids=[item['id']], checkStatus=check_status, checkUserId=20)
                    checkreq = CrmRequest(CrmUrls().order_check).post(data)
                    time.sleep(4)
                    MyLog.loginfo(
                        "学员姓名:{}，学员号:{}，审核人:{},审核状态:{}".format(item['name'],
                                                               item['stuNum'], 'crmadmin', checkreq['msg']))
        else:
            MyLog.logwarning("没有查询到订单待审核记录")

    # 查询学员报班信息
    @classmethod
    def stuclass(cls, stunum):
        data = {
            "page": 1,
            "size": 30,
            "stuNum": stunum
        }
        stuclassinfo = CrmRequest(CrmUrls().student_class).post(data)['data']
        if stuclassinfo['list']:
            MyLog.loginfo('学员报班数量为：{}'.format(stuclassinfo['total']))
            studentclasslist = []
            print(stuclassinfo['list'])
            for item in stuclassinfo['list']:
                stuclassdict = {'state': item['changeStateName'], 'ordercode': item['orderCode'],
                                'orderdetailcode': item['orderDetailCode'], 'classid': item['classId'],
                                'classcode': item['classCode'], 'className': item['className'],
                                'stuclassid': item['stuClassId']}
                studentclasslist.append(stuclassdict)
            else:
                return studentclasslist
        else:
            MyLog.logwarning("学号不存在或者学员没有报任何班级！")

    # 封装一个查询学员是否报班成功的函数，用于后续报班
    @classmethod
    def stuclassif(cls, stunum, classcode):
        data = {
            "page": 1,
            "size": 10,
            "stuNum": stunum
        }
        stuclassinfo = CrmRequest(CrmUrls().student_class).post(data)['data']
        if stuclassinfo['list']:
            stuclasslist = stuclassinfo['list']
            if classcode in [x['classCode'] for x in stuclasslist]:
                MyLog.loginfo("学员：{}，已经在班级：{}".format(stunum, classcode))
            else:
                MyLog.logwarning("班级编码有误或者学员不在班！")
        else:
            MyLog.logwarning("学号不存在或者该学员没有报任何班级！")

    @classmethod
    def stuquit_check(cls, parentmobile=None):
        timenow = int(time.time() * 1000)
        timeago = timenow - 2000000000
        data = {
            "size": 10,
            "page": 1,
            "allData": 1,
            "startDate": timeago,
            "endDate": timenow,
            "telephone": parentmobile
        }
        quitreq = CrmRequest(CrmUrls().class_quit_info).post(data)['data']
        # print(quitreq)
        if quitreq['list']:
            MyLog.loginfo("待退班数量为：{}".format(quitreq['total']))
            userinfo_name = RWConfig.read_logininfo('name')
            for item in quitreq['list']:  # 20通过，30驳回
                data = {"id": item['id'], "reviewState": "20", "rejectReason": "退班测试"}
                req = CrmRequest(CrmUrls().class_quit_check).post(data)
                MyLog.loginfo(
                    "学员姓名:{}，学员号:{}，班级编号:{}，订单金额:{},审核人:{},审核状态:{}".format(item['name'],
                                                                           item['stuNum'], item['classCode'],
                                                                           item['realPrice'], userinfo_name,
                                                                           req['msg']))
                time.sleep(4)
        else:
            MyLog.logwarning("没有查询到退班记录")


if __name__ == "__main__":
    PlatformLogin.login_bbp()
    # asas = Student.studentinfo(parentmobile='17190084003')
    # print(asas)
    # stulist = [b['stuNum'] for b in asas]
    # for stu in range(4):
    #     ordercode = Student.order_create(stulist[stu], ['21A01010L100007021A'])
    #     time.sleep(2)
    #     Student.order_check(ordercode=ordercode)
# print(Student.classinfo('21S01010L200139021S'))
# Student.classinfo('21S01060L100113021S')  '393651138',
    ordercode = Student.order_create('665344511', ['21S01060L100119021S'])
    time.sleep(3)
    Student.order_check(ordercode=ordercode)

# Student.order_check(parentmobile='13811494438')
#     Student.stuquit_check(parentmobile='17190084003')
# ss = Student.stuclass('133867351')
# print(ss)
# Student.stuclassif('617691721','21S01060L200005021S')
# for item in ss:
#    if item['classcode'] == '21S01060L300002021S':
#        print(item)
#     # s1 = Student.order_create('135737561', ['22W01060L300097021S', '22P01060L400097021S'])
#     # Student.order_check(ordercode=s1)
# print(Student.studentinfo(parentmobile='15150420012'))
# print(Student.stuclass('156474431'))
#     Student.order_check(parentmobile='15811326167')
# Student.stuquit_check()

#     # 外部订单审核
#     student.order_check('11002105123783817311')
# student.stuclassif('311614491', '21S01060L300002021S')
# student.studentinfo(parentmobile='')
# student.stuquit_check('13811494438')
# student.stuclassif('188311118','21A21010L100073021S')
# print(student.stuclass('188311118'))
# print(student.studentinfo('17190084003', '测试张'))
# student.classinfo('21A21010L10u0073021S')
# classcodelist = ['21A21010L100073021S', '21A21010L100074121A']
#     order1 = student.order_create('149851325', classcodelist)
#     time.sleep(2)
#     student.order_check(order1)
