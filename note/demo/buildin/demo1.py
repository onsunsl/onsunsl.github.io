# -*- coding: utf-8 -*-
# @Project : onsunsl_github_io
# @Author  : GuangLin
# @File    : demo1.py
# @Time    : 2022/11/18 18:30
# @Email   : Guanglin.Liang@DMall.com
# @Version : 0.01
# @Desc    : 
#
# @History
# -------------------------------------------
#     Time         Author          Desc
# -------------------------------------------
import builtins

builtins.__dict__['hello'] = "a132132"

print(getattr(builtins, 'hello'))