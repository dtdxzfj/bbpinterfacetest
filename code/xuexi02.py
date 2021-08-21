'''
9、随机输入5个数，输出最大值和最小值：

10、判断字符串中字母，数字，下划线的个数。's3j_d67h_a5s624b_u'


11、单位给发了一张150元购物卡，拿着到超市买三类洗化用品。洗发水15元，香皂2元，牙刷5元。
求刚好花完150元，有多少种买法，每种买法都是各买几样？

12、求s=a+aa+aaa+aaaa+.....,其中a是一个数字，例如2+22+222+2222+.....，input输入时几个数相加，a是那个数字

'''


class XueXi02:

    def d01(self):
        sum = 0
        for i in range(0, 101, 3):
            sum += i
        print(sum)

    def d02(self):
        s = int(input("请输入一个数："))
        for i in range(1, s + 1):
            if s % i == 0:
                print(i)

    def d03(self):
        s = str(input("请输入数字："))
        count = 0
        max_num = 0
        for i in s:
            if i == '0':
                count += 1
            if int(i) > max_num:
                max_num = int(i)
        else:
            print('零的个数为{a},各位数字中的最大为{b}'.format(a=count, b=max_num))

    def d05(self):
        x2 = 1
        x1 = 0
        for day in range(1, 10):
            x1 = (x2 + 1) * 2
            x2 = x1
        print(x1)

    def d06(self):
        score = []
        for i in range(1, 6):
            num = int(input("第{}门成绩:".format(i)))
            if num < 0:
                print("录入错误")
                break
            score.append(num)
        else:
            print(score)

    def d08(self):
        n = int(input("请输入数字："))
        s = 0
        for i in range(1, n):
            s += (i + 1) / i
        else:
            print(s)

    def d10(self):
        string = 's3j_d67242yuhaT5sh__fuYcz212 4d2ea624b_u'
        import re
        pattern = {'数字总数：': r'\d', '字母总数：': r'[a-z]|[A-Z]', '下划线总数：': r'\_'}
        for k,v in pattern.items():
            print(k,len(re.findall(v, string)))

    def d11(self):
        a = 0  # 洗发水
        b = 0  # 香皂
        c = 0  # 牙刷
        count = 0
        for x in range(int(150 / 15 + 1)):
            for y in range(int(150 / 2 + 1)):
                for z in range(int(150 / 5 + 1)):
                    if 15 * x + 2 * y + 5 * z == 150:
                        count += 1
                        print("第{q}种买法，洗发水个数为：{w}，香皂个数为：{e}牙刷个数为：{r} ,".format(q=count, w=a, e=b, r=c))
        else:
            print("一共{a}种买法,".format(a=count))

    def d12(self, a, n):
        s = 0
        ss = 0
        for i in range(n):
            s += (10 ** i) * a
            ss += s
            print(i, s, ss)
        else:
            return ss

    def d13(self):
        for j in range(2, 101):
            k = []
            n = -1
            s = j
            for i in range(1, j):
                if j % i == 0:
                    n += 1
                    s -= i
                    k.append(i)

            if s == 0:
                print(j, *[a for a in k])

    def d14(self):
        L1 = 100
        L2 = L1 / 2
        for n in range(2, 11):
            L1 += 2 * L2
            L2 /= 2

        print(L1, L2)

    def d15(self):
        a = 2.0
        b = 1.0
        s = 0.0
        for n in range(1, 21):
            s += a / b
            b, a = a, a + b
        else:
            print(s)

    def d18(self, n):
        print(__name__)
        if n == 1:
            c = 10
        else:
            c = self.d18(n - 1) + 2
        return c

    def d19(self):
        from tools.mylog import MyLog
        s = str(input("请输入一个5位数:"))
        for i in range(0, 3):
            if s[i] == s[4 - i]:
                print("是回文数")
                MyLog.loginfo('cesi ')
                break
        else:
            print("不是回文数")

    def d20(self):
        for n in range(100, 1001):
            i = int(n / 100)  # 百位数
            j = int(n % 10)  # 个位数
            k = int((int(n / 10)) / 10)  # 十位数
            # print(i, k, j)
            if i ** 3 + j ** 3 + k ** 3 == n:
                print(n)

            # else:
            #     print("不存在这样的数字")

    def hongbao(self, sum, num):
        import random
        listd = random.sample(range(0, sum * 100), num - 1)
        listd.sort()
        # listn = [0] + listd + [sum * 100]
        listd.insert(0, 0)
        listd.append(sum * 100)
        listn = listd
        # hb = []
        for i in range(len(listn) - 1):
            item = yield (listn[i + 1] - listn[i]) / 100
            return item
            # print(item.__n)
            # item = (listn[i+1]-listn[i])/100
            # hb.append(item)
        # print(hb)
        # return hb


if __name__ == "__main__":
    XueXi02().d10()
    # for ii in range(4):
    import time
    # a = time.time()
    # for o in range(10):
    # ii = XueXi02().hongbao(200, 10).__next__()
    #     # o+=1
    # print(ii,end='-')
    # b =time.time()
    # time.sleep(1)
    # print(b-a)
    # d18(2)
    # print(XueXi02().__dict__,XueXi02().__dir__(),XueXi02().__str__())
    # s = 'hjdaksnasldkasj'
    import inspect
    # from
    # print(*[[i,j] for i,j in enumerate(s)])
    # print(sys.modules,)
