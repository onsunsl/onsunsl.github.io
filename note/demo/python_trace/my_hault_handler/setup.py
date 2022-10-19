from setuptools import setup
from setuptools import Extension
from Cython.Build import cythonize


# c 写实现的模块
c_extensions = list()
c_extensions.append(Extension("faulthandler2", ["faulthandler2.c"]))

setup(
    name="faulthandler2",
    version="0.0.1",
    description="Just test my package",
    author="Onsunsl",
    author_email="Onsunsl@foxmail.com",
    url="https://www.jili.ink",
    ext_modules=c_extensions,
)


