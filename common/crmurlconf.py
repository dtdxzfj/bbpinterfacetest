from tools.rwconfig import RWConfig
from tools.mylog import MyLog

"""
存放所有接口的地址信息


"""


class CrmUrls:

    # 读取配置文件，初始化登录环境配置
    def __init__(self, platform=None):
        if platform is None:
            platform = RWConfig.read_config('platform', 'platform')
        platform_url = {'smix2': 'https://lapi-smix2.t.blingabc.com', 'alpha': 'https://oapi-alpha.t.blingabc.com',
                        'official': 'https://lapi.blingabc.com', 't': 'https://oapi.t.blingabc.com',
                        'smix1': 'https://oapi-smix1.t.blingabc.com'}
        if platform in platform_url.keys():
            self.url = platform_url[platform]
        else:
            MyLog.logwarning('登录平台存在错误！')

        # ar平台或者crm平台登录接口
        self.login = f'{self.url}/auth/open-api/login/v1/get-login-info'

        # support模块支持接口url
        # 更新alpha环境基础平台表数据
        self.update_alpha = f'{self.url}/bms/user-api/platform/v1/update'
        # 更新外教老师可用时间缓存
        self.update_tech_cache = f'{self.url}/share-schedule/user-api/foreign-teacher/update-single?foreignTeacherId='
        # 批量更新外教老师可用时间缓存 暂不可用，域名不对
        self.update_tech_cache_all = f'{self.url}/share-schedule/user-api/foreign-teacher/re-init'
        # 查询班级和对应外教的时间占用情况
        self.get_classlesson_time = f'{self.url}/bms/user-api/scheduleclass/v1/schedule-check?classCode='
        # 更新班级当前班容信息
        self.update_currentcontain = f'{self.url}/bms/user-api/classinfo/v1/currentcontain/'
        # 查询当前班级可报班名额
        self.class_count = f'{self.url}/bms/user-api/classinfo/v1/redis/count/'

        # 课时添加接口
        self.lesson_add = '{url}/bms/user-api/lesson/v1/insert'.format(url=self.url)
        # 课时ID查询，由于课时创建之后接口不返回对应ID等信息，需要主动查询
        self.lesson_info = '{url}/bms/user-api/lesson/v1/lessons'.format(url=self.url)
        # 课时发布
        self.lesson_state = '{url}/bms/user-api/lesson/v1/update/state'.format(url=self.url)
        # 课时撤销发布
        self.lesson_offstate = '{url}/bms/user-api/lesson/v1/off-shelf'.format(url=self.url)
        # 课时废弃
        self.lesson_batch = '{url}/bms/user-api/lesson/v1/batch/status'.format(url=self.url)

        # 组课
        self.course_add = '{url}/bms/user-api/course/v1/insert'.format(url=self.url)
        # 课程查询
        self.course_info = '{url}/bms/user-api/course/v1/courses'.format(url=self.url)
        # 课程发布
        self.course_state = '{url}/bms/user-api/course/v1/update'.format(url=self.url)
        # 课程课时信息
        self.course_lesson = '{url}/bms/user-api/course/v1/courses/'.format(url=self.url)
        # 课程废弃
        self.course_batch = '{url}/bms/user-api/course/v1/batch/status'.format(url=self.url)

        # 班级模板创建
        self.temp_add = '{url}/bms/user-api/template/v1/insert'.format(url=self.url)
        # 模板查询
        self.temp_info = '{url}/bms/user-api/template/v1/templates'.format(url=self.url)
        # 模板开班
        self.temp_openclass = '{url}/bms/user-api/classinfo/v1/create'.format(url=self.url)
        # 模板废弃
        self.temp_abandon = '{url}/bms/user-api/template/v1/batch/abandon'.format(url=self.url)

        # 更新班级为发布状态
        self.class_state = '{url}/bms/user-api/classinfo/v2/batch/release?ids='.format(url=self.url)
        # 更新班级渠道信息
        self.class_channel = '{url}/bms/user-api/classinfo/v1/update-classinfo'.format(url=self.url)
        # 班级管理查询新
        self.class_info = '{url}/bms/user-api/classinfo/v1/classInfos'.format(url=self.url)
        # 查询班级报班学生信息，班级课时信息
        self.class_studentinfo = '{url}/bms/user-api/studentlesson/v1/stuclass/'.format(url=self.url)
        # 配置班级上课时间
        self.class_time = '{url}/bms/user-api/classinfo/v1/edit-time'.format(url=self.url)
        # 查询班级可排外教老师：
        self.class_foreignteacher = '{url}/bms/user-api/foreignteacher/v1/list'.format(url=self.url)
        # 查询中教老师
        self.class_chinesetecher = '{url}/bms/user-api/foreign/headmaster/v1/headmaster_list_page'.format(url=self.url)
        # 安排班级外教或者中教老师(可以直接指定）
        self.class_editteacher = '{url}/bms/user-api/classinfo/v1/edit-teacher'.format(url=self.url)
        # 班级下架
        self.class_offstate = '{url}/bms/user-api/classinfo/v2/batch/offshelves?ids='.format(url=self.url)
        # 班级废弃
        self.class_abandon = '{url}/bms/user-api/classinfo/v1/batch/abandon'.format(url=self.url)

        # 查询家长信息
        self.parent = '{url}/bms/user-api/parent/v1/info/mobile?mobile='.format(url=self.url)
        # 查询学生信息
        self.student = '{url}/bms/user-api/student/v1/studentlist?parentNum='.format(url=self.url)
        # 学员下单
        self.order_create = '{url}/bms/user-api/order/v1/create'.format(url=self.url)
        # 获取课程优惠信息（等待完善）
        self.order_favourable = f'{self.url}/bms/user-api/order/v1/caleCourseFavourablePrice'
        # 订单id查询
        self.order_id = '{url}/bms/user-api/order/v2/order-list-page/order-code?page=1&size=10&orderCode='.format(
            url=self.url)
        # 账号id等信息获取
        self.user_info = f'{self.url}/bms/user-api/usermanage/v1/userroles?page=1&size=10'
        # 订单审核列表
        self.order_info = f'{self.url}/bms/user-api/order/v2/check/order-list-page?page=1&size=30&checkStatus=0'
        # 订单审核
        self.order_check = '{url}/bms/user-api/order/v2/check'.format(url=self.url)
        # 退班审核列表
        self.class_quit_info = '{url}/bms/user-api/classQuit/v1/quits/unreview'.format(url=self.url)
        # 退班审核
        self.class_quit_check = '{url}/bms/user-api/classQuit/v1/review'.format(url=self.url)
        # 报班成功之后查询学生所在班级列表信息
        self.student_class = '{url}/bms/user-api/classinfo/v1/stuClasses'.format(url=self.url)

        # 筛选出待排班
        self.resubmit_info = '{url}/bms/user-api/initclass/v1/original/list'.format(url=self.url)
        # 一键开续班
        self.resubmit_class = '{url}/bms/user-api/initclass/v1/original/resubmit'.format(url=self.url)
        # 续班生成情况
        self.resubmit_class_info = '{url}/bms/user-api/progress/v1/query/'.format(url=self.url)
        # 续班上课周期变换
        self.resubmit_time = '{url}/bms/user-api/resubmittimeConfig/v1/save'.format(url=self.url)
        # 续班上周周期查询
        self.resubmit_time_info = f'{self.url}/bms/user-api/resubmittimeConfig/v1/page'

# if __name__ == "__main__":
#     print(CrmUrls('t').login)
