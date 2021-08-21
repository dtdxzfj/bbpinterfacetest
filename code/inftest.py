from code.platformlogin import PlatformLogin
from common.crmrequest import CrmRequest
import time

class InfTest:

    @classmethod
    def testinterface(cls, testfile):
        with open(testfile, encoding='utf-8') as testinf, open('C:\\Users\\blingabc\\Desktop\\testout.txt', mode='a',
                                                               encoding='utf-8') as testout:
            for line in testinf:
                testurl = f'https://oapi.t.blingabc.com{line.strip()}'
                # print(testurl)
                req = CrmRequest(testurl).post()
                time.sleep(4)
                if 'status' in req:
                    if int(req['status']) == 404:
                        testout.write(f'报404：{line.strip()}\n')
                else:
                    testout.write(f'{line.strip()},{req["code"]},{req["msg"]}\n')
                    if int(req["code"]) == 500:
                        break


if __name__ == "__main__":
    PlatformLogin.login_bbp()
    InfTest.testinterface('C:\\Users\\blingabc\\Desktop\\jiekou2.txt')
