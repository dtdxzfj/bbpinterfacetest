# import collections


class xuexi:

    def s01(self):
        # 使用列表嵌套列表
        namedict = [["姓名：", ""], ["籍贯：", ""], ["年龄：", ""], ["手机：", ""], ["工作：", ""], ["住址：", ""]]
        for i in range(0, len(namedict) - 1):
            # print(namedict[i])
            namedict[i][1] = input("请输入您的{info}".format(info=namedict[i][0]))
        print('=========我的名片=========')
        for j in range(0, len(namedict) - 1):
            print("{a} {b}".format(a=namedict[j][0], b=namedict[j][1]))
        print('==========================')
        # else:
        #     print('=========我的名片=========')
        #     print(lambda x, y: namedict[0], namedict[1])
        # print('==========================')

    def s02(self):
        for i in range(1, 101):
            if i % 2 == 0:
                print(i)

    def s03(self):
        for i in range(6):
            print(" *" * i)

    def s04(self):
        for i in range(10):
            for j in range(1, i + 1):
                print("{a}*{b}={c} ".format(a=i, b=j, c=i * j), end='')
            print()

    def s05(self):
        # while True:
        for i in range(6):
            print(" *" * i)
        for j in range(4, 0, -1):
            print(" *" * j)
        # break

    def s06(self):
        # 变量初始化
        day = 22
        money = 6
        i = 1
        sum = int(0)
        # 费用计算，使用for或者while都可以
        for i in range(1, day + 1):
            if sum < 101:
                sum += 2 * money
                # print(i, sum)
            elif sum < 151:
                sum += 2 * money * 0.8
                print(i, sum)
            else:
                sum += 2 * money * 0.5
                print(i, sum)
            i += 1
        else:
            print("您的总消费金额为：{s}元".format(s=sum))

    def s07(self):
        str1 = '1234567890'
        print("截取第一位到第三位的字符：{s}".format(s=str1[0:3]))
        print("截取字符串最后三位的字符：{s}".format(s=str1[-3:]))
        print("截取字符串的第七个字符到结尾：{s}".format(s=str1[6:]))
        print("截取字符串的第一位到倒数第三位之间的字符：{s}".format(s=str1[0:-3]))
        print("截取字符串的倒数第一个字符：{s}".format(s=str1[-1]))
        print("截取字符串的第三个字符：{s}".format(s=str1[2]))
        print("截取与原字符串顺序相反的字符串：{s}".format(s=str1[::-1]))
        print("截取字符串的第一位字符到最后一位字符之间的字符，每隔一个字符截取一次：{s}".format(s=str1[::2]))

    def s08(self):
        list = [12, 3, 23, 2, 5, 45, 4, 54, 6, 561, 5, 7, 5, 4, 456, 45, 6, 456, 56, 4]
        list.sort()
        print("最大值：{da}".format(da=list[-1]))
        print("最小值：{xa}".format(xa=list[0]))

    def s09(self):
        # s =collections.Counter('fghjghjg6f6fyu')
        # 解题思路参考网络，这个题目一时之间没有想到办法
        str = "fas favc  regsdf asd"
        strdict = {}
        for i in str:
            if i != ' ':  # 判断是否有空格，有则直接跳过空格计数
                if i in strdict:
                    strdict[i] += 1
                else:
                    strdict[i] = 1
            else:
                i = str[str.count(i) + 1]
        print(strdict)

    def s10(self):
        """
        搁置，需要建类初始化函数之后弄
        def add(self,name,args)

        :return:
        """
        pass

    def s11(self):
        str = input("请输入需要反转的字符串：")
        print("字符串反转为：{s}".format(s=str[::-1]))

    def s12(self):
        str = "你好\t或打算\thkjas hdj hjh\thjkhg jj"
        print(str.split()[-2])  # split方法默认使用空格分隔，\t可以自动分隔

    def s13(self):
        alist = [1, 2, 3, 4]
        # aset = {...}
        a = 0
        for i in alist:
            for j in alist:
                for k in alist:
                    if i == j and j == k:
                        continue
                    else:
                        print(i, j, k)
                        a += 1
        print("数量为：{sum}".format(sum=a))

    def s14(self):
        p = int(input("请输入利润（万元）："))
        price = 0  # 奖金数
        if p <= 10:
            price += p * 0.1
        elif p <= 20:
            price += 10 * 0.1 + (p - 10) * 0.075
        elif p <= 40:
            price += 10 * 0.1 + 10 * 0.075 + (p - 20) * 0.05
        elif p <= 60:
            price += 10 * 0.1 + 10 * 0.075 + 20 * 0.05 + (p - 40) * 0.03
        elif p <= 100:
            price += 10 * 0.1 + 10 * 0.075 + 20 * 0.05 + (p - 60) * 0.015
        else:
            price += 10 * 0.1 + 10 * 0.075 + 20 * 0.05 + 40 * 0.015 + (p - 100) * 0.01
        print("您的奖金为：{p1}".format(p1=price))

    def s15(self):
        # import math  # 需要引入python的math库
        # sq = math.sqrt(13)
        # 由于题目中没有给定一个范围，这个暂时无法实现
        # print(sq)
        pass

    def s16(self):
        # import math  # 需要引入python的math库
        pass

    def s17(self):
        adate = str(input("请输入年月日："))
        year = int(adate[:4])
        m = int(adate[4:6])
        d = int(adate[6:])
        datelist = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        day = 0
        i = 1
        if year % 4 or year % 400 or year % 100:
            day += 1
        for i in range(1, m):
            # while i < m:
            day += datelist[i]
            # i += 1
            # print(i)
        day += d
        # print(year, m, d)
        print("天数：{dd}".format(dd=day))

    def s18(self):
        # list排序问题
        pass

    def s19(self):
        # 假设12个月，兔子总数按对算，属于斐波那契数列
        result_list = []
        a, b = 0, 1
        n = 10
        while n > 0:
            result_list.append(b)
            a, b = b, a + b  # 学习，元祖赋值，类似于函数传参，等同于(a, b) = (b, a+b)
            n -= 1

        print(result_list)

    def s20(self):
        # 学习，使用for （break） else 语句
        for num in range(101, 201):
            for i in range(2, num):
                if (num % i) == 0:
                    print(num, "不是质数")
                    print(i, "乘于", num // i, "是", num)
                    break
            else:
                print(num, "是质数")


# if __name__ == "__main__":
#     l2 = ['name', 'age']
#     dic2 = dict(l2)
#     print(dic2)
    # xuexi().s01()
    # names = ['Bob', 'Alice', 'Guido']
    # print([*names[:2],*names[:1]])
    # for index, value in enumerate(names,1):
    #     print(f'{index}: {value}')

# import time
#
# def strtime( date):
#     a = "{d} 00:00:00".format(d=date)
#     s = time.strptime(a, "%Y-%m-%d %H:%M:%S")  # 格式化当前元组,先传日期类型字符串，后传格式参数
#     ss = int(time.mktime(s))
#     print(ss)

# time.time()# 获取当前时间戳
# # time.localtime()  获取当前时间元组，
# time.strptime("需要格式化的字符串，精确到秒","格式化的规则，常见：%Y-%m-%d %H:%M:%S")
# Y表示完整的年，例如2021，y表示两位数的年，21，返回时间元组
# time.mktime() # 传入时间元组，返回时间戳，与localtime正好相反
# time.localtime() # 传入时间戳，返回时间
# 不论时间戳转换日期还是日期转换时间卓，都需要格式化时间，然后进行转换


# strtime("2021-03-29")

