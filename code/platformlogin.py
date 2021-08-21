import requests
import json
from common.crmurlconf import CrmUrls
from common.crmtoolconf import CrmTools
from tools.rwconfig import RWConfig
from tools.mylog import MyLog


class PlatformLogin:

    @classmethod
    def login_bbp(cls):
        platform = RWConfig.read_config('platform', 'platform')
        platform_list = eval(RWConfig.read_config('platform', 'platform_list'))
        if platform in platform_list:
            cls.reqbbp = json.loads(
                requests.request('POST', url=CrmUrls().login, data=json.dumps(CrmTools.bbp_user_info_official),
                                 headers=CrmTools.bbp_header).text)
        else:
            cls.reqbbp = json.loads(
                requests.request('POST', url=CrmUrls().login, data=json.dumps(CrmTools.bbp_user_info),
                                 headers=CrmTools.bbp_header).text)
        if 'data' in cls.reqbbp:
            bbpuerinfo = cls.reqbbp['data']['userInfoVO']
            CrmTools.bbp_header["token"] = bbpuerinfo['token']
            MyLog.loginfo("bbp平台:{p}环境，登录成功！登录账号：{name}".format(p=platform, name=bbpuerinfo['username']))
            kwdict = dict(platform=platform, userid=str(bbpuerinfo['id']), username=bbpuerinfo['username'],
                          name=bbpuerinfo['name'])
            RWConfig.write_config(kwdict)
        else:
            MyLog.logwarning("登录信息有误：{msg}".format(msg=cls.reqbbp['msg']))

# if __name__ == '__main__':
#     PlatformLogin.login_bbp()
