# Copyright (c) 2022, Riverbank Computing Limited
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
# 
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.


PY_MAJOR_VERSION = @PY_MAJOR_VERSION@
PY_MINOR_VERSION = @PY_MINOR_VERSION@
PY_PATCH_VERSION = @PY_PATCH_VERSION@
PY_DYNAMIC_LOADING = @PY_DYNAMIC_LOADING@

!defined(SYSROOT, var) {
    error("SYSROOT must be defined on the qmake command line")
}

TEMPLATE = lib

win32 {
    TARGET = python$${PY_MAJOR_VERSION}$${PY_MINOR_VERSION}
} else {
    TARGET = python$${PY_MAJOR_VERSION}.$${PY_MINOR_VERSION}
}

CONFIG -= qt
CONFIG += warn_off staticlib

# Work around QTBUG-39300.
CONFIG -= android_install

OBJECTS_DIR = .obj

DEFINES += NDEBUG Py_BUILD_CORE

# These are needed by getpath.c but the actual values don't matter too much as
# the path is set properly elsewhere.
DEFINES += VERSION=\\\"$${PY_MAJOR_VERSION}.$${PY_MINOR_VERSION}\\\"
DEFINES += VPATH=\\\".\\\"
DEFINES += PREFIX=\\\"/\\\"
DEFINES += EXEC_PREFIX=\\\"/\\\"
DEFINES += PYTHONPATH=\\\"/lib/python$${PY_MAJOR_VERSION}.$${PY_MINOR_VERSION}\\\"

greaterThan(PY_MINOR_VERSION, 8) {
    DEFINES += PLATLIBDIR=\\\"lib\\\"
}

INCLUDEPATH += . Include

greaterThan(PY_MINOR_VERSION, 7) {
    INCLUDEPATH += Include/internal
}

win32 {
    DEFINES += PLATFORM=\\\"win32\\\"

    greaterThan(PY_MINOR_VERSION, 9) {
        DEFINES += PY3_DLLNAME=\\\"python3\\\"
    }

    INCLUDEPATH += PC
} else {
    android {
        DEFINES += PLATFORM=\\\"linux\\\"
        DEFINES += MULTIARCH=\\\"android\\\"
        ANDROID_ABIS = @ANDROID_ABIS@
    }
    ios {
        DEFINES += PLATFORM=\\\"darwin\\\"
        DEFINES += MULTIARCH=\\\"ios\\\"
    }
    macx {
        DEFINES += PLATFORM=\\\"darwin\\\"
        DEFINES += MULTIARCH=\\\"darwin\\\"
    }
    linux-* {
        DEFINES += PLATFORM=\\\"linux\\\"
        DEFINES += MULTIARCH=\\\"x86_64-linux-gnu\\\"
    }

    DEFINES += ABIFLAGS=\\\"m\\\"

    QMAKE_CFLAGS_RELEASE = -O3
    QMAKE_CFLAGS += -fwrapv

    greaterThan(PY_MINOR_VERSION, 10) {
        QMAKE_CFLAGS += -std=c11
    } else {
        QMAKE_CFLAGS += -std=c99
    }
}

target.path = $$SYSROOT/lib

