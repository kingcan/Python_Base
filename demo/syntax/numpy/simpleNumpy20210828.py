"""
# @Author: Larkin
# @Date: 2021/8/28 15:19
# @Function:
# @ModuleName:simpleNumpy20210828
"""


# 文件名称可用于访问 age 列的内容
import numpy as np
import sys

dt = np.dtype([('age', np.int8)])
a = np.array([(10,), (20,), (30,)], dtype=dt)
print(dt)#
print(a)
print(a['age'])
#输出
"""
[('age', 'i1')]//i1是int8的简称。字节数
[(10,) (20,) (30,)]
[10 20 30]
"""
student = np.dtype([('name','U10'),  ('age',  'i1'),  ('marks',  'f4')])
a = np.array([('中国',  21,  50),('xyz',  18,  75)], dtype = student)
print(a)#U代表的是Unicode编码
print(a.itemsize)#字节大小
print("中国必胜")