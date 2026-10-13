import re

s = "手机号是:16563789354,另一个手机号是:18547289365,QQ号是:15764529876"
s1 = "16563789354是手机号,另一个手机号是:18547289365,QQ号是:15764529876"

"""
输出结果:
match: 没匹配到（手机号不在开头）
==============================
match: 16563789354
==============================
match: 16563789354
==============================
match: ['16563789354', '18547289365', '15764529876']
"""

#match -- 从字符串的开头开始匹配,返回Match对象
result = re.match(r"1[3-9]\d{9}",s)
if result:
    print("match:", result.group())
else:
    print("match: 没匹配到（手机号不在开头）")

print("==============================")

result = re.match(r"1[3-9]\d{9}", s1)
if result:
    print("match:", result.group())
else:
    print("match: 没匹配到（手机号不在开头）")

print("==============================")

#search -- 从任意位置开始匹配,搜索第一个匹配项,返回Match对象
result_1 = re.search(r"1[3-9]\d{9}",s)
if result_1:
    print("match:", result_1.group())
else:
    print("match: 没匹配到（手机号不在开头）")

print("==============================")

#findall -- 从任意位置开始匹配,搜索所有匹配项,返回列表
result_2 = re.findall(r"1[3-9]\d{9}",s)
if result_2:
    print("match:", result_2)
else:
    print("match: 没匹配到（手机号不在开头）")