headers.path = $$SYSROOT/include/python$${PY_MAJOR_VERSION}.$${PY_MINOR_VERSION}
headers.files = pyconfig.h Include/*.h

greaterThan(PY_MINOR_VERSION, 7) {
    headers.files += Include/cpython Include/internal
}

stdlib.path = $$SYSROOT/lib/python$${PY_MAJOR_VERSION}.$${PY_MINOR_VERSION}
stdlib.files = Lib/*

INSTALLS += target headers stdlib

PARSER_SOURCES = Parser/myreadline.c Parser/tokenizer.c

greaterThan(PY_MINOR_VERSION, 9) {
    PARSER_SOURCES += \
        Parser/pegen.c \
        Parser/parser.c \
        Parser/string_parser.c \
        Parser/peg_api.c

    greaterThan(PY_MINOR_VERSION, 10) {
        PARSER_SOURCES += \
            Parser/pegen_errors.c \
            Parser/action_helpers.c
    }

    PARSER_SOURCES += \
        Parser/token.c
} else {
    PARSER_SOURCES += \
        Parser/acceler.c \
        Parser/grammar1.c \
        Parser/listnode.c \
        Parser/node.c \
        Parser/parser.c \
        Parser/parsetok.c

    greaterThan(PY_MINOR_VERSION, 8) {
        PARSER_SOURCES += \
            Parser/pegen/pegen.c \
            Parser/pegen/parse.c \
            Parser/pegen/parse_string.c \
            Parser/pegen/peg_api.c
    }

    greaterThan(PY_MINOR_VERSION, 7) {
        PARSER_SOURCES += \
            Parser/token.c
    } else {
        PARSER_SOURCES += \
            Parser/bitset.c \
            Parser/metagrammar.c \
            Parser/firstsets.c \
            Parser/grammar.c \
            Parser/pgen.c
    }
}

OBJECT_SOURCES = \
    Objects/abstract.c \
    Objects/accu.c \
    Objects/boolobject.c \
    Objects/bytes_methods.c \
    Objects/bytearrayobject.c \
    Objects/bytesobject.c \
    Objects/call.c \
    Objects/capsule.c \
    Objects/cellobject.c \
    Objects/classobject.c \
    Objects/codeobject.c \
    Objects/complexobject.c \
    Objects/descrobject.c \
    Objects/enumobject.c \
    Objects/exceptions.c \
    Objects/genobject.c \
    Objects/fileobject.c \
    Objects/floatobject.c \
    Objects/frameobject.c \
    Objects/funcobject.c \
    Objects/iterobject.c \
    Objects/listobject.c \
    Objects/longobject.c \
    Objects/dictobject.c \
    Objects/odictobject.c \
    Objects/memoryobject.c \
    Objects/methodobject.c \
    Objects/moduleobject.c \
    Objects/namespaceobject.c \
    Objects/object.c \
    Objects/obmalloc.c \
    Objects/rangeobject.c \
    Objects/setobject.c \
    Objects/sliceobject.c \
    Objects/structseq.c \
    Objects/tupleobject.c \
    Objects/typeobject.c \
    Objects/unicodeobject.c \
    Objects/unicodectype.c \
    Objects/weakrefobject.c

greaterThan(PY_MINOR_VERSION, 9) {
    OBJECT_SOURCES += \
        Objects/unionobject.c
}

greaterThan(PY_MINOR_VERSION, 7) {
    OBJECT_SOURCES += \
        Objects/interpreteridobject.c \
        Objects/picklebufobject.c
}

greaterThan(PY_MINOR_VERSION, 8) {
    OBJECT_SOURCES += \
        Objects/genericaliasobject.c
}

PYTHON_SOURCES = \
    Python/_warnings.c \
    Python/Python-ast.c \
    Python/asdl.c \
    Python/ast.c \
    Python/ast_opt.c \
    Python/ast_unparse.c \
    Python/bltinmodule.c \
    Python/ceval.c \
    Python/codecs.c \
    Python/compile.c \
    Python/context.c \
    Python/dynamic_annotations.c \
    Python/errors.c \
    Python/frozenmain.c \
    Python/future.c \
    Python/getargs.c \
    Python/getcompiler.c \
    Python/getcopyright.c \
    Python/getplatform.c \
    Python/getversion.c \
    Python/hamt.c \
    Python/import.c \
    Python/importdl.c \
    Python/marshal.c \
    Python/modsupport.c \
    Python/mysnprintf.c \
    Python/mystrtoul.c \
    Python/pathconfig.c \
    Python/pyarena.c \
    Python/pyctype.c \
    Python/pyfpe.c \
    Python/pyhash.c \
    Python/pylifecycle.c \
    Python/pymath.c \
    Python/pystate.c \
    Python/pythonrun.c \
    Python/pytime.c \
    Python/bootstrap_hash.c \
    Python/structmember.c \
    Python/symtable.c \
    Python/sysmodule.c \
    Python/thread.c \
    Python/traceback.c \
    Python/getopt.c \
    Python/pystrcmp.c \
    Python/pystrtod.c \
    Python/pystrhex.c \
    Python/dtoa.c \
    Python/formatter_unicode.c \
    Python/fileutils.c

win32 {
    PYTHON_SOURCES += \
        PC/invalid_parameter_handler.c
}

greaterThan(PY_MINOR_VERSION, 10) {
    PYTHON_SOURCES += \
        Python/Python-tokenize.c \
        Python/frame.c \
        Python/specialize.c
}

greaterThan(PY_MINOR_VERSION, 9) {
    PYTHON_SOURCES += \
        Python/suggestions.c
}

lessThan(PY_MINOR_VERSION, 10) {
    PYTHON_SOURCES += \
        Python/graminit.c \
        Python/peephole.c
}

greaterThan(PY_MINOR_VERSION, 7) {
    PYTHON_SOURCES += \
        Python/initconfig.c \
        Python/preconfig.c
}

greaterThan(PY_MINOR_VERSION, 8) {
    PYTHON_SOURCES += \
        Python/hashtable.c
}

equals(PY_DYNAMIC_LOADING, "enabled") {
    DEFINES += SOABI=\\\"cpython-$${PY_MAJOR_VERSION}$${PY_MINOR_VERSION}\\\"

    win32 {
        PYTHON_SOURCES += Python/dynload_win.c
    } else {
        PYTHON_SOURCES += Python/dynload_shlib.c
    }
}

MODULE_SOURCES = \
    Modules/config.c \
    Modules/main.c \
    Modules/gcmodule.c

greaterThan(PY_MINOR_VERSION, 10) {
    MODULE_SOURCES += \
        Modules/getpath.c

    win32 {
        MODULE_SOURCES += \
            PC/dl_nt.c
    }
} else {
    win32 {
        MODULE_SOURCES += \
            PC/getpathp.c
    } else {
        MODULE_SOURCES += \
            Modules/getpath.c
    }
}

MOD_SOURCES = \
    Modules/atexitmodule.c \
    Modules/faulthandler.c \
    Modules/posixmodule.c \
    Modules/signalmodule.c \
    Modules/_tracemalloc.c \
    Modules/_codecsmodule.c \
    Modules/_collectionsmodule.c \
    Modules/errnomodule.c \
    Modules/_io/_iomodule.c \
    Modules/_io/iobase.c \
    Modules/_io/fileio.c \
    Modules/_io/bytesio.c \
    Modules/_io/bufferedio.c \
    Modules/_io/textio.c \
    Modules/_io/stringio.c \
    Modules/itertoolsmodule.c \
    Modules/_threadmodule.c \
    Modules/timemodule.c \
    Modules/_weakref.c \
    Modules/_functoolsmodule.c \
    Modules/_localemodule.c \
    Modules/_operator.c \
    Modules/_stat.c \
    Modules/symtablemodule.c

win32 {
    MOD_SOURCES += \
        Modules/_io/winconsoleio.c \
        PC/msvcrtmodule.c \
        PC/winreg.c
} else {
    MOD_SOURCES += \
        Modules/pwdmodule.c
}

greaterThan(PY_MINOR_VERSION, 10) {
    MOD_SOURCES += \
        Modules/_abc.c \
        Modules/_sre/sre.c
} else {
    MOD_SOURCES += \
        Modules/_sre.c
}

lessThan(PY_MINOR_VERSION, 9) {
    MOD_SOURCES += \
        Modules/hashtable.c
}

isEqual(PY_MINOR_VERSION, 7) {
    MOD_SOURCES += Modules/zipimport.c

    lessThan(PY_PATCH_VERSION, 3) {
        win32 {
            # Work around the PyVarObject_HEAD_INIT() problem in Python v3.7.0
            # to v3.7.2 by always compiling this module.
            MOD_SOURCES += Modules/_abc.c
        }
    }
}

isEqual(PY_MINOR_VERSION, 9) {
    MOD_SOURCES += \
        Modules/_peg_parser.c
}

SOURCES = Modules/getbuildinfo.c
SOURCES += $$PARSER_SOURCES
SOURCES += $$OBJECT_SOURCES
SOURCES += $$PYTHON_SOURCES
SOURCES += $$MODULE_SOURCES
SOURCES += $$MOD_SOURCES
