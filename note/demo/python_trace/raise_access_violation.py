import faulthandler_demo1
faulthandler_demo1.enable()
faulthandler_demo1.disable()
code = faulthandler_demo1._EXCEPTION_ACCESS_VIOLATION
faulthandler_demo1._raise_exception(code)