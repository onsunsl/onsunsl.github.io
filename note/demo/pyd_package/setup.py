from setuptools import setup
from setuptools import Extension
from Cython.Build import cythonize

# cython 实现的模块
pyx_extensions = list()
pyx_extensions.append(Extension("my_module.pyx_fib", ["my_module/py_fib.pyx"]))

# c 写实现的模块
c_extensions = list()
c_extensions.append(Extension("my_module.c_fib", ["my_module/c_fib.c"]))

# python实现的模块（也可以转成c）
# pyx_extensions.append(Extension('my_module', ['my_module/my_module.py']))
# pyx_extensions.append(Extension('sub_folder.sub_module', ['my_module/sub_folder/sub_module.py']))

extensions = c_extensions + cythonize(pyx_extensions, compiler_directives={'language_level': 2})

setup(
    name="my_module",
    version="0.0.1",
    description="Just test my package",
    author="Onsunsl",
    author_email="Onsunsl@foxmail.com",
    url="https://www.jili.ink",
    ext_modules=extensions,
    packages=["my_module", "my_module.sub_folder"],
)


