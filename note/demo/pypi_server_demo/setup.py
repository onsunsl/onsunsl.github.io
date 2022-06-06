# -*- coding: utf-8 -*-
# @Project : onsunsl.github.io
# @Author  : GuangLin
# @File    : setup.py
# @Time    : 2022/6/6 9:58
# @Version : 0.01
# @Desc    : 
#
# @History
# -------------------------------------------
#     Time         Author          Desc
# -------------------------------------------
from setuptools import setup

REQUIRES = [

]

INDEX_URLS = [
    # your pypi server link
    # "https://pypi.douban.com/simple/"
]


setup(
    name="first_package",
    version="0.0.1",
    # 依赖的模块
    install_requires=REQUIRES,

    # 依赖模块安装源
    dependency_links=INDEX_URLS,
    description="Test my pypi server",
    author="Onunsl",
    author_email="Onsunsl@foxmail.com",
    url="https://www.jili.ink",
    packages=["first_package"],
    include_package_data=True,
    platforms=["Windows"],
    package_data={
        "first_package.data": ["first_package/data/*"]
    }
)
