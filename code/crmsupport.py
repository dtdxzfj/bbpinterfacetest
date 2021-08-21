from common.crmrequest import CrmRequest
from common.crmurlconf import CrmUrls
from common.crmtoolconf import CrmTools
import time
from tools.mylog import MyLog
from code.platformlogin import PlatformLogin


class CrmSupport:

    @classmethod
    def update_alpha_late(cls):
        data = {
            "id": 4,
            "code": "0004",
            "name": "基础业务平台",
            "description": "BBP",
            "url": "https://bbp-alpha.t.blingabc.com/",
            "status": 1
        }
        updatereq = CrmRequest(CrmUrls(platform='alpha').update_alpha).post(data)
        MyLog.loginfo(f'alpha环境平台数据更新：{updatereq["data"]}')

    # 更新对应环境的当前外教可用时间缓存数据
    @classmethod
    def update_tech_cache(cls, techerid):
        techreq = CrmRequest(CrmUrls().update_tech_cache).get(techerid)
        MyLog.loginfo(f'更新老师排班缓存数据：{techreq["msg"]}')

    # 更新对应环境的所有外教可用时间缓存数据，地址不太对
    @classmethod
    def update_tech_cache_all(cls):
        techallreq = CrmRequest(CrmUrls().update_tech_cache_all).get('szdhfcgvb')
        MyLog.loginfo(f"更新全部老师排班缓存数据：{techallreq['msg']}")

    # 查询外教占用情况，查询当前班级的课时是否可以排上这个外教
    @classmethod
    def get_classlesson_time(cls, classcode, teacherid):
        urldata = f'{str(classcode)}{"&foreignTeacherId="}{str(teacherid)}'
        timereq = CrmRequest(CrmUrls().get_classlesson_time).get(urldata)
        if timereq['data']:
            timedata = timereq['data']
            timedatalist = []
            for item in timedata:
                if item['availableResults']:
                    timedict = {'classLessonId': item['id'], 'beginDate': item['beginDate'], 'endDate': item['endDate'],
                                'remark': item['remark'], 'occupyClassId': item['availableResults'][0]['occupyClassId'],
                                'occupyClassLessonId': item['availableResults'][0]['occupyClassLessonId']}
                else:
                    timedict = {'classLessonId': item['id'], 'beginDate': item['beginDate'], 'endDate': item['endDate'],
                                'remark': item['remark']}
                timedatalist.append(timedict)
            else:
                MyLog.loginfo(f'外教时间占用情况：{timedatalist}')

    # 更新班级当前班容信息（仅限未结课的班级）
    @classmethod
    def update_current_contain(cls, classcode):
        req = CrmRequest(CrmUrls().update_currentcontain).get(classcode)
        time.sleep(1)
        MyLog.loginfo(req['msg'])
    # 查询当前班级还可以在报几个学员名额
    @classmethod
    def class_count(cls,classid):
        req = CrmRequest(CrmUrls().class_count).get(classid)
        time.sleep(1)
        MyLog.loginfo(f'查询班级可用名额情况：{req["msg"]}，查询可用名额数量：{req["data"]}')


if __name__ == "__main__":
    PlatformLogin.login_bbp()
    CrmSupport.update_current_contain('21A02080L400017021A')
    # CrmSupport.class_count('476201')
    # CrmSupport.update_alpha_late()
    # CrmSupport.update_tech_cache_all()
    #     CrmSupport.get_classlesson_time('21S01010L100114021S','6960')
    # classlist = ['21S01080L400001021S']
    # url = 'https://lapi-smix2.t.blingabc.com/bms/user-api/classinfo/v1/currentcontain/'
    # for item in classlist:
    #     pass
