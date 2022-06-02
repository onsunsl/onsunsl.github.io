//
// Created by guanglin.liang on 2022/6/2.
//
#include<Python.h>

// c_fib 方法实现
static PyObject * c_fib(PyObject *self, PyObject *args) {

    long n;
    // 提取参数转成long 赋给n
    if (!PyArg_ParseTuple(args, "l", &n)) {
        PyErr_Format(PyExc_ValueError, "参数需要long类型, 而不是 %s", Py_TYPE(n) -> tp_name);
        return NULL;
    }
    long i;
    long a = 0, b = 1, tmp;
    for (i = 0; i < n; i++){
        tmp = a; a = a + b; b = tmp;
    }
    return Py_BuildValue("l", a);
}

// python 模块方法结构
// {name, method, flags, doc}
// 即 {名称，包装函数，哪种argument形式如METH_VARARGS 和 METH_KEYWORDS， 描述}
// c_fib模块方法声明
static PyMethodDef  c_fibMethods[] = {
        {"c_fib", c_fib, METH_VARARGS, "这个是c_fib"},
        {NULL, NULL, 0, NULL} // 以 NULL 作结
};

// python 模块结构
// {base, name, doc, size, module methods 表}
// 即 {PyModuleDef_HEAD_INIT, 名字， 描述， 分配内存大小， module 方法列表}
// c_fib 模块结构声明
static struct PyModuleDef c_fib_module = {
        PyModuleDef_HEAD_INIT,
        "c_fib",
        "这个是用C实现的fib模块.",
        -1, // global state
        c_fibMethods
};


// import c_fib 时会调用必须以PyInit_开头
PyMODINIT_FUNC PyInit_c_fib(){
    return PyModule_Create(&c_fib_module);
}