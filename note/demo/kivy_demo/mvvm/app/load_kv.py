
import os
import pickle

from kivy.lang.builder import Builder

work_path = os.getcwd()
try:
    with open("ui/kv/cache/ui.data", "rb") as f:
        kv_cache = pickle.load(f)
except Exception as err:
    kv_cache = dict()
    _ = err


class KvLoadException(Exception):
    def __init__(self, msg):
        self.msg = msg


class KvLoad:
    __slots__ = ()

    @staticmethod
    def load(py_file: str, **kwargs) -> None:
        kv_file = None
        try:
            if py_file.endswith(".py"):
                kv_file = py_file.replace(".py", ".kv")
            else:
                kv_file = py_file.replace(".pyc", ".kv")
            if kv_file in Builder.files:
                return

            _, r_name = os.path.abspath(kv_file).split(work_path)
            kv = kv_cache.get(r_name)
            kwargs["filename"] = kv_file
            if kv:
                Builder.load_string(kv, **kwargs)
            else:
                with open(kv_file, "r", encoding="utf-8") as fd:
                    Builder.load_string(fd.read(), **kwargs)
        except Exception as err:
            raise KvLoadException("Load {} file error:{}".format(kv_file, err))
