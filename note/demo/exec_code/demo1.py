def run_code_block(code: str, *args, **kwargs):
    namespace = {}
    fun = compile(code, '<string>', 'exec')
    exec(fun, namespace)
    return namespace['fun'](*args, **kwargs)


if __name__ == '__main__':
    codes = """
def fun(a, *args, **kwargs):
    return a+1
"""
    print(f"run:{codes}\nresult:{run_code_block(codes, 1)}")
