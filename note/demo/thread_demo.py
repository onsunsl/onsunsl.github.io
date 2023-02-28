# -*- coding: utf-8 -*-
# @Project : onsunsl_github_io
# @Author  : GuangLin
# @File    : thread_demo.py
# @Time    : 2022/10/20 14:00
# @Email   : Guanglin.Liang@DMall.com
# @Version : 0.01
# @Desc    : 
#
# @History
# -------------------------------------------
#     Time         Author          Desc
# -------------------------------------------


import threading

e = threading.Event()
e.set()
e.set()

print("end")