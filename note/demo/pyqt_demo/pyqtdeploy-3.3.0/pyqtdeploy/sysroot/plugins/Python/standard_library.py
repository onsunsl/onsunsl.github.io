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


from .... import ExtensionModule, PythonModule


class CodecModule(PythonModule):
    """ Encapsulate the meta-data for a Python module that implements a codec
    in the encodings package.
    """

    def __init__(self, min_version=None, version=None, max_version=None,
            target='', deps=(), core=False):
        """ Initialise the object. """

        if isinstance(deps, str):
            deps = (deps, )

        all_deps = ('encodings', 'codecs') + deps

        super().__init__(min_version=min_version, version=version,
                max_version=max_version, target=target, deps=all_deps,
                core=core)


class CoreExtensionModule(ExtensionModule):
    """ Encapsulate the meta-data for an extension module that is always
    compiled in to the interpreter library.  These are modules that the core
    relies on and modules that can only be built with Py_BUILD_CORE defined.
    """

    def __init__(self, min_version=None, version=None, max_version=None,
            target='', internal=False, deps=(), hidden_deps=()):
        """ Initialise the object. """

        super().__init__(source=(), min_version=min_version, version=version,
                max_version=max_version, target=target, internal=internal,
                deps=deps, hidden_deps=hidden_deps, core=True)


class CorePythonModule(PythonModule):
    """ Encapsulate the meta-data for a Python module that is always required
    by an application.
    """

    def __init__(self, min_version=None, version=None, max_version=None,
            target='', internal=False, deps=(), hidden_deps=(), builtin=False):
        """ Initialise the object. """

        super().__init__(min_version=min_version, version=version,
                max_version=max_version, target=target, internal=internal,
                deps=deps, hidden_deps=hidden_deps, core=True, builtin=builtin)


# The meta-data for each module.
standard_library = {
    # These are the public modules.

    '__future__':
        PythonModule(),

    '_thread':
        CoreExtensionModule(),

    'abc':
        PythonModule(deps='_abc'),

    'aifc':
        PythonModule(
                deps=('audioop', 'chunk', 'collections', 'math', 'struct',
                        'warnings')),

    'argparse': (
        PythonModule(version=(3, 7),
                deps=('copy', 'gettext', 'os', 're', 'textwrap', 'warnings')),
        PythonModule(min_version=(3, 8),
                deps=('copy', 'gettext', 'os', 're', 'shutil', 'textwrap',
                        'warnings'))),

    'array': (
        ExtensionModule(max_version=(3, 9), source='arraymodule.c'),
        ExtensionModule(min_version=(3, 10), source='arraymodule.c',
                defines='Py_BUILD_CORE_MODULE')),

    'ast': (
        PythonModule(max_version=(3, 8),
                deps=('_ast', 'collections', 'inspect')),
        PythonModule(min_version=(3, 9),
                deps=('_ast', 'collections', 'contextlib', 'enum',
                        'inspect'))),

    'asynchat': (
        PythonModule(max_version=(3, 9), deps=('asyncore', 'collections')),
        PythonModule(min_version=(3, 10),
                deps=('asyncore', 'collections', 'warnings'))),

    'asyncore':
        PythonModule(
                deps=('errno', 'os', 'select', 'socket', 'time', 'warnings')),

    'asyncio': (
        PythonModule(version=(3, 7),
                deps=('asyncio.base_events', 'asyncio.coroutines',
                        'asyncio.events', 'asyncio.futures', 'asyncio.locks',
                        'asyncio.protocols', 'asyncio.runners',
                        'asyncio.queues', 'asyncio.streams',
                        'asyncio.subprocess', 'asyncio.tasks',
                        'asyncio.transports', '!win#asyncio.unix_events',
                        'win#asyncio.windows_events')),
        PythonModule(version=(3, 8),
                deps=('asyncio.base_events', 'asyncio.coroutines',
                        'asyncio.events', 'asyncio.exceptions',
                        'asyncio.futures', 'asyncio.locks',
                        'asyncio.protocols', 'asyncio.runners',
                        'asyncio.queues', 'asyncio.streams',
                        'asyncio.subprocess', 'asyncio.tasks',
                        'asyncio.transports', '!win#asyncio.unix_events',
                        'win#asyncio.windows_events')),
        PythonModule(min_version=(3, 9), max_version=(3, 10),
                deps=('asyncio.base_events', 'asyncio.coroutines',
                        'asyncio.events', 'asyncio.exceptions',
                        'asyncio.futures', 'asyncio.locks',
                        'asyncio.protocols', 'asyncio.runners',
                        'asyncio.queues', 'asyncio.streams',
                        'asyncio.subprocess', 'asyncio.tasks',
                        'asyncio.threads', 'asyncio.transports',
                        '!win#asyncio.unix_events',
                        'win#asyncio.windows_events')),
        PythonModule(min_version=(3, 11),
                deps=('asyncio.base_events', 'asyncio.coroutines',
                        'asyncio.events', 'asyncio.exceptions',
                        'asyncio.futures', 'asyncio.locks',
                        'asyncio.protocols', 'asyncio.runners',
                        'asyncio.queues', 'asyncio.streams',
                        'asyncio.subprocess', 'asyncio.tasks',
                        'asyncio.taskgroups', 'asyncio.timeouts',
                        'asyncio.threads', 'asyncio.transports',
                        '!win#asyncio.unix_events',
                        'win#asyncio.windows_events'))),

    'atexit':
        CoreExtensionModule(),

    'audioop':
        ExtensionModule(source='audioop.c', libs='linux#-lm'),

    'base64': (
        PythonModule(max_version=(3, 8),
                deps=('binascii', 're', 'struct', 'warnings')),
        PythonModule(min_version=(3, 9), deps=('binascii', 're', 'struct'))),

    'bdb':
        PythonModule(
                deps=('fnmatch', 'inspect', 'linecache', 'os', 'reprlib')),

    'binascii':
        ExtensionModule(source='binascii.c'),

    'binhex': (
        PythonModule(max_version=(3, 8),
                deps=('binascii', 'io', 'os', 'struct')),
        PythonModule(min_version=(3, 9), max_version=(3, 10),
                deps=('binascii', 'contextlib', 'io', 'os', 'struct',
                        'warnings'))),

    'bisect':
        PythonModule(deps='_bisect'),

    'bz2': (
        PythonModule(max_version=(3, 8),
                deps=('_compression', '_bz2', 'io', 'os', 'threading',
                        'warnings')),
        PythonModule(version=(3, 9),
                deps=('_compression', '_bz2', 'io', 'os', 'threading')),
        PythonModule(min_version=(3, 10),
                deps=('_compression', '_bz2', 'io', 'os'))),

    'calendar':
        PythonModule(deps=('datetime', 'itertools', 'locale')),

    'cgi': (
        PythonModule(version=(3, 7),
                deps=('collections.abc', 'email.message', 'email.parser',
                        'html', 'io', 'locale', 'os', 're', 'tempfile',
                        'traceback', 'urllib.parse', 'warnings')),
        PythonModule(min_version=(3, 8), max_version=(3, 9),
                deps=('collections.abc', 'email.message', 'email.parser',
                        'html', 'io', 'locale', 'os', 're', 'tempfile',
                        'traceback', 'urllib.parse')),
        PythonModule(min_version=(3, 10),
                deps=('collections.abc', 'email.message', 'email.parser',
                        'html', 'io', 'locale', 'os', 're', 'tempfile',
                        'traceback', 'urllib.parse', 'warnings'))),

    'cgitb': (
        PythonModule(max_version=(3, 10),
                deps=('inspect', 'keyword', 'linecache', 'os', 'pydoc',
                        'tempfile', 'time', 'tokenize', 'traceback')),
        PythonModule(min_version=(3, 11),
                deps=('html', 'inspect', 'keyword', 'linecache', 'os', 'pydoc',
                        'tempfile', 'time', 'tokenize', 'traceback',
                        'warnings'))),

    'chunk': (
        PythonModule(max_version=(3, 10), deps='struct'),
        PythonModule(min_version=(3, 11), deps=('struct', 'warnings'))),

    'cmath': (
        ExtensionModule(max_version=(3, 8),
                source=('cmathmodule.c', '_math.c'), libs='linux#-lm'),
        ExtensionModule(min_version=(3, 9), max_version=(3, 10),
                source=('cmathmodule.c', '_math.c'),
                defines='Py_BUILD_CORE_MODULE', libs='linux#-lm'),
        ExtensionModule(min_version=(3, 11),
                source='cmathmodule.c',
                defines='Py_BUILD_CORE_MODULE', libs='linux#-lm')),

    'cmd':
        PythonModule(deps='string'),

    'code':
        PythonModule(deps=('codeop', 'traceback')),

    'codecs':
        PythonModule(deps='_codecs'),

    'codeop': (
        PythonModule(max_version=(3, 7, 7), deps='__future__'),
        PythonModule(min_version=(3, 7, 8), max_version=(3, 7),
                deps=('__future__', 'warnings')),
        PythonModule(min_version=(3, 8), max_version=(3, 8, 3),
                deps='__future__'),
        PythonModule(min_version=(3, 8, 4), deps=('__future__', 'warnings'))),

    'collections':
        PythonModule(
                deps=('_collections', '_collections_abc', 'copy', 'heapq',
                        'itertools', 'keyword', 'operator', 'reprlib',
                        'warnings', '_weakref')),

    'collections.abc':
        PythonModule(deps='_collections_abc'),

    'colorsys':
        PythonModule(),

    'compileall': (
        PythonModule(max_version=(3, 8),
                deps=('concurrent.futures', 'functools', 'importlib.util',
                        'os', 'py_compile', 'struct')),
        PythonModule(min_version=(3, 9),
                deps=('concurrent.futures', 'filecmp', 'functools',
                        'importlib.util', 'os', 'pathlib', 'py_compile',
                        'struct'))),

    'concurrent':
        PythonModule(),

    'concurrent.futures':
        PythonModule(
                deps=('concurrent', 'concurrent.futures._base',
                        'concurrent.futures.process',
                        'concurrent.futures.thread')),

    'configparser':
        PythonModule(
                deps=('collections', 'collections.abc', 'functools', 'io',
                        'itertools', 'os', 're', 'warnings')),

    'contextlib': (
        PythonModule(version=(3, 7),
                deps=('abc', 'collections', '_collections_abc', 'functools')),
        PythonModule(min_version=(3, 8), max_version=(3, 10),
                deps=('abc', 'collections', '_collections_abc', 'functools',
                        'types')),
        PythonModule(min_version=(3, 11),
                deps=('abc', 'collections', '_collections_abc', 'functools',
                        'os', 'types'))),

    'contextvars':
        PythonModule(deps='_contextvars'),

    'copy':
        PythonModule(deps=('copyreg', 'types', 'weakref')),

    'copyreg': (
        PythonModule(max_version=(3, 9)),
        PythonModule(min_version=(3, 10), deps=('functools', 'operator'))),

    'cProfile':
        PythonModule(deps=('_lsprof', 'marshal', 'profile', 'pstats')),

    'crypt': (
        PythonModule(max_version=(3, 8), target='!win',
                deps=('collections', '_crypt', 'random', 'string')),
        PythonModule(min_version=(3, 9), max_version=(3, 10), target='!win',
                deps=('collections', '_crypt', 'errno', 'random', 'string')),
        PythonModule(min_version=(3, 11), target='!win',
                deps=('collections', '_crypt', 'errno', 'random', 'string',
                        'warnings'))),

    'csv': (
        PythonModule(version=(3, 7), deps=('collections', '_csv', 'io', 're')),
        PythonModule(min_version=(3, 8), deps=('_csv', 'io', 're'))),

    'ctypes': (
        PythonModule(version=(3, 7), target='linux|macos|win',
                deps=('_ctypes', 'ctypes._endian', 'os', 'struct')),
        PythonModule(version=(3, 8), target='linux|macos|win',
                deps=('_ctypes', 'ctypes._endian', 'win#nt', 'os', 'struct')),
        PythonModule(min_version=(3, 9), target='linux|macos|win',
                deps=('_ctypes', 'ctypes._endian', 'win#nt', 'os', 'struct',
                        'types'))),

    'ctypes.util':
        PythonModule(target='linux|macos|win',
                deps=('ctypes', 'ctypes.macholib.dyld', 'importlib.machinery',
                        'os', 're', 'shutil', 'struct', 'subprocess',
                        'tempfile')),

    'ctypes.wintypes':
        PythonModule(target='win', deps='ctypes'),

    'curses':
        PythonModule(target='!win', deps=('curses.has_key', '_curses', 'os')),

    'curses.ascii':
        PythonModule(target='!win', deps='curses'),

    'curses.panel':
        PythonModule(target='!win', deps=('curses', '_curses_panel')),

    'curses.textpad':
        PythonModule(target='!win', deps=('curses', 'curses.ascii')),

    'dataclasses': (
        PythonModule(max_version=(3, 7, 1),
                deps=('copy', 'inspect', 'keyword', 're', 'types')),
        PythonModule(min_version=(3, 7, 2), max_version=(3, 9),
                deps=('copy', 'functools', 'inspect', 'keyword', 're',
                        '_thread', 'types')),
        PythonModule(version=(3, 10),
                deps=('abc', 'copy', 'functools', 'inspect', 'keyword', 're',
                        '_thread', 'types')),
        PythonModule(min_version=(3, 11),
                deps=('abc', 'copy', 'functools', 'inspect', 'itertools',
                        'keyword', 're', '_thread', 'types'))),

    'datetime': (
        PythonModule(max_version=(3, 9),
                deps=('_datetime', 'math', '_strptime', 'time')),
        PythonModule(min_version=(3, 10),
                deps=('_datetime', 'math', 'operator', '_strptime', 'time'))),

    'dbm':
        PythonModule(deps=('io', 'os', 'struct')),

    'dbm.dumb': (
        PythonModule(version=(3, 7),
                deps=('dbm', 'ast', 'collections.abc', 'io', 'os',
                        'warnings')),
        PythonModule(min_version=(3, 8),
                deps=('dbm', 'ast', 'collections.abc', 'io', 'os'))),

    'dbm.gnu':
        PythonModule(target='!win', deps=('dbm', '_gdbm')),

    'dbm.ndbm':
        PythonModule(target='!win', deps=('dbm', '_dbm')),

    'decimal':
        PythonModule(deps='_pydecimal'),

    'difflib': (
        PythonModule(max_version=(3, 8), deps=('collections', 'heapq', 're')),
        PythonModule(min_version=(3, 9),
                deps=('collections', 'heapq', 're', 'types'))),

    'dis':
        PythonModule(deps=('collections', 'io', 'opcode', 'types')),

    'distutils': (
        PythonModule(max_version=(3, 9)),
        PythonModule(min_version=(3, 10), deps='warnings')),

    'distutils.archive_util':
        PythonModule(
                deps=('distutils.dir_util', 'distutils.errors',
                        'distutils.log', 'distutils.spawn',
                        '!win#grp', 'os', '!win#pwd', 'tarfile', 'warnings',
                        'zipfile')),

    'distutils.bcppcompiler':
        PythonModule(
                deps=('distutils.ccompiler', 'distutils.dep_util',
                        'distutils.errors', 'distutils.file_util',
                        'distutils.log', 'os')),

    'distutils.ccompiler':
        PythonModule(
                deps=('distutils.debug', 'distutils.dep_util',
                        'distutils.dir_util', 'distutils.errors',
                        'distutils.fancy_getopt', 'distutils.file_util',
                        'distutils.log', 'distutils.spawn',
                        'distutils.sysconfig', 'distutils.util', 'os', 're',
                        'tempfile')),

    'distutils.cmd':
        PythonModule(
                deps=('distutils.archive_util', 'distutils.debug',
                        'distutils.dep_util', 'distutils.dir_util',
                        'distutils.dist', 'distutils.errors',
                        'distutils.fancy_getopt', 'distutils.file_util',
                        'distutils.log', 'distutils.spawn', 'distutils.util',
                        'os', 're')),

    'distutils.command':
        PythonModule(),

    'distutils.command.bdist':
        PythonModule(
                deps=('distutils.core', 'distutils.errors',
                        'distutils.fancy_getopt', 'distutils.util', 'os')),

    'distutils.command.bdist_dumb':
        PythonModule(
                deps=('distutils.core', 'distutils.dir_util',
                        'distutils.errors', 'distutils.log',
                        'distutils.sysconfig', 'distutils.util', 'os')),

    'distutils.command.bdist_msi': (
        PythonModule(max_version=(3, 8), target='win',
                deps=('distutils.core', 'distutils.dir_util',
                        'distutils.errors', 'distutils.log',
                        'distutils.sysconfig', 'distutils.util',
                        'distutils.version', 'msilib', 'os')),
        PythonModule(min_version=(3, 9), max_version=(3, 10), target='win',
                deps=('distutils.core', 'distutils.dir_util',
                        'distutils.errors', 'distutils.log',
                        'distutils.sysconfig', 'distutils.util',
                        'distutils.version', 'msilib', 'os', 'warnings'))),

    'distutils.command.bdist_rpm': (
        PythonModule(max_version=(3, 8),
                deps=('distutils.core', 'distutils.debug', 'distutils.errors',
                        'distutils.file_util', 'distutils.log',
                        'distutils.sysconfig', 'distutils.util', 'os',
                        'subprocess')),
        PythonModule(min_version=(3, 9),
                deps=('distutils.core', 'distutils.debug', 'distutils.errors',
                        'distutils.file_util', 'distutils.log',
                        'distutils.sysconfig', 'os', 'subprocess'))),

    'distutils.command.bdist_wininst': (
        PythonModule(version=(3, 7), target='win',
                deps=('distutils.core', 'distutils.dir_util',
                        'distutils.errors', 'distutils.log',
                        'distutils.sysconfig', 'distutils.util', 'msvcrt',
                        'os', 'struct', 'tempfile', 'time')),
        PythonModule(min_version=(3, 8), max_version=(3, 9), target='win',
                deps=('distutils.core', 'distutils.dir_util',
                        'distutils.errors', 'distutils.log',
                        'distutils.sysconfig', 'distutils.util', 'msvcrt',
                        'os', 'struct', 'tempfile', 'time', 'warnings'))),

    'distutils.command.build':
        PythonModule(
                deps=('distutils.ccompiler', 'distutils.core',
                        'distutils.errors', 'distutils.util', 'os')),

    'distutils.command.build_clib':
        PythonModule(
                deps=('distutils.ccompiler', 'distutils.core',
                        'distutils.errors', 'distutils.log',
                        'distutils.sysconfig', 'os')),

    'distutils.command.build_ext':
        PythonModule(
                deps=('concurrent.futures', 'contextlib',
                        'distutils.ccompiler', 'distutils.core',
                        'distutils.dep_util', 'distutils.errors',
                        'distutils.extension', 'distutils.log',
                        'win#distutils._msvccompiler', 'distutils.sysconfig',
                        'distutils.util', 'os', 're')),

    'distutils.command.build_py':
        PythonModule(
                deps=('distutils.core', 'distutils.errors', 'distutils.log',
                        'distutils.util', 'glob', 'importlib.util', 'os')),

    'distutils.command.build_scripts':
        PythonModule(
                deps=('distutils.core', 'distutils.dep_util', 'distutils.log',
                        'distutils.sysconfig', 'distutils.util', 'os', 're',
                        'stat', 'tokenize')),

    'distutils.command.check':
        PythonModule(deps=('distutils.core', 'distutils.errors')),

    'distutils.command.clean':
        PythonModule(
                deps=('distutils.core', 'distutils.dir_util', 'distutils.log',
                        'os')),

    'distutils.command.config':
        PythonModule(
                deps=('distutils.ccompiler', 'distutils.core',
                        'distutils.errors', 'distutils.log',
                        'distutils.sysconfig', 'os', 're')),

    'distutils.command.install': (
        PythonModule(max_version=(3, 9),
                deps=('distutils.core', 'distutils.debug', 'distutils.errors',
                        'distutils.fancy_getopt', 'distutils.file_util',
                        'distutils.log', 'distutils.sysconfig',
                        'distutils.util', 'os', 'pprint')),
        PythonModule(min_version=(3, 10),
                deps=('distutils.core', 'distutils.debug', 'distutils.errors',
                        'distutils.fancy_getopt', 'distutils.file_util',
                        'distutils.log', 'distutils.sysconfig',
                        'distutils.util', 'os', 'pprint', 're', 'sysconfig'))),

    'distutils.command.install_data':
        PythonModule(deps=('distutils.core', 'distutils.util', 'os')),

    'distutils.command.install_egg_info':
        PythonModule(
                deps=('distutils.cmd', 'distutils.dir_util', 'distutils.log',
                        'os', 're')),

    'distutils.command.install_headers':
        PythonModule(deps='distutils.core'),

    'distutils.command.install_lib':
        PythonModule(
                deps=('distutils.core', 'distutils.errors', 'distutils.util',
                        'importlib.util', 'os')),

    'distutils.command.install_scripts':
        PythonModule(deps=('distutils.core', 'distutils.log', 'os', 'stat')),

    'distutils.command.register':
        PythonModule(
                deps=('distutils.core', 'distutils.errors', 'distutils.log',
                        'getpass', 'io', 'urllib.parse', 'urllib.request',
                        'warnings')),

    'distutils.command.sdist':
        PythonModule(
                deps=('distutils.archive_util', 'distutils.core',
                        'distutils.dir_util',
                        'distutils.errors', 'distutils.fancy_getopt',
                        'distutils.file_util', 'distutils.filelist',
                        'distutils.log', 'distutils.text_file',
                        'distutils.util', 'glob', 'os', 'warnings')),

    'distutils.command.upload': (
        PythonModule(max_version=(3, 8),
                deps=('base64', 'distutils.core', 'distutils.errors',
                        'distutils.log', 'distutils.spawn', 'hashlib', 'io',
                        'os', 'platform', 'urllib.parse', 'urllib.request')),
        PythonModule(min_version=(3, 9),
                deps=('base64', 'distutils.core', 'distutils.errors',
                        'distutils.log', 'distutils.spawn', 'hashlib', 'io',
                        'os', 'urllib.parse', 'urllib.request'))),

    'distutils.core':
        PythonModule(
                deps=('distutils.cmd', 'distutils.config', 'distutils.debug',
                        'distutils.dist', 'distutils.errors',
                        'distutils.extension', 'os')),

    'distutils.cygwinccompiler': (
        PythonModule(max_version=(3, 8),
                deps=('copy', 'distutils.ccompiler', 'distutils.errors',
                        'distutils.file_util', 'distutils.log',
                        'distutils.spawn', 'distutils.sysconfig',
                        'distutils.unixccompiler', 'distutils.version', 'os',
                        're', 'subprocess')),
        PythonModule(min_version=(3, 9),
                deps=('copy', 'distutils.errors', 'distutils.file_util',
                        'distutils.spawn', 'distutils.sysconfig',
                        'distutils.unixccompiler', 'distutils.version', 'os',
                        're', 'subprocess'))),

    'distutils.debug':
        PythonModule(deps='os'),

    'distutils.dep_util':
        PythonModule(deps=('distutils.errors', 'os', 'stat')),

    'distutils.dir_util':
        PythonModule(deps=('distutils.errors', 'distutils.file_util',
                'distutils.log', 'errno', 'os')),

    'distutils.dist':
        PythonModule(
                deps=('configparser', 'distutils.cmd', 'distutils.command',
                        'distutils.core', 'distutils.debug',
                        'distutils.errors', 'distutils.fancy_getopt',
                        'distutils.log', 'distutils.util',
                        'distutils.versionpredicate', 'email', 'os', 'pprint',
                        're', 'warnings')),

    'distutils.errors':
        PythonModule(),

    'distutils.extension': (
        PythonModule(max_version=(3, 9),
                deps=('distutils.sysconfig', 'distutils.text_file',
                        'distutils.util', 'os', 'warnings')),
        PythonModule(min_version=(3, 10),
                deps=('distutils.sysconfig', 'distutils.text_file',
                        'distutils.util', 'os', 're', 'warnings'))),

    'distutils.fancy_getopt':
        PythonModule(
                deps=('distutils.errors', 'getopt', 're', 'string')),

    'distutils.file_util':
        PythonModule(
                deps=('distutils.dep_util', 'distutils.errors',
                        'distutils.log', 'errno', 'os', 'stat')),

    'distutils.filelist':
        PythonModule(
                deps=('distutils.debug', 'distutils.errors', 'distutils.log',
                        'distutils.util', 'fnmatch', 'functools', 'os',
                        're')),

    'distutils.log':
        PythonModule(),

    'distutils.msvccompiler':
        PythonModule(target='win',
                deps=('distutils.ccompiler', 'distutils.errors',
                        'distutils.log', 'distutils.msvc9compiler', 'os',
                        'winreg')),

    'distutils.spawn': (
        PythonModule(max_version=(3, 8),
                deps=('distutils.debug', 'distutils.errors', 'distutils.log',
                        'distutils.sysconfig', 'os')),
        PythonModule(min_version=(3, 9),
                deps=('distutils.debug', 'distutils.errors', 'distutils.log',
                        'distutils.sysconfig', 'os', 'spawn'))),

    'distutils.sysconfig': (
        PythonModule(version=(3, 7),
                deps=('distutils.errors', 'distutils.text_file', '_imp', 'os',
                        'ios|macos#_osx_support', 're', 'warnings')),
        PythonModule(version=(3, 8),
                deps=('distutils.errors', 'distutils.util',
                        'distutils.text_file', '_imp', 'os',
                        'ios|macos#_osx_support', 're', 'warnings')),
        PythonModule(version=(3, 9),
                deps=('distutils.errors', 'distutils.text_file', '_imp', 'os',
                        'ios|macos#_osx_support', 're', 'warnings')),
        PythonModule(min_version=(3, 10),
                deps=('distutils.errors', 'distutils.text_file', 'functools',
                        '_imp', 'os', 'ios|macos#_osx_support', 're',
                        'sysconfig', 'warnings'))),

    'distutils.text_file':
        PythonModule(deps='io'),

    'distutils.unixccompiler':
        PythonModule(
                deps=('distutils.ccompiler', 'distutils.dep_util',
                        'distutils.errors', 'distutils.log',
                        'distutils.sysconfig', 'os', 'ios|macos#_osx_support',
                        're')),

    'distutils.util': (
        PythonModule(version=(3, 9),
                deps=('distutils.dep_util', 'distutils.errors',
                        'distutils.log', 'distutils.spawn',
                        'distutils.sysconfig', 'importlib.util', 'os',
                        'ios|macos#_osx_support', '!win#pwd', 'py_compile',
                        're', 'string', 'subprocess', 'tempfile')),
        PythonModule(min_version=(3, 10),
                deps=('distutils', 'distutils.dep_util', 'distutils.errors',
                        'distutils.log', 'distutils.spawn',
                        'distutils.sysconfig', 'importlib.util', 'os',
                        'ios|macos#_osx_support', '!win#pwd', 'py_compile',
                        're', 'string', 'subprocess', 'tempfile'))),

    'distutils.version':
        PythonModule(deps='re'),

    'email':
        PythonModule(deps='email.parser'),

    'email.charset':
        PythonModule(
                deps=('email', 'email.base64mime', 'email.encoders',
                        'email.errors', 'email.quoprimime', 'functools')),

    'email.contentmanager':
        PythonModule(
                deps=('email', 'binascii', 'email.charset', 'email.errors',
                        'email.message', 'email.quoprimime')),

    'email.encoders':
        PythonModule(deps=('email', 'base64', 'quopri')),

    'email.errors':
        PythonModule(deps='email'),

    'email.generator':
        PythonModule(
                deps=('email', 'copy', 'email.utils', 'io', 'random', 're',
                        'time')),

    'email.header':
        PythonModule(
                deps=('email', 'binascii', 'email.base64mime', 'email.charset',
                        'email.errors', 'email.quoprimime', 're')),

    'email.headerregistry':
        PythonModule(
                deps=('email', 'email.errors', 'email._header_value_parser',
                        'email.utils', 'types')),

    'email.iterators':
        PythonModule(deps=('email', 'io')),

    'email.message': (
        PythonModule(max_version=(3, 10),
                deps=('email', 'email.charset', 'email._encoded_words',
                        'email.errors', 'email.generator', 'email.iterators',
                        'email.policy', 'email._policybase', 'email.utils',
                        'io', 'quopri', 're', 'uu')),
        PythonModule(min_version=(3, 11),
                deps=('email', 'email.charset', 'email._encoded_words',
                        'email.errors', 'email.generator', 'email.iterators',
                        'email.policy', 'email._policybase', 'email.utils',
                        'binascii', 'io', 'quopri', 're'))),

    'email.mime':
        PythonModule(deps='email'),

    'email.mime.application':
        PythonModule(
                deps=('email.mime', 'email.encoders',
                        'email.mime.nonmultipart')),

    'email.mime.audio': (
        PythonModule(max_version=(3, 10),
                deps=('email.mime', 'email.encoders',
                        'email.mime.nonmultipart', 'io', 'sndhdr')),
        PythonModule(min_version=(3, 11),
                deps=('email.mime', 'email.encoders',
                        'email.mime.nonmultipart', 'io'))),

    'email.mime.base':
        PythonModule(deps=('email.mime', 'email.message', 'email.policy')),

    'email.mime.image': (
        PythonModule(max_version=(3, 10),
                deps=('email.mime', 'email.encoders',
                        'email.mime.nonmultipart', 'imghdr')),
        PythonModule(min_version=(3, 11),
                deps=('email.mime', 'email.encoders',
                        'email.mime.nonmultipart'))),

    'email.mime.message':
        PythonModule(
                deps=('email.mime', 'email.message',
                        'email.mime.nonmultipart')),

    'email.mime.multipart':
        PythonModule(deps=('email.mime', 'email.mime.base')),

    'email.mime.nonmultipart':
        PythonModule(deps=('email.mime', 'email.errors', 'email.mime.base')),

    'email.mime.text':
        PythonModule(
                deps=('email.mime', 'email.charset',
                        'email.mime.nonmultipart')),

    'email.parser':
        PythonModule(
                deps=('email', 'email.feedparser', 'email._policybase', 'io')),

    'email.policy':
        PythonModule(
                deps=('email', 'email.contentmanager', 'email.headerregistry',
                        'email.message', 'email._policybase', 'email.utils',
                        're')),

    'email.utils':
        PythonModule(
                deps=('email', 'datetime', 'email.charset', 'email._parseaddr',
                        'os', 'random', 're', 'socket', 'time',
                        'urllib.parse')),

    'encodings':
        PythonModule(
                deps=('encodings.aliases', 'codecs', 'win#_winapi')),

    'encodings.ascii':
        CodecModule(core=True),

    'encodings.base64_codec':
        CodecModule(deps='base64'),

    'encodings.big5':
        CodecModule(deps=('_codecs_tw', '_multibytecodec')),

    'encodings.big5hkscs':
        CodecModule(deps=('_codecs_hk', '_multibytecodec')),

    'encodings.bz2_codec':
        CodecModule(deps='bz2'),

    'encodings.charmap':
        CodecModule(),

    'encodings.cp037':
        CodecModule(),

    'encodings.cp1006':
        CodecModule(),

    'encodings.cp1026':
        CodecModule(),

    'encodings.cp1125':
        CodecModule(),

    'encodings.cp1140':
        CodecModule(),

    'encodings.cp1250':
        CodecModule(),

    'encodings.cp1251':
        CodecModule(),

    'encodings.cp1252':
        CodecModule(),

    'encodings.cp1253':
        CodecModule(),

    'encodings.cp1254':
        CodecModule(),

    'encodings.cp1255':
        CodecModule(),

    'encodings.cp1256':
        CodecModule(),

    'encodings.cp1257':
        CodecModule(),

    'encodings.cp1258':
        CodecModule(),

    'encodings.cp273':
        CodecModule(),

    'encodings.cp424':
        CodecModule(),

    'encodings.cp437':
        CodecModule(core=True),

    'encodings.cp500':
        CodecModule(),

    'encodings.cp65001':
        CodecModule(version=(3, 7)),

    'encodings.cp720':
        CodecModule(),

    'encodings.cp737':
        CodecModule(),

    'encodings.cp775':
        CodecModule(),

    'encodings.cp850':
        CodecModule(),

    'encodings.cp852':
        CodecModule(),

    'encodings.cp855':
        CodecModule(),

    'encodings.cp856':
        CodecModule(),

    'encodings.cp857':
        CodecModule(),

    'encodings.cp858':
        CodecModule(),

    'encodings.cp860':
        CodecModule(),

    'encodings.cp861':
        CodecModule(),

    'encodings.cp862':
        CodecModule(),

    'encodings.cp863':
        CodecModule(),

    'encodings.cp864':
        CodecModule(),

    'encodings.cp865':
        CodecModule(),

    'encodings.cp866':
        CodecModule(),

    'encodings.cp869':
        CodecModule(),

    'encodings.cp874':
        CodecModule(),

    'encodings.cp875':
        CodecModule(),

    'encodings.cp932':
        CodecModule(deps=('_codecs_jp', '_multibytecodec')),

    'encodings.cp949':
        CodecModule(deps=('_codecs_kr', '_multibytecodec')),

    'encodings.cp950':
        CodecModule(deps=('_codecs_tw', '_multibytecodec')),

    'encodings.euc_jis_2004':
        CodecModule(deps=('_codecs_jp', '_multibytecodec')),

    'encodings.euc_jisx0213':
        CodecModule(deps=('_codecs_jp', '_multibytecodec')),

    'encodings.euc_jp':
        CodecModule(deps=('_codecs_jp', '_multibytecodec')),

    'encodings.euc_kr':
        CodecModule(deps=('_codecs_kr', '_multibytecodec')),

    'encodings.gb18030':
        CodecModule(deps=('_codecs_cn', '_multibytecodec')),

    'encodings.gb2312':
        CodecModule(deps=('_codecs_cn', '_multibytecodec')),

    'encodings.gbk':
        CodecModule(deps=('_codecs_cn', '_multibytecodec')),

    'encodings.hex_codec':
        CodecModule(deps='binascii'),

    'encodings.hp_roman8':
        CodecModule(),

    'encodings.hz':
        CodecModule(deps=('_codecs_cn', '_multibytecodec')),

    'encodings.idna':
        PythonModule(
                deps=('encodings', 'codecs', 're', 'stringprep',
                        'unicodedata')),

    'encodings.iso2022_jp':
        CodecModule(deps=('_codecs_iso2022', '_multibytecodec')),

    'encodings.iso2022_jp_1':
        CodecModule(deps=('_codecs_iso2022', '_multibytecodec')),

    'encodings.iso2022_jp_2':
        CodecModule(deps=('_codecs_iso2022', '_multibytecodec')),

    'encodings.iso2022_jp_2004':
        CodecModule(deps=('_codecs_iso2022', '_multibytecodec')),

    'encodings.iso2022_jp_3':
        CodecModule(deps=('_codecs_iso2022', '_multibytecodec')),

    'encodings.iso2022_jp_ext':
        CodecModule(deps=('_codecs_iso2022', '_multibytecodec')),

    'encodings.iso2022_kr':
        CodecModule(deps=('_codecs_iso2022', '_multibytecodec')),

    'encodings.iso8859_1':
        CodecModule(),

    'encodings.iso8859_10':
        CodecModule(),

    'encodings.iso8859_11':
        CodecModule(),

    'encodings.iso8859_13':
        CodecModule(),

    'encodings.iso8859_14':
        CodecModule(),

    'encodings.iso8859_15':
        CodecModule(),

    'encodings.iso8859_16':
        CodecModule(),

    'encodings.iso8859_2':
        CodecModule(),

    'encodings.iso8859_3':
        CodecModule(),

    'encodings.iso8859_4':
        CodecModule(),

    'encodings.iso8859_5':
        CodecModule(),

    'encodings.iso8859_6':
        CodecModule(),

    'encodings.iso8859_7':
        CodecModule(),

    'encodings.iso8859_8':
        CodecModule(),

    'encodings.iso8859_9':
        CodecModule(),

    'encodings.johab':
        CodecModule(deps=('_codecs_kr', '_multibytecodec')),

    'encodings.koi8_r':
        CodecModule(),

    'encodings.koi8_t':
        CodecModule(),

    'encodings.koi8_u':
        CodecModule(),

    'encodings.kz1048':
        CodecModule(),

    'encodings.latin_1':
        CodecModule(core=True),

    'encodings.mac_arabic':
        CodecModule(),

    'encodings.mac_centeuro':
        CodecModule(max_version=(3, 8)),

    'encodings.mac_croatian':
        CodecModule(),

    'encodings.mac_cyrillic':
        CodecModule(),

    'encodings.mac_farsi':
        CodecModule(),

    'encodings.mac_greek':
        CodecModule(),

    'encodings.mac_iceland':
        CodecModule(),

    'encodings.mac_latin2':
        CodecModule(),

    'encodings.mac_roman':
        CodecModule(),

    'encodings.mac_romanian':
        CodecModule(),

    'encodings.mac_turkish':
        CodecModule(),

    'encodings.mbcs':
        CodecModule(target='win', core=True),

    'encodings.oem':
        CodecModule(target='win', deps=('codecs')),

    'encodings.palmos':
        CodecModule(),

    'encodings.ptcp154':
        CodecModule(),

    'encodings.punycode':
        CodecModule(),

    'encodings.quopri_codec':
        CodecModule(deps=('io', 'quopri')),

    'encodings.raw_unicode_escape':
        CodecModule(),

    'encodings.rot_13':
        CodecModule(),

    'encodings.shift_jis':
        CodecModule(deps=('_codecs_jp', '_multibytecodec')),

    'encodings.shift_jis_2004':
        CodecModule(deps=('_codecs_jp', '_multibytecodec')),

    'encodings.shift_jisx0213':
        CodecModule(deps=('_codecs_jp', '_multibytecodec')),

    'encodings.tis_620':
        CodecModule(),

    'encodings.undefined':
        CodecModule(),

    'encodings.unicode_escape':
        CodecModule(),

    'encodings.unicode_internal':
        CodecModule(version=(3, 7)),

    'encodings.utf_16':
        CodecModule(),

    'encodings.utf_16_be':
        CodecModule(),

    'encodings.utf_16_le':
        CodecModule(),

    'encodings.utf_32':
        CodecModule(),

    'encodings.utf_32_be':
        CodecModule(),

    'encodings.utf_32_le':
        CodecModule(),

    'encodings.utf_7':
        CodecModule(),

    'encodings.utf_8':
        CodecModule(core=True),

    'encodings.utf_8_sig':
        CodecModule(),

    'encodings.uu_codec':
        CodecModule(deps=('binascii', 'io')),

    'encodings.zlib_codec':
        CodecModule(deps='zlib'),

    'enum': (
        PythonModule(version=(3, 7), deps=('_collections', 'types')),
        PythonModule(min_version=(3, 8), max_version=(3, 10), deps='types'),
        PythonModule(min_version=(3, 11),
                deps=('functools', 'operator', 'types'))),

    'errno':
        CoreExtensionModule(),

    'faulthandler':
        CoreExtensionModule(),

    'fcntl':
        ExtensionModule(target='!win', source='fcntlmodule.c'),

    'filecmp': (
        PythonModule(max_version=(3, 8), deps=('itertools', 'os', 'stat')),
        PythonModule(min_version=(3, 9),
                deps=('itertools', 'os', 'stat', 'types'))),

    'fileinput': (
        PythonModule(max_version=(3, 8), deps=('os', 'warnings')),
        PythonModule(version=(3, 9), deps=('os', 'types', 'warnings')),
        PythonModule(min_version=(3, 10),
                deps=('io', 'os', 'types', 'warnings'))),

    'fnmatch': (
        PythonModule(max_version=(3, 8),
                deps=('functools', 'os', 'posixpath', 're')),
        PythonModule(min_version=(3, 9), max_version=(3, 10),
                deps=('functools', 'itertools', 'os', 'posixpath', 're')),
        PythonModule(min_version=(3, 11),
                deps=('functools', 'os', 'posixpath', 're'))),

    'formatter':
        PythonModule(max_version=(3, 9), deps='warnings'),

    'fractions': (
        PythonModule(max_version=(3, 8),
                deps=('decimal', 'math', 'numbers', 'operator', 're',
                        'warnings')),
        PythonModule(min_version=(3, 9),
                deps=('decimal', 'math', 'numbers', 'operator', 're'))),

    'ftplib':
        PythonModule(deps=('re', 'socket', '?ssl', 'warnings')),

    'functools': (
        PythonModule(max_version=(3, 10),
                deps=('abc', 'collections', '_functools', 'reprlib', '_thread',
                        'types', 'weakref')),
        PythonModule(min_version=(3, 11),
                deps=('abc', 'collections', '_functools', 'reprlib', '_thread',
                        'types', 'typing', 'weakref'))),

    'gc':
        CoreExtensionModule(),

    'getopt':
        PythonModule(deps=('gettext', 'os')),

    'getpass':
        PythonModule(
                deps=('contextlib', 'io', 'win#msvcrt', 'os', '!win#pwd',
                        '!win#termios', 'warnings')),

    'gettext':
        PythonModule(
                deps=('copy', 'errno', 'locale', 'os', 're', 'struct',
                        'warnings')),

    'glob': (
        PythonModule(max_version=(3, 9, 5), deps=('fnmatch', 'os', 're')),
        PythonModule(min_version=(3, 9, 6), max_version=(3, 9),
                deps=('contextlib', 'fnmatch', 'os', 're')),
        PythonModule(min_version=(3, 10),
                deps=('contextlib', 'fnmatch', 'itertools', 'os', 're',
                        'stat'))),

    'graphlib': (
        PythonModule(max_version=(3, 10)),
        PythonModule(min_version=(3, 11), deps='types')),

    'grp':
        ExtensionModule(target='!win', min_android_api=26,
                source='grpmodule.c'),

    'gzip':
        PythonModule(
                deps=('_compression', 'errno', 'io', 'os', 'struct', 'time',
                        'warnings', 'zlib')),

    'hashlib':
        PythonModule(
                deps=('?_hashlib', '!_md5', '!_sha1', '!_sha256', '!_sha512',
                        '_blake2', '_sha3')),

    'heapq':
        PythonModule(deps='_heapq'),

    'hmac':
        PythonModule(deps=('hashlib', '?_hashlib', '_operator', 'warnings')),

    'html':
        PythonModule(deps=('html.entities', 're')),

    'html.entities':
        PythonModule(deps='html'),

    'html.parser':
        PythonModule(deps=('html', '_markupbase', 're', 'warnings')),

    'http':
        PythonModule(deps='enum'),

    'http.client': (
        PythonModule(max_version=(3, 9, 7),
                deps=('http', 'collections.abc', 'email.message',
                        'email.parser', 'io', 're', 'socket', '?ssl',
                        'urllib.parse', 'warnings')),
        PythonModule(min_version=(3, 9, 8), max_version=(3, 9),
                deps=('http', 'collections.abc', 'email.message',
                        'email.parser', 'errno', 'io', 're', 'socket', '?ssl',
                        'urllib.parse', 'warnings')),
        PythonModule(version=(3, 10, 0),
                deps=('http', 'collections.abc', 'email.message',
                        'email.parser', 'io', 're', 'socket', '?ssl',
                        'urllib.parse', 'warnings')),
        PythonModule(min_version=(3, 10, 1),
                deps=('http', 'collections.abc', 'email.message',
                        'email.parser', 'errno', 'io', 're', 'socket', '?ssl',
                        'urllib.parse', 'warnings'))),

    'http.cookiejar': (
        PythonModule(version=(3, 7),
                deps=('http', 'calendar', 'copy', 'datetime', 'http.client',
                        're', 'threading', 'time', 'urllib.parse',
                        'urllib.request')),
        PythonModule(min_version=(3, 8),
                deps=('http', 'calendar', 'copy', 'datetime', 'http.client',
                        'os', 're', 'threading', 'time', 'urllib.parse',
                        'urllib.request'))),

    'http.cookies': (
        PythonModule(max_version=(3, 8),
                deps=('http', 're', 'string', 'time')),
        PythonModule(min_version=(3, 9),
                deps=('http', 're', 'string', 'time', 'types'))),

    'http.server': (
        PythonModule(max_version=(3, 8, 1),
                deps=('http', 'base64', 'binascii', 'copy', 'datetime',
                        'email.utils', 'functools', 'html', 'http.client',
                        'io', 'mimetypes', 'os', 'posixpath', '!win#pwd',
                        'select', 'shutil', 'socket', 'socketserver',
                        'subprocess', 'time', 'urllib.parse')),
        PythonModule(min_version=(3, 8, 2), max_version=(3, 9, 10),
                deps=('http', 'base64', 'binascii', 'contextlib', 'copy',
                        'datetime', 'email.utils', 'functools', 'html',
                        'http.client', 'io', 'mimetypes', 'os', 'posixpath',
                        '!win#pwd', 'select', 'shutil', 'socket',
                        'socketserver', 'subprocess', 'time',
                        'urllib.parse')),
        PythonModule(min_version=(3, 9, 10), max_version=(3, 9),
                deps=('http', 'base64', 'binascii', 'copy', 'datetime',
                        'email.utils', 'html', 'http.client', 'io',
                        'mimetypes', 'os', 'posixpath', '!win#pwd', 'select',
                        'shutil', 'socket', 'socketserver', 'subprocess',
                        'time', 'urllib.parse')),
        PythonModule(min_version=(3, 10), max_version=(3, 10, 2),
                deps=('http', 'base64', 'binascii', 'contextlib', 'copy',
                        'datetime', 'email.utils', 'functools', 'html',
                        'http.client', 'io', 'mimetypes', 'os', 'posixpath',
                        '!win#pwd', 'select', 'shutil', 'socket',
                        'socketserver', 'subprocess', 'time',
                        'urllib.parse')),
        PythonModule(min_version=(3, 10, 3),
                deps=('http', 'base64', 'binascii', 'copy', 'datetime',
                        'email.utils', 'html', 'http.client', 'io',
                        'mimetypes', 'os', 'posixpath', '!win#pwd', 'select',
                        'shutil', 'socket', 'socketserver', 'subprocess',
                        'time', 'urllib.parse'))),

    'imaplib':
        PythonModule(
                deps=('binascii', 'calendar', 'datetime', 'errno', 'hmac',
                        'io', 'random', 're', 'socket', '?ssl', 'subprocess',
                        'time', 'warnings')),

    'imghdr': (
        PythonModule(max_version=(3, 10), deps='os'),
        PythonModule(min_version=(3, 11), deps=('os', 'warnings'))),

    'imp':
        CorePythonModule(
                deps=('_imp', 'importlib', 'importlib._bootstrap',
                        'importlib._bootstrap_external', 'importlib.machinery',
                        'importlib.util', 'os', 'tokenize', 'types',
                        'warnings')),

    'importlib': (
        CorePythonModule(max_version=(3, 9),
                deps=('importlib._bootstrap', 'importlib._bootstrap_external',
                        '_imp', 'types'),
                hidden_deps='warnings'),
        CorePythonModule(min_version=(3, 10),
                deps=('importlib._bootstrap', 'importlib._bootstrap_external',
                        '_imp'),
                hidden_deps='warnings')),

    'importlib.abc': (
        PythonModule(max_version=(3, 8),
                deps=('importlib', 'abc', 'importlib._bootstrap',
                        'importlib._bootstrap_external', 'importlib.machinery',
                        'warnings')),
        PythonModule(version=(3, 9),
                deps=('importlib', 'abc', 'importlib._bootstrap',
                        'importlib._bootstrap_external', 'importlib.machinery',
                        'typing', 'warnings')),
        PythonModule(version=(3, 10),
                deps=('importlib', 'abc', 'importlib._abc',
                        'importlib._bootstrap_external', 'importlib.machinery',
                        'typing', 'warnings')),
        PythonModule(min_version=(3, 11),
                deps=('importlib', 'abc', 'importlib._abc',
                        'importlib._bootstrap_external', 'importlib.machinery',
                        'importlib.resources.abc', 'warnings'))),

    'importlib.machinery': (
        PythonModule(max_version=(3, 9),
                deps=('importlib', '_imp', 'importlib._bootstrap',
                        'importlib._bootstrap_external')),
        PythonModule(min_version=(3, 10),
                deps=('importlib', 'importlib._bootstrap',
                        'importlib._bootstrap_external'))),

    'importlib.metadata': (
        PythonModule(min_version=(3, 8), max_version=(3, 8, 1),
                deps=('importlib', 'abc', 'collections', 'configparser',
                        'contextlib', 'csv', 'email', 'functools',
                        'importlib.abc', 'io', 'itertools', 'operator', 'os',
                        'pathlib', 're', 'zipfile')),
        PythonModule(min_version=(3, 8, 2), max_version=(3, 9),
                deps=('importlib', 'abc', 'collections', 'configparser',
                        'contextlib', 'csv', 'email', 'functools',
                        'importlib.abc', 'io', 'itertools', 'operator', 'os',
                        'pathlib', 'posixpath', 're', 'zipfile')),
        PythonModule(min_version=(3, 10),
                deps=('importlib', 'abc', 'collections', 'contextlib', 'csv',
                        'email', 'functools', 'importlib.abc',
                        'importlib.metadata._adapters',
                        'importlib.metadata._collections',
                        'importlib.metadata._itertools',
                        'importlib.metadata._functools',
                        'importlib.metadata._meta', 'itertools', 'operator',
                        'os', 'pathlib', 'posixpath', 're', 'textwrap',
                        'typing', 'warnings', 'zipfile'))),

    'importlib.resources': (
        PythonModule(max_version=(3, 8),
                deps=('importlib', 'contextlib', 'importlib.abc', 'io',
                        'pathlib', 'os', 'tempfile', 'types', 'typing',
                        'zipimport')),
        PythonModule(version=(3, 9),
                deps=('importlib', 'contextlib', 'importlib.abc',
                        'importlib._common', 'io', 'pathlib', 'os', 'tempfile',
                        'types', 'typing')),
        PythonModule(version=(3, 10),
                deps=('collections', 'contextlib', 'functools',
                        'importlib.abc', 'importlib._common',
                        'importlib.machinery', 'io', 'pathlib', 'os',
                        'tempfile', 'types', 'typing')),
        PythonModule(min_version=(3, 11),
                deps=('importlib.resources._common',
                        'importlib.resources._legacy',
                        'importlib.resources.abc'))),

    'importlib.resources.abc':
        PythonModule(min_version=(3, 11),
                deps=('abc', 'io', 'os', 'typing')),

    'importlib.util': (
        PythonModule(max_version=(3, 9),
                deps=('importlib', 'contextlib', 'functools', '_imp',
                        'importlib.abc', 'importlib._bootstrap',
                        'importlib._bootstrap_external', 'types', 'warnings')),
        PythonModule(min_version=(3, 10),
                deps=('importlib', 'contextlib', 'functools', '_imp',
                        'importlib._abc', 'importlib._bootstrap',
                        'importlib._bootstrap_external', 'types',
                        'warnings'))),

    'inspect': (
        PythonModule(max_version=(3, 10),
                deps=('abc', 'ast', 'collections', 'collections.abc', 'dis',
                        'enum', 'functools', 'importlib.machinery',
                        'itertools', 'linecache', 'operator', 'os', 're',
                        'token', 'tokenize', 'types', 'warnings')),
        PythonModule(min_version=(3, 11),
                deps=('abc', 'ast', 'collections', 'collections.abc', 'dis',
                        'enum', 'functools', 'importlib.machinery',
                        'itertools', 'keyword', 'linecache', 'operator', 'os',
                        're', 'token', 'tokenize', 'types'))),

    'io':
        CorePythonModule(deps=('abc', '_io')),

    'ipaddress':
        PythonModule(deps='functools'),

    'itertools':
        CoreExtensionModule(),

    'json':
        PythonModule(deps=('codecs', 'json.decoder', 'json.encoder')),

    'keyword':
        PythonModule(),

    'linecache':
        PythonModule(deps=('functools', 'os', 'tokenize')),

    'locale': (
        PythonModule(max_version=(3, 9),
                deps=('_bootlocale', '_collections_abc', 'encodings',
                        'encodings.aliases', 'functools', '_locale', 'os',
                        're')),
        PythonModule(version=(3, 10),
                deps=('_collections_abc', 'encodings', 'encodings.aliases',
                        'functools', '_locale', 'os', 're')),
        PythonModule(min_version=(3, 11),
                deps=('_collections_abc', 'encodings', 'encodings.aliases',
                        'functools', '_locale', 'os', 're', 'warnings'))),

    'logging': (
        PythonModule(version=(3, 7),
                deps=('atexit', 'collections.abc', 'io', 'os', 'pickle',
                        'string', 'threading', 'time', 'traceback', 'warnings',
                        'weakref')),
        PythonModule(min_version=(3, 8), max_version=(3, 10),
                deps=('atexit', 'collections.abc', 'io', 'os', 'pickle', 're',
                        'string', 'threading', 'time', 'traceback', 'warnings',
                        'weakref')),
        PythonModule(min_version=(3, 11),
                deps=('atexit', 'collections.abc', 'io', 'os', 'pickle', 're',
                        'string', 'threading', 'time', 'traceback', 'types',
                        'warnings', 'weakref'))),

    'logging.config':
        PythonModule(
                deps=('logging', 'errno', 'configparser', 'io', 'json',
                        'logging.handlers', 're', 'select', 'socketserver',
                        'struct', 'threading', 'traceback')),

    'logging.handlers': (
        PythonModule(max_version=(3, 7, 3),
                deps=('logging', 'base64', 'codecs', 'email.message',
                        'email.utils', 'errno', 'http.client', 'os', 'pickle',
                        'queue', 're', 'socket', 'smtplib', 'stat', 'struct',
                        'threading', 'time', 'urllib.parse')),
        PythonModule(min_version=(3, 7, 4), max_version=(3, 9),
                deps=('logging', 'base64', 'codecs', 'copy', 'email.message',
                        'email.utils', 'errno', 'http.client', 'os', 'pickle',
                        'queue', 're', 'socket', 'smtplib', 'stat', 'struct',
                        'threading', 'time', 'urllib.parse')),
        PythonModule(min_version=(3, 10),
                deps=('logging', 'base64', 'codecs', 'copy', 'email.message',
                        'email.utils', 'errno', 'http.client', 'io', 'os',
                        'pickle', 'queue', 're', 'socket', 'smtplib', 'stat',
                        'struct', 'threading', 'time', 'urllib.parse'))),

    'lzma':
        PythonModule(deps=('_compression', 'io', '_lzma', 'os')),

    'macpath':
        PythonModule(version=(3, 7),
                deps=('genericpath', 'os', 'stat', 'warnings')),

    'mailbox': (
        PythonModule(max_version=(3, 8),
                deps=('calendar', 'contextlib', 'copy', 'email',
                        'email.generator', 'email.message', 'errno',
                        '!win#fcntl', 'io', 'os', 'socket', 'time',
                        'warnings')),
        PythonModule(min_version=(3, 9),
                deps=('calendar', 'contextlib', 'copy', 'email',
                        'email.generator', 'email.message', 'errno',
                        '!win#fcntl', 'io', 'os', 'socket', 'time', 'types',
                        'warnings'))),

    'mailcap': (
        PythonModule(max_version=(3, 10, 7), deps=('os', 'warnings')),
        PythonModule(min_version=(3, 10, 8), deps=('os', 're', 'warnings'))),

    'marshal':
        CoreExtensionModule(),

    'math': (
        ExtensionModule(max_version=(3, 8), source=('mathmodule.c', '_math.c'),
                libs='linux#-lm'),
        ExtensionModule(min_version=(3, 9), max_version=(3, 10),
                source=('mathmodule.c', '_math.c'),
                defines='Py_BUILD_CORE_MODULE', libs='linux#-lm'),
        ExtensionModule(min_version=(3, 11), source='mathmodule.c',
                defines='Py_BUILD_CORE_MODULE', libs='linux#-lm')),

    'mimetypes': (
        PythonModule(max_version=(3, 9),
                deps=('os', 'posixpath', 'urllib.parse', 'win#winreg')),
        PythonModule(min_version=(3, 10),
                deps=('os', 'posixpath', 'urllib.parse', 'win#_winapi',
                        'win#winreg'))),

    'mmap':
        ExtensionModule(source='mmapmodule.c'),

    'modulefinder': (
        PythonModule(max_version=(3, 8, 2),
                deps=('dis', 'importlib._bootstrap_external',
                        'importlib.machinery', 'marshal', 'os', 'types',
                        'warnings')),
        PythonModule(min_version=(3, 8, 3), max_version=(3, 8),
                deps=('dis', 'importlib._bootstrap_external',
                        'importlib.machinery', 'io', 'marshal', 'os', 'types',
                        'warnings')),
        PythonModule(min_version=(3, 9),
                deps=('dis', 'importlib._bootstrap_external',
                        'importlib.machinery', 'io', 'marshal', 'os'))),

    'msilib': (
        PythonModule(max_version=(3, 10), target='win',
                deps=('_msi', 'fnmatch', 'os', 're', 'string', 'tempfile')),
        PythonModule(min_version=(3, 11), target='win',
                deps=('_msi', 'fnmatch', 'os', 're', 'string', 'tempfile',
                        'warnings'))),

    'msvcrt':
        CoreExtensionModule(target='win'),

    'multiprocessing':
        PythonModule(deps='multiprocessing.context'),

    'multiprocessing.connection':
        PythonModule(
                deps=('multiprocessing', 'hmac', 'io', 'itertools',
                        '_multiprocessing', 'multiprocessing.context',
                        'multiprocessing.resource_sharer',
                        'multiprocessing.util', 'os', 'selectors', 'socket',
                        'struct', 'tempfile', 'time', 'win#_winapi',
                        'xmlrpc.client')),

    'multiprocessing.dummy':
        PythonModule(
                deps=('multiprocessing', 'array',
                        'multiprocessing.dummy.connection',
                        'multiprocessing.pool', 'queue', 'threading',
                        'weakref')),

    'multiprocessing.managers': (
        PythonModule(version=(3, 7),
                deps=('multiprocessing', 'array', 'multiprocessing.connection',
                        'multiprocessing.context', 'multiprocessing.pool',
                        'multiprocessing.process', 'multiprocessing.util',
                        'queue', 'threading', 'time', 'traceback')),
        PythonModule(version=(3, 8),
                deps=('multiprocessing', 'array', 'multiprocessing.connection',
                        'multiprocessing.context', 'multiprocessing.pool',
                        'multiprocessing.process',
                        '!win#multiprocessing.resource_tracker',
                        'multiprocessing.shared_memory',
                        'multiprocessing.util', 'os', 'queue', 'signal',
                        'threading', 'time', 'traceback')),
        PythonModule(min_version=(3, 9),
                deps=('multiprocessing', 'array', 'multiprocessing.connection',
                        'multiprocessing.context', 'multiprocessing.pool',
                        'multiprocessing.process',
                        '!win#multiprocessing.resource_tracker',
                        'multiprocessing.shared_memory',
                        'multiprocessing.util', 'os', 'queue', 'signal',
                        'threading', 'time', 'traceback', 'types'))),

    'multiprocessing.pool': (
        PythonModule(version=(3, 7),
                deps=('multiprocessing', 'collections', 'itertools',
                        'multiprocessing.dummy', 'multiprocessing.util',
                        'queue', 'threading', 'time', 'traceback')),
        PythonModule(version=(3, 8),
                deps=('multiprocessing', 'collections', 'itertools',
                        'multiprocessing.connection', 'multiprocessing.dummy',
                        'multiprocessing.util', 'queue', 'threading', 'time',
                        'traceback', 'warnings')),
        PythonModule(min_version=(3, 9),
                deps=('multiprocessing', 'collections', 'itertools',
                        'multiprocessing.connection', 'multiprocessing.dummy',
                        'multiprocessing.util', 'queue', 'threading', 'time',
                        'traceback', 'types', 'warnings'))),

    'multiprocessing.shared_memory': (
        PythonModule(version=(3, 8),
                deps=('multiprocessing', '!win#_posixshmem', 'win#_winapi',
                        'errno', 'mmap',
                        '!win#multiprocessing.resource_tracker', 'os',
                        'secrets', 'struct')),
        PythonModule(min_version=(3, 9), max_version=(3, 10, 5),
                deps=('multiprocessing', '!win#_posixshmem', 'win#_winapi',
                        'errno', 'mmap',
                        '!win#multiprocessing.resource_tracker', 'os',
                        'secrets', 'struct', 'types')),
        PythonModule(min_version=(3, 10, 6),
                deps=('multiprocessing', '!win#_posixshmem', 'win#_winapi',
                        'errno', 'mmap', 'multiprocessing.resource_tracker',
                        'os', 'secrets', 'struct', 'types'))),

    'multiprocessing.sharedctypes':
        PythonModule(
                deps=('multiprocessing', 'ctypes', 'multiprocessing.context',
                        'multiprocessing.heap', 'weakref')),

    'netrc':
        PythonModule(deps=('os', '!win#pwd', 'shlex', 'stat')),

    'nis':
        ExtensionModule(target='!win', source='nismodule.c',
                libs='linux#-lnsl'),

    'nntplib': (
        PythonModule(max_version=(3, 8),
                deps=('collections', 'datetime', 'email.header', 'netrc', 're',
                        'socket', '?ssl', 'warnings')),
        PythonModule(min_version=(3, 9), max_version=(3, 10),
                deps=('collections', 'datetime', 'email.header', 'netrc', 're',
                        'socket', '?ssl')),
        PythonModule(min_version=(3, 11),
                deps=('collections', 'datetime', 'email.header', 'netrc', 're',
                        'socket', '?ssl', 'warnings'))),

    'numbers':
        PythonModule(deps='abc'),

    'operator':
        PythonModule(deps=('functools', '_operator')),

    'optparse':
        PythonModule(deps=('gettext', 'os', 'textwrap')),

    'os': (
        PythonModule(version=(3, 7),
                deps=('abc', '_collections_abc', 'io', 'win#nt', 'win#ntpath',
                        '!win#posix', '!win#posixpath', 'stat', 'subprocess',
                        'warnings')),
        PythonModule(min_version=(3, 8), max_version=(3, 8, 1),
                deps=('abc', 'io', 'win#nt', 'win#ntpath', '!win#posix',
                        '!win#posixpath', 'stat', 'subprocess', 'warnings')),
        PythonModule(min_version=(3, 8, 2),
                deps=('abc', '_collections_abc', 'io', 'win#nt', 'win#ntpath',
                        '!win#posix', '!win#posixpath', 'stat', 'subprocess',
                        'warnings'))),

    'ossaudiodev':
        ExtensionModule(source='ossaudiodev.c'),

    'parser':
        ExtensionModule(source='parsermodule.c'),

    'pathlib': (
        PythonModule(max_version=(3, 9),
                deps=('_collections_abc', 'errno', 'fnmatch', 'functools',
                        '!win#grp', 'io', 'win#nt', 'ntpath', 'operator', 'os',
                        'posixpath', '!win#pwd', 're', 'stat',
                        'urllib.parse')),
        PythonModule(min_version=(3, 10),
                deps=('_collections_abc', 'errno', 'fnmatch', 'functools',
                        '!win#grp', 'io', 'ntpath', 'operator', 'os',
                        'posixpath', '!win#pwd', 're', 'stat', 'urllib.parse',
                        'warnings'))),

    'pdb': (
        PythonModule(max_version=(3, 8, 0),
                deps=('bdb', 'cmd', 'code', 'dis', 'glob', 'inspect',
                        'linecache', 'os', 'pprint', 'pydoc', 're', 'runpy',
                        'shlex', 'signal', 'traceback')),
        PythonModule(min_version=(3, 8, 1), max_version=(3, 8, 3),
                deps=('bdb', 'cmd', 'code', 'dis', 'glob', 'inspect', 'io',
                        'linecache', 'os', 'pprint', 'pydoc', 're', 'runpy',
                        'shlex', 'signal', 'traceback')),
        PythonModule(min_version=(3, 8, 4), max_version=(3, 10),
                deps=('bdb', 'cmd', 'code', 'dis', 'glob', 'inspect', 'io',
                        'linecache', 'os', 'pprint', 'pydoc', 're', 'runpy',
                        'shlex', 'signal', 'tokenize', 'traceback')),
        PythonModule(min_version=(3, 11),
                deps=('bdb', 'cmd', 'code', 'dis', 'functools', 'glob',
                        'inspect', 'io', 'linecache', 'os', 'pprint', 'pydoc',
                        're', 'runpy', 'shlex', 'signal', 'tokenize',
                        'traceback', 'typing'))),

    'pickle':
        PythonModule(
                deps=('codecs', '_compat_pickle', 'copyreg', 'functools', 'io',
                        'itertools', 'marshal', '_pickle', 're', 'struct',
                        'types')),

    'pickletools':
        PythonModule(deps=('codecs', 'io', 'pickle', 're', 'struct')),

    'pipes': (
        PythonModule(max_version=(3, 10), target='!win',
                deps=('os', 're', 'shlex', 'tempfile')),
        PythonModule(min_version=(3, 11), target='!win',
                deps=('os', 're', 'shlex', 'tempfile', 'warnings'))),

    'pkgutil': (
        PythonModule(max_version=(3, 8),
                deps=('collections', 'functools', 'importlib',
                        'importlib.machinery', 'importlib.util', 'inspect',
                        'marshal', 'os', 'types', 'warnings')),
        PythonModule(min_version=(3, 9),
                deps=('collections', 'functools', 'importlib',
                        'importlib.machinery', 'importlib.util', 'inspect',
                        'marshal', 'os', 're', 'types', 'warnings'))),

    'platform': (
        PythonModule(version=(3, 7),
                deps=('collections', 'os', 'plistlib', 're', 'socket',
                        'struct', 'subprocess', 'warnings', 'win#winreg')),
        PythonModule(version=(3, 8),
                deps=('collections', 'os', 'plistlib', 're', 'socket',
                        'struct', 'subprocess', 'win#winreg')),
        PythonModule(min_version=(3, 9),
                deps=('collections', 'functools', 'itertools', 'os',
                        'plistlib', 're', 'socket', 'struct', 'subprocess',
                        'win#winreg'))),

    'plistlib': (
        PythonModule(max_version=(3, 8),
                deps=('binascii', 'codecs', 'contextlib', 'datetime', 'enum',
                        'io', 'itertools', 'os', 're', 'struct', 'warnings',
                        'xml.parsers.expat')),
        PythonModule(min_version=(3, 9),
                deps=('binascii', 'codecs', 'datetime', 'enum', 'io',
                        'itertools', 'os', 're', 'struct',
                        'xml.parsers.expat'))),

    'poplib':
        PythonModule(
                deps=('errno', 'hashlib', 're', 'socket', '?ssl', 'warnings')),

    'posix':
        CoreExtensionModule(target='!win'),

    'pprint': (
        PythonModule(max_version=(3, 9),
                deps=('collections', 'io', 're', 'time', 'types')),
        PythonModule(min_version=(3, 10),
                deps=('collections', 'dataclasses', 'io', 're', 'time',
                        'types'))),

    'profile':
        PythonModule(deps=('marshal', 'pstats', 'time')),

    'pstats': (
        PythonModule(max_version=(3, 8),
                deps=('enum', 'functools', 'marshal', 'os', 're', 'time')),
        PythonModule(min_version=(3, 9),
                deps=('dataclasses', 'enum', 'functools', 'marshal', 'os',
                        're', 'time', 'typing'))),

    'pty':
        PythonModule(target='!win', deps=('fcntl', 'os', 'select', 'tty')),

    'pwd':
        CoreExtensionModule(target='!win'),

    'py_compile':
        PythonModule(
                deps=('enum', 'importlib._bootstrap_external',
                        'importlib.machinery', 'importlib.util', 'os',
                        'traceback')),

    'pyclbr': (
        PythonModule(max_version=(3, 9),
                deps=('importlib.util', 'io', 'token', 'tokenize')),
        PythonModule(min_version=(3, 10), deps=('ast', 'importlib.util'))),

    'pydoc': (
        PythonModule(max_version=(3, 7, 6),
                deps=('collections', 'email.message', 'http.server',
                        'importlib._bootstrap',
                        'importlib._bootstrap_external', 'importlib.machinery',
                        'importlib.util', 'inspect', 'io', 'os', 'pkgutil',
                        'platform', 're', 'reprlib', 'select', 'subprocess',
                        'tempfile', 'textwrap', 'threading', 'time',
                        'tokenize', 'traceback', '?tty', 'urllib.parse',
                        'warnings')),
        PythonModule(min_version=(3, 7, 7), max_version=(3, 7),
                deps=('collections', 'email.message', 'http.server',
                        'importlib._bootstrap',
                        'importlib._bootstrap_external', 'importlib.machinery',
                        'importlib.util', 'inspect', 'io', 'os', 'pkgutil',
                        'platform', 're', 'reprlib', 'select', 'subprocess',
                        'sysconfig', 'tempfile', 'textwrap', 'threading',
                        'time', 'tokenize', 'traceback', '?tty',
                        'urllib.parse', 'warnings')),
        PythonModule(min_version=(3, 8), max_version=(3, 8, 1),
                deps=('collections', 'email.message', 'http.server',
                        'importlib._bootstrap',
                        'importlib._bootstrap_external', 'importlib.machinery',
                        'importlib.util', 'inspect', 'io', 'os', 'pkgutil',
                        'platform', 're', 'reprlib', 'select', 'subprocess',
                        'tempfile', 'textwrap', 'threading', 'time',
                        'tokenize', 'traceback', '?tty', 'urllib.parse',
                        'warnings')),
        PythonModule(min_version=(3, 8, 2), max_version=(3, 9, 11),
                deps=('collections', 'email.message', 'http.server',
                        'importlib._bootstrap',
                        'importlib._bootstrap_external', 'importlib.machinery',
                        'importlib.util', 'inspect', 'io', 'os', 'pkgutil',
                        'platform', 're', 'reprlib', 'select', 'subprocess',
                        'sysconfig', 'tempfile', 'textwrap', 'threading',
                        'time', 'tokenize', 'traceback', '?tty',
                        'urllib.parse', 'warnings')),
        PythonModule(min_version=(3, 9, 12), max_version=(3, 9),
                deps=('collections', 'email.message', 'http.server',
                        'importlib._bootstrap',
                        'importlib._bootstrap_external', 'importlib.machinery',
                        'importlib.util', 'inspect', 'io', 'os', 'pkgutil',
                        'platform', 're', 'reprlib', 'select', 'subprocess',
                        'sysconfig', 'tempfile', 'textwrap', 'threading',
                        'time', 'tokenize', 'traceback', '?tty', 'types',
                        'urllib.parse', 'warnings')),
        PythonModule(min_version=(3, 10), max_version=(3, 10, 3),
                deps=('collections', 'email.message', 'http.server',
                        'importlib._bootstrap',
                        'importlib._bootstrap_external', 'importlib.machinery',
                        'importlib.util', 'inspect', 'io', 'os', 'pkgutil',
                        'platform', 're', 'reprlib', 'select', 'subprocess',
                        'sysconfig', 'tempfile', 'textwrap', 'threading',
                        'time', 'tokenize', 'traceback', '?tty',
                        'urllib.parse', 'warnings')),
        PythonModule(min_version=(3, 10, 4), max_version=(3, 10),
                deps=('collections', 'email.message', 'http.server',
                        'importlib._bootstrap',
                        'importlib._bootstrap_external', 'importlib.machinery',
                        'importlib.util', 'inspect', 'io', 'os', 'pkgutil',
                        'platform', 're', 'reprlib', 'select', 'subprocess',
                        'sysconfig', 'tempfile', 'textwrap', 'threading',
                        'time', 'tokenize', 'traceback', '?tty', 'types',
                        'urllib.parse', 'warnings')),
        PythonModule(min_version=(3, 11),
                deps=('collections', 'email.message', 'http.server',
                        'importlib._bootstrap',
                        'importlib._bootstrap_external', 'importlib.machinery',
                        'importlib.util', 'inspect', 'io', 'os', 'pkgutil',
                        'platform', 're', 'reprlib', 'select', 'subprocess',
                        'sysconfig', 'tempfile', 'textwrap', 'threading',
                        'time', 'tokenize', 'traceback', '?tty',
                        'urllib.parse', 'warnings'))),

    'queue': (
        PythonModule(max_version=(3, 8),
                deps=('collections', 'heapq', '_queue', 'threading', 'time')),
        PythonModule(min_version=(3, 9),
                deps=('collections', 'heapq', '_queue', 'threading', 'time',
                        'types'))),

    'quopri':
        PythonModule(deps=('binascii', 'io')),

    'random': (
        PythonModule(version=(3, 7),
                deps=('bisect', '_collections_abc', 'hashlib', 'itertools',
                        'math', 'os', '_random', 'types', 'warnings')),
        PythonModule(min_version=(3, 8), max_version=(3, 9),
                deps=('bisect', '_collections_abc', 'itertools', 'math', 'os',
                        '_random', '_sha512', 'warnings')),
        PythonModule(min_version=(3, 10),
                deps=('bisect', '_collections_abc', 'itertools', 'math',
                        'operator', 'os', '_random', '_sha512', 'warnings'))),

    're': (
        PythonModule(max_version=(3, 10),
                deps=('copyreg', 'enum', 'functools', '_locale', 'sre_compile',
                        'sre_constants', 'sre_parse')),
        PythonModule(min_version=(3, 11),
                deps=('copyreg', 'enum', 'functools', 're._compiler',
                        're._constants', 're._parser'))),

    'readline':
        ExtensionModule(target='!win', source='readline.c',
                deps='Readline:readline'),

    'reprlib':
        PythonModule(deps=('itertools', '_thread')),

    'resource':
        ExtensionModule(target='!win', source='resource.c'),

    'rlcompleter': (
        PythonModule(max_version=(3, 9),
                deps=('atexit', 'keyword', 're', 'readline')),
        PythonModule(min_version=(3, 10),
                deps=('atexit', 'inspect', 'keyword', 're', 'readline'))),

    'runpy': (
        PythonModule(max_version=(3, 8, 0),
                deps=('importlib.machinery', 'importlib.util', 'pkgutil',
                        'types', 'warnings')),
        PythonModule(min_version=(3, 8, 1), max_version=(3, 8, 2),
                deps=('importlib.machinery', 'importlib.util', 'io', 'pkgutil',
                        'types', 'warnings')),
        PythonModule(min_version=(3, 8, 3), max_version=(3, 10),
                deps=('importlib.machinery', 'importlib.util', 'io', 'os',
                        'pkgutil', 'types', 'warnings')),
        PythonModule(min_version=(3, 11),
                deps=('importlib.machinery', 'importlib.util', 'io', 'os',
                        'pkgutil', 'warnings'))),

    'sched': (
        PythonModule(max_version=(3, 9),
                deps=('collections', 'heapq', 'threading', 'time')),
        PythonModule(min_version=(3, 10),
                deps=('collections', 'heapq', 'itertools', 'threading',
                        'time'))),

    'secrets': (
        PythonModule(max_version=(3, 8),
                deps=('base64', 'binascii', 'hmac', 'os', 'random')),
        PythonModule(min_version=(3, 9),
                deps=('base64', 'binascii', 'hmac', 'random'))),

    'select':
        ExtensionModule(source='selectmodule.c', pyd='select.pyd'),

    'selectors':
        PythonModule(
                deps=('abc', 'collections', 'collections.abc', 'math',
                        'select')),

    'shelve':
        PythonModule(deps=('collections.abc', 'dbm', 'io', 'pickle')),

    'shlex':
        PythonModule(deps=('collections', 'io', 'os', 're')),

    'shutil': (
        PythonModule(version=(3, 7),
                deps=('?bz2', 'collections', 'errno', 'fnmatch', '!win#grp',
                        '?lzma', 'win#nt', 'os', '!win#pwd', 'stat', 'tarfile',
                        'zipfile', '?zlib')),
        PythonModule(min_version=(3, 8),
                deps=('?bz2', 'collections', 'errno', 'fnmatch', '!win#grp',
                        '?lzma', 'win#nt', 'os', '!win#posix', '!win#pwd',
                        'stat', 'tarfile', 'zipfile', '?zlib'))),

    'signal': (
        PythonModule(max_version=(3, 9, 9),
                deps=('enum', 'functools', '_signal')),
        PythonModule(min_version=(3, 9, 10), max_version=(3, 9),
                deps=('enum', '_signal')),
        PythonModule(min_version=(3, 10), max_version=(3, 10, 1),
                deps=('enum', 'functools', '_signal')),
        PythonModule(min_version=(3, 10, 2), deps=('enum', '_signal'))),

    'smtpd':
        PythonModule(
                deps=('asynchat', 'asyncore', 'collections',
                        'email._header_value_parser', 'errno', 'getopt', 'os',
                        'smtplib', 'socket', 'time', 'warnings')),

    'smtplib':
        PythonModule(
                deps=('base64', 'copy', 'datetime', 'email.base64mime',
                        'email.generator', 'email.message', 'email.utils',
                        'hmac', 'io', 're', 'socket', '?ssl', 'warnings')),

    'sndhdr': (
        PythonModule(max_version=(3, 10),
                deps=('aifc', 'collections', 'wave')),
        PythonModule(min_version=(3, 11),
                deps=('aifc', 'collections', 'warnings', 'wave'))),

    'spwd':
        ExtensionModule(target='!win', source='spwdmodule.c'),

    'socket': (
        PythonModule(max_version=(3, 8),
                deps=('errno', 'enum', 'io', 'os', 'selectors', '_socket')),
        PythonModule(min_version=(3, 9),
                deps=('array', 'errno', 'enum', 'io', 'os', 'selectors',
                        '_socket'))),

    'socketserver':
        PythonModule(
                deps=('io', 'os', 'selectors', 'socket', 'time', 'traceback',
                        'threading')),

    'sqlite3':
        PythonModule(deps='sqlite3.dbapi2'),

    'ssl':
        PythonModule(
                deps=('base64', 'calendar', 'collections', 'enum', 'errno',
                        'os', 'socket', '_ssl', 'time', 'warnings')),

    'stat':
        PythonModule(deps='_stat'),

    'statistics': (
        PythonModule(version=(3, 7),
                deps=('bisect', 'collections', 'decimal', 'fractions',
                        'itertools', 'math', 'numbers')),
        PythonModule(min_version=(3, 8), max_version=(3, 10),
                deps=('bisect', 'collections', 'decimal', 'fractions',
                        'itertools', 'math', 'numbers', 'operator',
                        'random')),
        PythonModule(min_version=(3, 11),
                deps=('bisect', 'collections', 'decimal', 'fractions',
                        'functools', 'itertools', 'math', 'numbers',
                        'operator', 'random'))),

    'string':
        PythonModule(deps=('collections', 're', '_string')),

    'stringprep':
        PythonModule(deps='unicodedata'),

    'struct':
        PythonModule(deps='_struct'),

    'subprocess': (
        PythonModule(version=(3, 7),
                deps=('errno', 'gc', 'io', 'win#msvcrt', 'os',
                        '!win#_posixsubprocess', '!win#select',
                        '!win#selectors', 'signal', 'threading', 'time',
                        'traceback', 'warnings', 'win#_winapi')),
        PythonModule(version=(3, 8),
                deps=('contextlib', 'errno', 'gc', 'io', 'win#msvcrt', 'os',
                        '!win#_posixsubprocess', '!win#select',
                        '!win#selectors', 'signal', 'threading', 'time',
                        'traceback', 'warnings', 'win#_winapi')),
        PythonModule(version=(3, 9),
                deps=('contextlib', 'errno', 'gc', '!win#grp', 'io',
                        'win#msvcrt', 'os', '!win#_posixsubprocess',
                        '!win#pwd', '!win#select', '!win#selectors', 'signal',
                        'threading', 'time', 'traceback', 'types', 'warnings',
                        'win#_winapi')),
        PythonModule(version=(3, 10),
                deps=('contextlib', 'errno', '!win#fcntl', 'gc', '!win#grp',
                        'io', 'win#msvcrt', 'os', '!win#_posixsubprocess',
                        '!win#pwd', '!win#select', '!win#selectors', 'signal',
                        'threading', 'time', 'traceback', 'types', 'warnings',
                        'win#_winapi')),
        PythonModule(min_version=(3, 11),
                deps=('contextlib', 'errno', '!win#fcntl', 'gc', '!win#grp',
                        'io', 'locale', 'win#msvcrt', 'os',
                        '!win#_posixsubprocess', '!win#pwd', '!win#select',
                        '!win#selectors', 'signal', 'threading', 'time',
                        'traceback', 'types', 'warnings', 'win#_winapi'))),

    'sunau': (
        PythonModule(max_version=(3, 8),
                deps=('audioop', 'collections', 'warnings')),
        PythonModule(min_version=(3, 9), max_version=(3, 10),
                deps=('audioop', 'collections')),
        PythonModule(min_version=(3, 11),
                deps=('audioop', 'collections', 'warnings'))),

    'symbol': (
        PythonModule(max_version=(3, 8)),
        PythonModule(version=(3, 9), deps='warnings')),

    'symtable':
        PythonModule(deps=('_symtable', 'weakref')),

    'sysconfig': (
        PythonModule(max_version=(3, 8, 6),
                deps=('os', 'ios|macos#_osx_support', 'pprint', 're',
                        'android#_sysconfigdata_m_linux_android',
                        'ios#_sysconfigdata_m_darwin_ios',
                        'macos#_sysconfigdata_m_darwin_darwin',
                        'linux#_sysconfigdata_m_linux_x86_64-linux-gnu',
                        'ios|macos#types', 'warnings')),
        PythonModule(min_version=(3, 8, 7), max_version=(3, 8),
                deps=('win#_imp', 'os', 'ios|macos#_osx_support', 'pprint',
                        're', 'android#_sysconfigdata_m_linux_android',
                        'ios#_sysconfigdata_m_darwin_ios',
                        'macos#_sysconfigdata_m_darwin_darwin',
                        'linux#_sysconfigdata_m_linux_x86_64-linux-gnu',
                        'ios|macos#types', 'warnings')),
        PythonModule(min_version=(3, 9), max_version=(3, 9, 1),
                deps=('os', 'ios|macos#_osx_support', 'pprint', 're',
                        'android#_sysconfigdata_m_linux_android',
                        'ios#_sysconfigdata_m_darwin_ios',
                        'macos#_sysconfigdata_m_darwin_darwin',
                        'linux#_sysconfigdata_m_linux_x86_64-linux-gnu',
                        'ios|macos#types', 'warnings')),
        PythonModule(min_version=(3, 9, 2),
                deps=('win#_imp', 'os', 'ios|macos#_osx_support', 'pprint',
                        're', 'android#_sysconfigdata_m_linux_android',
                        'ios#_sysconfigdata_m_darwin_ios',
                        'macos#_sysconfigdata_m_darwin_darwin',
                        'linux#_sysconfigdata_m_linux_x86_64-linux-gnu',
                        'ios|macos#types', 'warnings'))),

    'syslog':
        ExtensionModule(target='!win', source='syslogmodule.c'),

    'tabnanny':
        PythonModule(deps=('os', 'tokenize')),

    'tarfile': (
        PythonModule(version=(3, 7),
                deps=('calendar', 'copy', 'errno', 'io', 'os', 're', 'shutil',
                        'stat', 'struct', 'time', 'warnings')),
        PythonModule(min_version=(3, 8), max_version=(3, 9, 7),
                deps=('calendar', 'copy', 'errno', 'io', 'os', 're', 'shutil',
                        'stat', 'struct', 'time')),
        PythonModule(min_version=(3, 9, 8),
                deps=('calendar', 'copy', 'errno', 'io', 'os', 're', 'shutil',
                        'stat', 'struct', 'time', 'zlib'))),

    'telnetlib': (
        PythonModule(max_version=(3, 10),
                deps=('errno', 're', 'selectors', 'socket', '_thread',
                        'time')),
        PythonModule(min_version=(3, 11),
                deps=('errno', 're', 'selectors', 'socket', '_thread',
                        'time', 'warnings'))),

    'tempfile': (
        PythonModule(max_version=(3, 8),
                deps=('errno', 'functools', 'io', 'os', 'random', 'shutil',
                        '_thread', 'warnings', 'weakref')),
        PythonModule(min_version=(3, 9),
                deps=('errno', 'functools', 'io', 'os', 'random', 'shutil',
                        '_thread', 'types', 'warnings', 'weakref'))),

    'termios':
        ExtensionModule(target='!win', source='termios.c'),

    'textwrap':
        PythonModule(deps='re'),

    'threading': (
        PythonModule(max_version=(3, 7, 2),
                deps=('_collections', 'itertools', 'os', '_thread', 'time',
                        'traceback', '_weakrefset')),
        PythonModule(min_version=(3, 7, 3), max_version=(3, 7),
                deps=('_collections', 'itertools', 'os', '_thread', 'time',
                        'traceback', 'warnings', '_weakrefset')),
        PythonModule(version=(3, 8),
                deps=('_collections', 'itertools', 'os', '_thread', 'time',
                        'warnings', '_weakrefset')),
        PythonModule(min_version=(3, 9),
                deps=('_collections', 'functools', 'itertools', 'os',
                        '_thread', 'time', '_weakrefset'))),

    'time':
        CoreExtensionModule(),

    'timeit':
        PythonModule(
                deps=('gc', 'itertools', 'linecache', 'time', 'traceback')),

    'token':
        PythonModule(),

    'tokenize': (
        PythonModule(max_version=(3, 9),
                deps=('codecs', 'collections', 'io', 'itertools', 're',
                        'token')),
        PythonModule(min_version=(3, 10),
                deps=('codecs', 'collections', 'functools', 'io', 'itertools',
                        're', 'token'))),

    'tomllib':
        PythonModule(min_version=(3, 11), deps='tomllib._parser'),

    'trace': (
        PythonModule(max_version=(3, 7, 6),
                deps=('dis', 'gc', 'inspect', 'linecache', 'os', 'pickle',
                        're', 'threading', 'time', 'token', 'tokenize')),
        PythonModule(min_version=(3, 7, 7), max_version=(3, 7),
                deps=('dis', 'gc', 'inspect', 'linecache', 'os', 'pickle',
                        're', 'sysconfig', 'threading', 'time', 'token',
                        'tokenize')),
        PythonModule(min_version=(3, 8), max_version=(3, 8, 1),
                deps=('dis', 'gc', 'inspect', 'linecache', 'os', 'pickle',
                        'threading', 'time', 'token', 'tokenize')),
        PythonModule(min_version=(3, 8, 2),
                deps=('dis', 'gc', 'inspect', 'linecache', 'os', 'pickle',
                        'sysconfig', 'threading', 'time', 'token',
                        'tokenize'))),

    'traceback': (
        PythonModule(max_version=(3, 10),
                deps=('collections', 'itertools', 'linecache')),
        PythonModule(min_version=(3, 11),
                deps=('ast', 'collections.abc', 'contextlib', 'itertools',
                        'linecache', 'textwrap'))),

    'tracemalloc':
        PythonModule(
                deps=('collections.abc', 'fnmatch', 'functools', 'linecache',
                        'os', 'pickle', '_tracemalloc')),

    'tty':
        PythonModule(target='!win', deps='termios'),

    'types':
        PythonModule(deps=('_collections_abc', 'functools')),

    'typing': (
        PythonModule(max_version=(3, 10),
                deps=('abc', 'collections', 'collections.abc', 'contextlib',
                        'functools', 'operator', 're', 'types')),
        PythonModule(min_version=(3, 11),
                deps=('abc', 'collections', 'collections.abc', 'contextlib',
                        'functools', 'operator', 're', 'types', 'warnings'))),

    'unicodedata': (
        ExtensionModule(max_version=(3, 9),
                source='unicodedata.c', pyd='unicodedata.pyd'),
        ExtensionModule(min_version=(3, 10),
                source='unicodedata.c', defines='Py_BUILD_CORE_MODULE',
                pyd='unicodedata.pyd')),

    'urllib':
        PythonModule(),

    'urllib.error':
        PythonModule(deps=('urllib', 'urllib.response')),

    'urllib.parse': (
        PythonModule(max_version=(3, 7, 2),
                deps=('urllib', 'collections', 're')),
        PythonModule(min_version=(3, 7, 3), max_version=(3, 7),
                deps=('urllib', 'collections', 're', 'unicodedata')),
        PythonModule(version=(3, 8),
                deps=('urllib', 'collections', 're', 'unicodedata',
                        'warnings')),
        PythonModule(min_version=(3, 9), max_version=(3, 10),
                deps=('urllib', 'collections', 're', 'types', 'unicodedata',
                        'warnings')),
        PythonModule(min_version=(3, 11),
                deps=('urllib', 'collections', 'functools', 're', 'types',
                        'unicodedata', 'warnings'))),

    'urllib.request':
        PythonModule(
                deps=('urllib', 'base64', 'bisect', 'contextlib', 'email',
                        'email.utils', 'macos#fnmatch', 'ftplib', 'getpass',
                        'hashlib', 'http.client', 'http.cookiejar', 'io',
                        'mimetypes', 'win#nturl2path', 'os', 'posixpath', 're',
                        'macos#_scproxy', 'socket', '?ssl', 'string',
                        'tempfile', 'time', 'urllib.error', 'urllib.parse',
                        'urllib.response', 'warnings', 'win#winreg')),

    'urllib.response':
        PythonModule(
                deps=('urllib', 'collections', 'tempfile', 'urllib.parse',
                        'urllib.request')),

    'urllib.robotparser':
        PythonModule(
                deps=('urllib', 'time', 'urllib.parse', 'urllib.request')),

    'uu': (
        PythonModule(max_version=(3, 10), deps=('binascii', 'os')),
        PythonModule(min_version=(3, 11),
                deps=('binascii', 'os', 'warnings'))),

    'uuid': (
        PythonModule(version=(3, 7),
                deps=('linux|macos|win#ctypes', 'enum', 'hashlib', 'os',
                        'random', 'shutil', 'socket', 'subprocess', 'time',
                        'ios|macos#_uuid', 'warnings')),
        PythonModule(min_version=(3, 8), max_version=(3, 8, 5),
                deps=('linux|macos|win#ctypes', 'enum', 'hashlib', 'os',
                        'platform', 'random', 'shutil', 'socket', 'subprocess',
                        'time', 'ios|macos#_uuid', 'warnings')),
        PythonModule(min_version=(3, 8, 6), max_version=(3, 8),
                deps=('linux|macos|win#ctypes', 'enum', 'hashlib', 'os',
                        'android|linux#platform', 'random', 'shutil', 'socket',
                        'subprocess', 'time', 'ios|macos#_uuid', 'warnings')),
        PythonModule(min_version=(3, 9), max_version=(3, 9, 7),
                deps=('enum', 'hashlib', 'io', 'os', 'android|linux#platform',
                        'random', 'shutil', 'socket', 'subprocess', 'time',
                        'ios|macos#_uuid')),
        PythonModule(min_version=(3, 9, 8),
                deps=('enum', 'hashlib', 'io', 'os', 'android|linux#platform',
                        'random', 'shutil', 'socket', 'subprocess', 'time',
                        'ios|linux|macos#_uuid'))),

    'warnings':
        PythonModule(deps=('linecache', 're', 'traceback', '_warnings')),

    'wave': (
        PythonModule(max_version=(3, 8),
                deps=('audioop', 'chunk', 'collections', 'struct',
                        'warnings')),
        PythonModule(min_version=(3, 9), max_version=(3, 10),
                deps=('audioop', 'chunk', 'collections', 'struct')),
        PythonModule(min_version=(3, 11), deps=('collections', 'struct'))),

    'weakref':
        PythonModule(
                deps=('atexit', '_collections_abc', 'copy', 'gc', 'itertools',
                        '_weakref', '_weakrefset')),

    'webbrowser': (
        PythonModule(max_version=(3, 10),
                deps=('copy', 'glob', 'os', '!win#pwd', 'shlex', 'shutil',
                        'socket', 'subprocess', 'tempfile', 'threading')),
        PythonModule(min_version=(3, 11),
                deps=('copy', 'glob', 'os', '!win#pwd', 'shlex', 'shutil',
                        'socket', 'subprocess', 'tempfile', 'threading',
                        'warnings'))),

    'winreg':
        CoreExtensionModule(target='win'),

    'winsound':
        ExtensionModule(target='win', source='../PC/winsound.c',
                libs='-lwinmm', pyd='winsound.pyd'),

    'wsgiref':
        PythonModule(),

    'wsgiref.handlers':
        PythonModule(
                deps=('wsgiref', 'os', 'time', 'traceback', 'warnings',
                        'wsgiref.headers', 'wsgiref.util')),

    'wsgiref.headers':
        PythonModule(deps=('wsgiref', 're')),

    'wsgiref.simple_server':
        PythonModule(
                deps=('wsgiref', 'http.server', 'platform', 'urllib.parse',
                        'wsgiref.handlers')),

    'wsgiref.types':
        PythonModule(min_version=(3, 11),
                deps=('wsgiref', 'collections', 'types', 'typing')),

    'wsgiref.util':
        PythonModule(deps=('wsgiref', 'posixpath', 'urllib.parse')),

    'wsgiref.validate':
        PythonModule(deps=('wsgiref', 're', 'warnings')),

    'xdrlib': (
        PythonModule(max_version=(3, 10), deps=('functools', 'io', 'struct')),
        PythonModule(min_version=(3, 11),
                deps=('functools', 'io', 'struct', 'warnings'))),

    'xml':
        PythonModule(),

    'xml.dom':
        PythonModule(deps=('xml', 'xml.dom.domreg')),

    'xml.dom.minidom':
        PythonModule(
                deps=('xml.dom', 'codecs', 'io', 'xml.dom.minicompat',
                        'xml.dom.xmlbuilder')),

    'xml.dom.pulldom':
        PythonModule(
                deps=('xml.dom', 'io', 'xml.dom.minidom', 'xml.sax.handler')),

    'xml.etree':
        PythonModule(deps='xml'),

    'xml.etree.ElementTree': (
        PythonModule(max_version=(3, 9, 12),
                deps=('xml.etree', 'collections', 'collections.abc',
                        'contextlib', '_elementtree', 'io', 'locale', 're',
                        'warnings', 'xml.etree.ElementPath',
                        'xml.parsers.expat')),
        PythonModule(min_version=(3, 9, 13), max_version=(3, 9),
                deps=('xml.etree', 'collections', 'collections.abc',
                        'contextlib', '_elementtree', 'io', 're', 'warnings',
                        'xml.etree.ElementPath', 'xml.parsers.expat')),
        PythonModule(min_version=(3, 10), max_version=(3, 10, 4),
                deps=('xml.etree', 'collections', 'collections.abc',
                        'contextlib', '_elementtree', 'io', 'locale', 're',
                        'warnings', 'xml.etree.ElementPath',
                        'xml.parsers.expat')),
        PythonModule(min_version=(3, 10, 5),
                deps=('xml.etree', 'collections', 'collections.abc',
                        'contextlib', '_elementtree', 'io', 're', 'warnings',
                        'xml.etree.ElementPath', 'xml.parsers.expat'))),

    'xml.parsers':
        PythonModule(deps='xml'),

    'xml.parsers.expat':
        PythonModule(deps=('xml.parsers', 'pyexpat')),

    'xml.sax':
        PythonModule(
                deps=('xml.sax', 'io', 'os', 'xml.sax._exceptions',
                        'xml.sax.handler', 'xml.sax.xmlreader')),

    'xml.sax.handler':
        PythonModule(deps='xml.sax'),

    'xml.sax.saxutils':
        PythonModule(
                deps=('xml.sax', 'codecs', 'io', 'os', 'urllib.parse',
                        'urllib.request', 'xml.sax.handler',
                        'xml.sax.xmlreader')),

    'xml.sax.xmlreader':
        PythonModule(
                deps=('xml.sax', 'xml.sax._exceptions', 'xml.sax.handler',
                        'xml.sax.saxutils')),

    'xmlrpc':
        PythonModule(),

    'xmlrpc.client':
        PythonModule(
                deps=('xmlrpc', 'base64', 'datetime', 'decimal', 'errno',
                        'http.client', 'io', 'socket', 'time', 'urllib.parse',
                        'xml.parsers.expat')),

    'xmlrpc.server': (
        PythonModule(max_version=(3, 7, 4),
                deps=('xmlrpc', '!win#fcntl', 'functools', 'http.server',
                        'inspect', 'os', 'pydoc', 're', 'socketserver',
                        'traceback', 'xmlrpc.client')),
        PythonModule(min_version=(3, 7, 5),
                deps=('xmlrpc', '!win#fcntl', 'functools', 'html',
                        'http.server', 'inspect', 'os', 'pydoc', 're',
                        'socketserver', 'traceback', 'xmlrpc.client'))),

    'zipapp':
        PythonModule(
                deps=('contextlib', 'os', 'pathlib', 'shutil', 'stat',
                        'zipfile')),

    'zipfile': (
        PythonModule(version=(3, 7),
                deps=('binascii', 'importlib.util', 'io', 'os', 'shutil',
                        'stat', 'struct', 'threading', 'time', 'warnings',
                        'zlib')),
        PythonModule(min_version=(3, 8), max_version=(3, 8, 1),
                deps=('binascii', 'functools', 'importlib.util', 'io',
                        'itertools', 'os', 'posixpath', 'shutil', 'stat',
                        'struct', 'threading', 'time', 'warnings', 'zlib')),
        PythonModule(version=(3, 8, 2),
                deps=('binascii', 'collections', 'contextlib', 'functools',
                        'importlib.util', 'io', 'itertools', 'os', 'posixpath',
                        'shutil', 'stat', 'struct', 'threading', 'time',
                        'warnings', 'zlib')),
        PythonModule(min_version=(3, 8, 3), max_version=(3, 8),
                deps=('binascii', 'contextlib', 'functools', 'importlib.util',
                        'io', 'itertools', 'os', 'posixpath', 'shutil', 'stat',
                        'struct', 'threading', 'time', 'warnings', 'zlib')),
        PythonModule(version=(3, 9),
                deps=('binascii', 'contextlib', 'importlib.util', 'io',
                        'itertools', 'os', 'posixpath', 'shutil', 'stat',
                        'struct', 'threading', 'time', 'warnings', 'zlib')),
        PythonModule(min_version=(3, 10),
                deps=('binascii', 'contextlib', 'importlib.util', 'io',
                        'itertools', 'os', 'pathlib', 'posixpath', 'shutil',
                        'stat', 'struct', 'threading', 'time', 'warnings',
                        'zlib'))),

    'zipimport': (
        CoreExtensionModule(version=(3, 7), deps='zlib'),
        PythonModule(min_version=(3, 8), max_version=(3, 9),
                deps=('_imp', 'importlib.abc', 'io', '_io', 'marshal',
                        'pathlib', 'time')),
        PythonModule(min_version=(3, 10),
                deps=('_imp', 'importlib.readers', '_io', 'marshal', 'time',
                        '_warnings'))),

    'zlib':
        ExtensionModule(source='zlibmodule.c', deps='zlib:zlib'),

    'zoneinfo':
        PythonModule(min_version=(3, 9),
                deps=('zoneinfo._common', 'zoneinfo._tzpath',
                        'zoneinfo._zoneinfo')),

    # These are internal modules.

    # For Python v3.7.0 to v3.7.2 on Windows this module cannot be linked
    # separately because of the PyVarObject_HEAD_INIT() bug.  In these cases it
    # is included in the static Python library build by pyqtdeploy-sysroot.
    '_abc': (
        ExtensionModule(max_version=(3, 7, 2), internal=True,
                source='!win#_abc.c'),
        ExtensionModule(min_version=(3, 7, 3), max_version=(3, 9),
                internal=True,
                source='_abc.c'),
        ExtensionModule(version=(3, 10), internal=True,
                source='_abc.c', defines='Py_BUILD_CORE_MODULE'),
        CoreExtensionModule(min_version=(3, 11), internal=True)),

    '_ast':
        CoreExtensionModule(internal=True),

    '_asyncio': (
        ExtensionModule(max_version=(3, 8), internal=True,
                source='_asynciomodule.c', pyd='_asyncio.pyd'),
        ExtensionModule(min_version=(3, 9), internal=True,
                source='_asynciomodule.c', defines='Py_BUILD_CORE_MODULE',
                pyd='_asyncio.pyd')),

    'asyncio.base_events': (
        PythonModule(version=(3, 7), internal=True,
                deps=('asyncio', 'asyncio.constants', 'asyncio.coroutines',
                        'asyncio.events', 'asyncio.futures', 'asyncio.log',
                        'asyncio.protocols', 'asyncio.sslproto',
                        'asyncio.tasks', 'asyncio.transports', 'collections',
                        'collections.abc', 'concurrent.futures', 'heapq',
                        'itertools', 'logging', 'os', 'socket', '?ssl',
                        'subprocess', 'threading', 'time', 'traceback',
                        'warnings', 'weakref')),
        PythonModule(min_version=(3, 8), internal=True,
                deps=('asyncio', 'asyncio.constants', 'asyncio.coroutines',
                        'asyncio.events', 'asyncio.exceptions',
                        'asyncio.futures', 'asyncio.log', 'asyncio.protocols',
                        'asyncio.sslproto', 'asyncio.staggered',
                        'asyncio.tasks', 'asyncio.transports',
                        'asyncio.trsock', 'collections', 'collections.abc',
                        'concurrent.futures', 'functools', 'heapq',
                        'itertools', 'os', 'socket', '?ssl', 'stat',
                        'subprocess', 'threading', 'time', 'traceback',
                        'warnings', 'weakref'))),

    'asyncio.base_futures': (
        PythonModule(version=(3, 7), internal=True,
                deps=('asyncio', 'asyncio.format_helpers',
                        'concurrent.futures', 'reprlib')),
        PythonModule(min_version=(3, 8), max_version=(3, 8, 6), internal=True,
                deps=('asyncio', 'asyncio.format_helpers', 'reprlib')),
        PythonModule(min_version=(3, 8, 7), max_version=(3, 8), internal=True,
                deps=('asyncio', 'asyncio.format_helpers', 'reprlib',
                        '_thread')),
        PythonModule(version=(3, 9, 0), internal=True,
                deps=('asyncio', 'asyncio.format_helpers', 'reprlib')),
        PythonModule(min_version=(3, 9, 1), internal=True,
                deps=('asyncio', 'asyncio.format_helpers', 'reprlib',
                        '_thread'))),

    'asyncio.base_subprocess':
        PythonModule(internal=True,
                deps=('asyncio', 'asyncio.log', 'asyncio.protocols',
                        'asyncio.transports', 'collections', 'subprocess',
                        'warnings')),

    'asyncio.base_tasks': (
        PythonModule(max_version=(3, 10), internal=True,
                deps=('asyncio', 'asyncio.base_futures', 'asyncio.coroutines',
                        'linecache', 'traceback')),
        PythonModule(min_version=(3, 11), internal=True,
                deps=('asyncio', 'asyncio.base_futures', 'asyncio.coroutines',
                        'linecache', 'reprlib', 'traceback'))),

    'asyncio.constants':
        PythonModule(internal=True, deps=('asyncio', 'enum')),

    'asyncio.coroutines': (
        PythonModule(version=(3, 7), internal=True,
                deps=('asyncio', 'asyncio.base_futures', 'asyncio.constants',
                        'asyncio.format_helpers', 'asyncio.log',
                        'collections.abc', 'functools', 'inspect', 'os',
                        'traceback', 'types')),
        PythonModule(min_version=(3, 8), max_version=(3, 10), internal=True,
                deps=('asyncio', 'asyncio.base_futures', 'asyncio.constants',
                        'asyncio.format_helpers', 'asyncio.log',
                        'collections.abc', 'functools', 'inspect', 'os',
                        'traceback', 'types', 'warnings')),
        PythonModule(min_version=(3, 11), internal=True,
                deps=('asyncio', 'collections.abc', 'inspect', 'os',
                        'traceback', 'types'))),

    'asyncio.events': (
        PythonModule(version=(3, 7), internal=True,
                deps=('asyncio', 'asyncio.format_helpers', '_asyncio',
                        'contextvars', 'os', 'socket', 'subprocess',
                        'threading')),
        PythonModule(version=(3, 8), internal=True,
                deps=('asyncio', 'asyncio.exceptions',
                        'asyncio.format_helpers', '_asyncio', 'contextvars',
                        'os', 'socket', 'subprocess', 'threading')),
        PythonModule(version=(3, 9), internal=True,
                deps=('asyncio', 'asyncio.format_helpers', '_asyncio',
                        'contextvars', 'os', 'socket', 'subprocess',
                        'threading')),
        PythonModule(min_version=(3, 10), internal=True,
                deps=('asyncio', 'asyncio.format_helpers', '_asyncio',
                        'contextvars', 'os', 'socket', 'subprocess',
                        'threading', 'warnings'))),

    'asyncio.exceptions':
        PythonModule(min_version=(3, 8), internal=True, deps='asyncio'),

    'asyncio.format_helpers':
        PythonModule(internal=True,
                deps=('asyncio', 'asyncio.constants', 'functools', 'inspect',
                        'reprlib', 'traceback')),

    'asyncio.futures': (
        PythonModule(version=(3, 7), internal=True,
                deps=('asyncio', 'asyncio.base_futures', 'asyncio.events',
                        'asyncio.format_helpers', '_asyncio',
                        'concurrent.futures', 'contextvars', 'logging')),
        PythonModule(min_version=(3, 8), max_version=(3, 9, 10), internal=True,
                deps=('asyncio', 'asyncio.base_futures', 'asyncio.events',
                        'asyncio.exceptions', 'asyncio.format_helpers',
                        '_asyncio', 'concurrent.futures', 'contextvars',
                        'logging')),
        PythonModule(min_version=(3, 9, 11), max_version=(3, 9), internal=True,
                deps=('asyncio', 'asyncio.base_futures', 'asyncio.events',
                        'asyncio.exceptions', 'asyncio.format_helpers',
                        '_asyncio', 'concurrent.futures', 'contextvars',
                        'logging', 'types')),
        PythonModule(min_version=(3, 10), max_version=(3, 10, 2),
                internal=True,
                deps=('asyncio', 'asyncio.base_futures', 'asyncio.events',
                        'asyncio.exceptions', 'asyncio.format_helpers',
                        '_asyncio', 'concurrent.futures', 'contextvars',
                        'logging')),
        PythonModule(min_version=(3, 10, 3), internal=True,
                deps=('asyncio', 'asyncio.base_futures', 'asyncio.events',
                        'asyncio.exceptions', 'asyncio.format_helpers',
                        '_asyncio', 'concurrent.futures', 'contextvars',
                        'logging', 'types'))),

    'asyncio.locks': (
        PythonModule(version=(3, 7), internal=True,
                deps=('asyncio', 'asyncio.coroutines', 'asyncio.events',
                        'asyncio.futures', 'collections', 'warnings')),
        PythonModule(version=(3, 8), internal=True,
                deps=('asyncio', 'asyncio.coroutines', 'asyncio.events',
                        'asyncio.exceptions', 'asyncio.futures', 'collections',
                        'types', 'warnings')),
        PythonModule(version=(3, 9), internal=True,
                deps=('asyncio', 'asyncio.events', 'asyncio.exceptions',
                        'collections', 'warnings')),
        PythonModule(min_version=(3, 10), max_version=(3, 10, 3),
                internal=True,
                deps=('asyncio', 'asyncio.exceptions', 'asyncio.mixins',
                        'collections')),
        PythonModule(min_version=(3, 10, 4), max_version=(3, 10),
                internal=True,
                deps=('asyncio', 'asyncio.exceptions', 'asyncio.mixins',
                        'asyncio.tasks', 'collections')),
        PythonModule(min_version=(3, 11), internal=True,
                deps=('asyncio', 'asyncio.exceptions', 'asyncio.mixins',
                        'asyncio.tasks', 'collections', 'enum'))),

    'asyncio.log':
        PythonModule(internal=True, deps=('asyncio', 'logging')),

    'asyncio.mixins':
        PythonModule(min_version=(3, 10), internal=True,
                deps=('asyncio', 'asyncio.events', 'threading')),

    'asyncio.proactor_events': (
        PythonModule(version=(3, 7), internal=True,
                deps=('asyncio', 'asyncio.base_events', 'asyncio.constants',
                        'asyncio.events', 'asyncio.futures', 'asyncio.log',
                        'asyncio.protocols', 'asyncio.sslproto',
                        'asyncio.transports', 'io', 'os', 'socket',
                        'warnings')),
        PythonModule(min_version=(3, 8), internal=True,
                deps=('asyncio', 'asyncio.base_events', 'asyncio.constants',
                        'asyncio.exceptions', 'asyncio.futures', 'asyncio.log',
                        'asyncio.protocols', 'asyncio.sslproto',
                        'asyncio.transports', 'asyncio.trsock', 'collections',
                        'io', 'os', 'signal', 'socket', 'threading',
                        'warnings'))),

    'asyncio.protocols':
        PythonModule(internal=True, deps='asyncio'),

    'asyncio.queues': (
        PythonModule(version=(3, 7), internal=True,
                deps=('asyncio', 'asyncio.events', 'asyncio.locks',
                        'collections', 'heapq')),
        PythonModule(min_version=(3, 8), max_version=(3, 9, 10), internal=True,
                deps=('asyncio', 'asyncio.events', 'asyncio.locks',
                        'collections', 'heapq', 'warnings')),
        PythonModule(min_version=(3, 9, 11), max_version=(3, 9), internal=True,
                deps=('asyncio', 'asyncio.events', 'asyncio.locks',
                        'collections', 'heapq', 'types', 'warnings')),
        PythonModule(min_version=(3, 10), max_version=(3, 10, 2),
                internal=True,
                deps=('asyncio', 'asyncio.locks', 'asyncio.mixins',
                        'collections', 'heapq')),
        PythonModule(min_version=(3, 10, 3), internal=True,
                deps=('asyncio', 'asyncio.locks', 'asyncio.mixins',
                        'collections', 'heapq', 'types'))),

    'asyncio.runners': (
        PythonModule(max_version=(3, 10), internal=True,
                deps=('asyncio', 'asyncio.coroutines', 'asyncio.events',
                        'asyncio.tasks')),
        PythonModule(min_version=(3, 11), internal=True,
                deps=('asyncio', 'asyncio.coroutines', 'asyncio.events',
                        'asyncio.exceptions', 'asyncio.tasks', 'contextvars'
                        'enum', 'functools', 'threading', 'signal'))),

    'asyncio.selector_events': (
        PythonModule(version=(3, 7), internal=True,
                deps=('asyncio', 'asyncio.base_events', 'asyncio.constants',
                        'asyncio.events', 'asyncio.futures', 'asyncio.log',
                        'asyncio.protocols', 'asyncio.sslproto',
                        'asyncio.transports', 'collections', 'errno',
                        'functools', 'selectors', 'socket', '?ssl', 'warnings',
                        'weakref')),
        PythonModule(min_version=(3, 8), internal=True,
                deps=('asyncio', 'asyncio.base_events', 'asyncio.constants',
                        'asyncio.events', 'asyncio.futures', 'asyncio.log',
                        'asyncio.protocols', 'asyncio.sslproto',
                        'asyncio.transports', 'asyncio.trsock', 'collections',
                        'errno', 'functools', 'selectors', 'socket', '?ssl',
                        'warnings', 'weakref'))),

    'asyncio.sslproto': (
        PythonModule(max_version=(3, 8), internal=True,
                deps=('asyncio', 'asyncio.base_events', 'asyncio.constants',
                        'asyncio.log', 'asyncio.protocols',
                        'asyncio.transports', 'collections', '?ssl',
                        'warnings')),
        PythonModule(min_version=(3, 9), max_version=(3, 10), internal=True,
                deps=('asyncio', 'asyncio.constants', 'asyncio.log',
                        'asyncio.protocols', 'asyncio.transports',
                        'collections', '?ssl', 'warnings')),
        PythonModule(min_version=(3, 11), internal=True,
                deps=('asyncio', 'asyncio.constants', 'asyncio.exceptions',
                        'asyncio.log', 'asyncio.protocols',
                        'asyncio.transports', 'collections', 'enum', '?ssl',
                        'warnings'))),

    'asyncio.staggered': (
        PythonModule(min_version=(3, 8), max_version=(3, 8, 1),
                internal=True,
                deps=('asyncio', 'asyncio.events', 'asyncio.futures',
                        'asyncio.locks', 'asyncio.tasks', 'contextlib',
                        'typing')),
        PythonModule(min_version=(3, 8, 2), internal=True,
                deps=('asyncio', 'asyncio.events', 'asyncio.exceptions',
                        'asyncio.locks', 'asyncio.tasks', 'contextlib',
                        'typing'))),

    'asyncio.streams': (
        PythonModule(version=(3, 7), internal=True,
                deps=('asyncio', 'asyncio.coroutines', 'asyncio.events',
                        'asyncio.log', 'asyncio.protocols', 'asyncio.tasks',
                        'socket')),
        PythonModule(min_version=(3, 8), max_version=(3, 10, 7), internal=True,
                deps=('asyncio', 'asyncio.coroutines', 'asyncio.events',
                        'asyncio.exceptions', 'asyncio.format_helpers',
                        'asyncio.log', 'asyncio.protocols', 'asyncio.tasks',
                        'socket', 'warnings', 'weakref')),
        PythonModule(min_version=(3, 10, 8), internal=True,
                deps=('asyncio', 'asyncio.coroutines', 'asyncio.events',
                        'asyncio.exceptions', 'asyncio.format_helpers',
                        'asyncio.log', 'asyncio.protocols', 'asyncio.tasks',
                        'collections', 'socket', 'warnings', 'weakref'))),

    'asyncio.subprocess': (
        PythonModule(version=(3, 7), internal=True,
                deps=('asyncio', 'asyncio.events', 'asyncio.log',
                        'asyncio.protocols', 'asyncio.streams',
                        'asyncio.tasks', 'subprocess')),
        PythonModule(min_version=(3, 8), max_version=(3, 9), internal=True,
                deps=('asyncio', 'asyncio.events', 'asyncio.log',
                        'asyncio.protocols', 'asyncio.streams',
                        'asyncio.tasks', 'subprocess', 'warnings')),
        PythonModule(min_version=(3, 10), internal=True,
                deps=('asyncio', 'asyncio.events', 'asyncio.log',
                        'asyncio.protocols', 'asyncio.streams',
                        'asyncio.tasks', 'subprocess'))),

    'asyncio.taskgroups':
        PythonModule(min_version=(3, 11), internal=True,
                deps=('asyncio', 'asyncio.events', 'asyncio.exceptions',
                        'asyncio.tasks')),

    'asyncio.tasks': (
        PythonModule(version=(3, 7), internal=True,
                deps=('asyncio', 'asyncio.base_tasks', 'asyncio.coroutines',
                        'asyncio.events', 'asyncio.futures', 'asyncio.queues',
                        'asyncio.tasks', '_asyncio', 'concurrent.futures',
                        'contextvars', 'functools', 'inspect', 'types',
                        'warnings', 'weakref')),
        PythonModule(min_version=(3, 8), internal=True,
                deps=('asyncio', 'asyncio.base_tasks', 'asyncio.coroutines',
                        'asyncio.events', 'asyncio.exceptions',
                        'asyncio.futures', 'asyncio.queues', 'asyncio.tasks',
                        '_asyncio', 'concurrent.futures', 'contextvars',
                        'functools', 'inspect', 'itertools', 'types',
                        'warnings', 'weakref'))),

    'asyncio.threads':
        PythonModule(min_version=(3, 9), internal=True,
                deps=('asyncio', 'asyncio.events', 'contextvars',
                        'functools')),

    'asyncio.timeouts':
        PythonModule(min_version=(3, 11), internal=True,
                deps=('asyncio', 'asyncio.events', 'asyncio.exceptions',
                        'asyncio.tasks', 'enum', 'types', 'typing')),

    'asyncio.transports':
        PythonModule(internal=True, deps='asyncio'),

    'asyncio.trsock': (
        PythonModule(min_version=(3, 8), max_version=(3, 10), internal=True,
                deps=('asyncio', 'socket', 'warnings')),
        PythonModule(min_version=(3, 11), internal=True,
                deps=('asyncio', 'socket'))),

    'asyncio.unix_events': (
        PythonModule(version=(3, 7), target='!win', internal=True,
                deps=('asyncio', 'asyncio.base_events',
                        'asyncio.base_subprocess', 'asyncio.constants',
                        'asyncio.coroutines', 'asyncio.events',
                        'asyncio.futures', 'asyncio.log',
                        'asyncio.selector_events', 'asyncio.transports',
                        'errno', 'io', 'os', 'selectors', 'signal', 'socket',
                        'stat', 'subprocess', 'threading', 'warnings')),
        PythonModule(min_version=(3, 8), target='!win', internal=True,
                deps=('asyncio', 'asyncio.base_events',
                        'asyncio.base_subprocess', 'asyncio.constants',
                        'asyncio.coroutines', 'asyncio.events',
                        'asyncio.exceptions', 'asyncio.futures', 'asyncio.log',
                        'asyncio.selector_events', 'asyncio.transports',
                        'errno', 'io', 'itertools', 'os', 'selectors',
                        'signal', 'socket', 'stat', 'subprocess', 'threading',
                        'warnings'))),

    'asyncio.windows_events': (
        PythonModule(max_version=(3, 7, 2), target='win',
                internal=True,
                deps=('asyncio', 'asyncio.events', 'asyncio.base_subprocess',
                        'asyncio.futures', 'asyncio.log',
                        'asyncio.proactor_events', 'asyncio.selector_events',
                        'asyncio.tasks', 'asyncio.windows_utils', 'errno',
                        'math', 'msvcrt', '_overlapped', 'socket', 'struct',
                        'weakref', '_winapi')),
        PythonModule(min_version=(3, 7, 3), max_version=(3, 7), target='win',
                internal=True,
                deps=('asyncio', 'asyncio.events', 'asyncio.base_subprocess',
                        'asyncio.futures', 'asyncio.log',
                        'asyncio.proactor_events', 'asyncio.selector_events',
                        'asyncio.tasks', 'asyncio.windows_utils', 'errno',
                        'math', 'msvcrt', '_overlapped', 'socket', 'struct',
                        'time', 'weakref', '_winapi')),
        PythonModule(min_version=(3, 8), target='win', internal=True,
                deps=('asyncio', 'asyncio.events', 'asyncio.base_subprocess',
                        'asyncio.exceptions', 'asyncio.futures', 'asyncio.log',
                        'asyncio.proactor_events', 'asyncio.selector_events',
                        'asyncio.tasks', 'asyncio.windows_utils', 'errno',
                        'math', 'msvcrt', '_overlapped', 'socket', 'struct',
                        'time', 'weakref', '_winapi'))),

    'asyncio.windows_utils':
        PythonModule(target='win', internal=True,
                deps=('asyncio', 'itertools', 'msvcrt', 'os', 'subprocess',
                        'tempfile', 'warnings', '_winapi')),

    '_bisect':
        ExtensionModule(internal=True, source='_bisectmodule.c'),

    '_blake2':
        # Note that we don't enable BLAKE2_USE_SSE because we don't have a way
        # of detecting and specifying x86_64 (although it wouldn't be too
        # difficult to do).
        ExtensionModule(internal=True,
                source=('_blake2/blake2module.c', '_blake2/blake2b_impl.c',
                        '_blake2/blake2s_impl.c'),
                includepath='_blake2'),

    '_bootlocale':
        PythonModule(max_version=(3, 9), internal=True, deps='_locale'),

    '_bz2':
        ExtensionModule(internal=True, source='_bz2module.c',
                deps='bzip2:bzip2', pyd='_bz2.pyd'),

    '_codecs':
        CoreExtensionModule(internal=True),

    '_codecs_cn':
        ExtensionModule(internal=True, source='cjkcodecs/_codecs_cn.c'),

    '_codecs_hk':
        ExtensionModule(internal=True, source='cjkcodecs/_codecs_hk.c'),

    '_codecs_iso2022':
        ExtensionModule(internal=True, source='cjkcodecs/_codecs_iso2022.c'),

    '_codecs_jp':
        ExtensionModule(internal=True, source='cjkcodecs/_codecs_jp.c'),

    '_codecs_kr':
        ExtensionModule(internal=True, source='cjkcodecs/_codecs_kr.c'),

    '_codecs_tw':
        ExtensionModule(internal=True, source='cjkcodecs/_codecs_tw.c'),

    '_collections':
        CoreExtensionModule(internal=True),

    '_collections_abc':
        PythonModule(internal=True, deps='abc'),

    '_compat_pickle':
        PythonModule(internal=True),

    '_compression':
        PythonModule(internal=True, deps='io'),

    'concurrent.futures._base': (
        PythonModule(max_version=(3, 8), internal=True,
                deps=('concurrent.futures', 'collections', 'logging',
                        'threading', 'time')),
        PythonModule(min_version=(3, 9), internal=True,
                deps=('concurrent.futures', 'collections', 'logging',
                        'threading', 'time', 'types'))),

    'concurrent.futures.process': (
        PythonModule(max_version=(3, 8), internal=True,
                deps=('concurrent.futures', 'atexit',
                        'concurrent.futures._base', 'functools', 'itertools',
                        'multiprocessing', 'multiprocessing.connection',
                        'multiprocessing.queues', 'os', 'queue', 'threading',
                        'traceback', 'weakref')),
        PythonModule(min_version=(3, 9), internal=True,
                deps=('concurrent.futures', 'concurrent.futures._base',
                        'functools', 'itertools', 'multiprocessing',
                        'multiprocessing.connection', 'multiprocessing.queues',
                        'os', 'threading', 'traceback', 'weakref'))),

    'concurrent.futures.thread': (
        PythonModule(max_version=(3, 8), internal=True,
                deps=('concurrent.futures', 'atexit',
                        'concurrent.futures._base', 'itertools', 'os', 'queue',
                        'threading', 'weakref')),
        PythonModule(min_version=(3, 9), internal=True,
                deps=('concurrent.futures', 'concurrent.futures._base',
                        'itertools', 'os', 'queue', 'threading', 'types',
                        'weakref'))),

    '_contextvars':
        ExtensionModule(internal=True, source='_contextvarsmodule.c'),

    '_crypt':
        ExtensionModule(target='!win', internal=True, source='_cryptmodule.c'),

    '_csv':
        ExtensionModule(internal=True, source='_csv.c'),

    '_ctypes': (
        ExtensionModule(max_version=(3, 7), target='linux|macos|win',
                internal=True,
                source=('_ctypes/_ctypes.c', '_ctypes/callbacks.c',
                        '_ctypes/callproc.c', '_ctypes/stgdict.c',
                        '_ctypes/cfield.c',
                        'macos#_ctypes/malloc_closure.c',
                        'macos#_ctypes/darwin/dlfcn_simple.c',
                        'macos#_ctypes/libffi_osx/ffi.c',
                        'macos#_ctypes/libffi_osx/x86/darwin64.S',
                        'macos#_ctypes/libffi_osx/x86/x86-darwin.S',
                        'macos#_ctypes/libffi_osx/x86/x86-ffi_darwin.c',
                        'macos#_ctypes/libffi_osx/x86/x86-ffi64.c',
                        'win#_ctypes/malloc_closure.c',
                        'win#_ctypes/libffi_msvc/prep_cif.c',
                        'win#_ctypes/libffi_msvc/ffi.c',
                        'win-32#_ctypes/libffi_msvc/win32.c',
                        'win-64#_ctypes/libffi_msvc/win64.asm'),
                defines='macos#MACOSX',
                includepath=('_ctypes',
                        'macos#_ctypes/darwin',
                        'macos#_ctypes/libffi_osx/include',
                        'win#_ctypes/libffi_msvc'),
                libs='linux#-lffi',
                pyd='_ctypes.pyd'),
        ExtensionModule(min_version=(3, 8), max_version=(3, 8, 9),
                target='linux|macos|win', internal=True,
                deps='libffi:linux|win#libffi',
                source=('_ctypes/_ctypes.c', '_ctypes/callbacks.c',
                        '_ctypes/callproc.c', '_ctypes/stgdict.c',
                        '_ctypes/cfield.c',
                        'macos#_ctypes/malloc_closure.c',
                        'macos#_ctypes/darwin/dlfcn_simple.c',
                        'macos#_ctypes/libffi_osx/ffi.c',
                        'macos#_ctypes/libffi_osx/x86/darwin64.S',
                        'macos#_ctypes/libffi_osx/x86/x86-darwin.S',
                        'macos#_ctypes/libffi_osx/x86/x86-ffi_darwin.c',
                        'macos#_ctypes/libffi_osx/x86/x86-ffi64.c',
                        'win#_ctypes/malloc_closure.c'),
                defines=('macos#MACOSX',
                         'win#FFI_BUILDING'),
                includepath=('_ctypes',
                        'macos#_ctypes/darwin',
                        'macos#_ctypes/libffi_osx/include'),
                pyd='_ctypes.pyd', dlls='libffi-7.dll'),
        ExtensionModule(min_version=(3, 8, 10), max_version=(3, 8),
                target='linux|macos|win', internal=True,
                deps='libffi:libffi',
                source=('_ctypes/_ctypes.c', '_ctypes/callbacks.c',
                        '_ctypes/callproc.c', '_ctypes/stgdict.c',
                        '_ctypes/cfield.c',
                        'macos#_ctypes/malloc_closure.c',
                        'win#_ctypes/malloc_closure.c'),
                defines=(
                        'linux|macos#HAVE_FFI_PREP_CIF_VAR=1',
                        'linux|macos#HAVE_FFI_PREP_CLOSURE_LOC=1',
                        'linux|macos#HAVE_FFI_CLOSURE_ALLOC=1',
                        'macos#MACOSX',
                        'macos#USING_APPLE_OS_LIBFFI=1',
                        'macos#USING_MALLOC_CLOSURE_DOT_C=1',
                        'win#FFI_BUILDING'),
                includepath=('_ctypes',
                        'macos#_ctypes/darwin'),
                pyd='_ctypes.pyd', dlls='libffi-7.dll'),
        ExtensionModule(min_version=(3, 9), target='linux|macos|win',
                internal=True,
                deps='libffi:libffi',
                source=('_ctypes/_ctypes.c', '_ctypes/callbacks.c',
                        '_ctypes/callproc.c', '_ctypes/stgdict.c',
                        '_ctypes/cfield.c',
                        'macos#_ctypes/malloc_closure.c',
                        'win#_ctypes/malloc_closure.c'),
                defines=('Py_BUILD_CORE_MODULE',
                        'linux|macos#HAVE_FFI_PREP_CIF_VAR=1',
                        'linux|macos#HAVE_FFI_PREP_CLOSURE_LOC=1',
                        'linux|macos#HAVE_FFI_CLOSURE_ALLOC=1',
                        'macos#MACOSX',
                        'macos#USING_APPLE_OS_LIBFFI=1',
                        'macos#USING_MALLOC_CLOSURE_DOT_C=1',
                        'win#FFI_BUILDING'),
                includepath=('_ctypes',
                        'macos#_ctypes/darwin'),
                pyd='_ctypes.pyd', dlls='libffi-7.dll')),

    'ctypes._endian':
        PythonModule(target='linux|macos|win', internal=True, deps='ctypes'),

    'ctypes.macholib':
        PythonModule(target='macos', internal=True, deps='ctypes'),

    'ctypes.macholib.dyld':
        PythonModule(target='macos', internal=True,
                deps=('ctypes.macholib', 'ctypes.macholib.dylib',
                        'ctypes.macholib.framework', 'itertools', 'os')),

    'ctypes.macholib.dylib':
        PythonModule(target='macos', internal=True,
                deps=('ctypes.macholib', 're')),

    'ctypes.macholib.framework':
        PythonModule(target='macos', internal=True,
                deps=('ctypes.macholib', 're')),

    'curses.has_key':
        PythonModule(target='!win', internal=True, deps=('curses', '_curses')),

    '_curses': (
        ExtensionModule(max_version=(3, 9), target='!win', internal=True,
                source='_cursesmodule.c', deps='curses:curses'),
        ExtensionModule(min_version=(3, 10), target='!win', internal=True,
                source='_cursesmodule.c', defines='Py_BUILD_CORE_MODULE',
                deps='curses:curses')),

    '_curses_panel':
        ExtensionModule(target='!win', internal=True,
                source='_curses_panel.c', deps='curses:panel'),

    '_datetime': (
        ExtensionModule(max_version=(3, 9), internal=True,
                source='_datetimemodule.c', libs='linux#-lm'),
        ExtensionModule(min_version=(3, 10), internal=True,
                source='_datetimemodule.c', defines='Py_BUILD_CORE_MODULE',
                libs='linux#-lm')),

    '_dbm':
        ExtensionModule(internal=True, source='_dbmmodule.c',
                defines='HAVE_NDBM_H', deps='ndbm:ndbm'),

    'distutils.config': (
        PythonModule(max_version=(3, 10),
                deps=('cgi', 'configparser', 'distutils.cmd', 'os')),
        PythonModule(min_version=(3, 11),
                deps=('cgi', 'configparser', 'distutils.cmd', 'os',
                        'warnings'))),

    '_distutils_findvs':
        ExtensionModule(max_version=(3, 7, 1), target='win', internal=True,
                source='../PC/_findvs.cpp', pyd='_distutils_findvs.pyd'),

    'distutils.msvc9compiler':
        PythonModule(target='win',
                deps=('distutils.ccompiler', 'distutils.errors',
                        'distutils.log', 'distutils.util', 'os', 're',
                        'subprocess', 'winreg')),

    'distutils._msvccompiler': (
        PythonModule(max_version=(3, 7, 1), target='win',
                deps=('distutils.ccompiler', 'distutils.errors',
                        '_distutils_findvs', 'distutils.log', 'distutils.util',
                        'glob', 'itertools', 'os', 'shutil', 'stat',
                        'subprocess', 'threading', 'winreg')),
        PythonModule(min_version=(3, 7, 2), max_version=(3, 7, 6),
                target='win',
                deps=('distutils.ccompiler', 'distutils.errors',
                        'distutils.log', 'distutils.util', 'glob', 'itertools',
                        'json', 'os', 'shutil', 'stat', 'subprocess',
                        'winreg')),
        PythonModule(min_version=(3, 7, 7), max_version=(3, 7), target='win',
                deps=('distutils.ccompiler', 'distutils.errors',
                        'distutils.log', 'distutils.util', 'itertools', 'json',
                        'os', 'shutil', 'stat', 'subprocess', 'winreg')),
        PythonModule(min_version=(3, 8), max_version=(3, 8, 2), target='win',
                deps=('distutils.ccompiler', 'distutils.errors',
                        'distutils.log', 'distutils.util', 'glob', 'itertools',
                        'json', 'os', 'shutil', 'stat', 'subprocess',
                        'winreg')),
        PythonModule(min_version=(3, 8, 3), max_version=(3, 8), target='win',
                deps=('distutils.ccompiler', 'distutils.errors',
                        'distutils.log', 'distutils.util', 'itertools', 'json',
                        'os', 'shutil', 'stat', 'subprocess', 'winreg')),
        PythonModule(min_version=(3, 9), target='win',
                deps=('distutils.ccompiler', 'distutils.errors',
                        'distutils.log', 'distutils.util', 'itertools', 'os',
                        'subprocess', 'winreg'))),

    'distutils.versionpredicate':
        PythonModule(
                deps=('distutils.version', 'operator', 're')),

    '_elementtree':
        ExtensionModule(internal=True, source='_elementtree.c',
                defines=('win#COMPILED_FROM_DSP',
                        '!win#HAVE_EXPAT_CONFIG_H',
                        'USE_PYEXPAT_CAPI', 'XML_POOR_ENTROPY'),
                deps=('copy', 'pyexpat', 'xml.etree.ElementPath'),
                pyd='_elementtree.pyd'),

    'email.base64mime':
        PythonModule(internal=True, deps=('email', 'base64', 'binascii')),

    'email._encoded_words':
        PythonModule(internal=True,
                deps=('email', 'base64', 'binascii', 'email.errors',
                        'functools', 're', 'string')),

    'email.feedparser':
        PythonModule(internal=True,
                deps=('email', 'collections', 'email.errors', 'email.message',
                        'email._policybase', 'io', 're')),

    'email._header_value_parser': (
        PythonModule(version=(3, 7), internal=True,
                deps=('email', 'collections', 'email._encoded_words',
                        'email.errors', 'email.utils', 'operator', 're',
                        'string', 'urllib')),
        PythonModule(min_version=(3, 8), internal=True,
                deps=('email', 'email._encoded_words', 'email.errors',
                        'email.utils', 'operator', 're', 'string', 'urllib'))),

    'email._parseaddr':
        PythonModule(internal=True, deps=('email', 'calendar', 'time')),

    'email._policybase':
        PythonModule(internal=True,
                deps=('email', 'abc', 'email.charset', 'email.header',
                        'email.utils')),

    'email.quoprimime':
        PythonModule(internal=True, deps=('email', 're', 'string')),

    'encodings.aliases':
        CorePythonModule(internal=True, deps='encodings'),

    '_functools':
        CoreExtensionModule(internal=True),

    '_gdbm':
        ExtensionModule(internal=True, source='_gdbmmodule.c',
                deps='gdbm:gdbm'),

    'genericpath':
        PythonModule(internal=True, deps=('os', 'stat')),

    '_hashlib':
        ExtensionModule(internal=True, source='_hashopenssl.c',
                deps='OpenSSL:openssl', pyd='_hashlib.pyd'),

    '_heapq': (
        ExtensionModule(max_version=(3, 9), internal=True,
                source='_heapqmodule.c'),
        ExtensionModule(min_version=(3, 10), internal=True,
                source='_heapqmodule.c', defines='Py_BUILD_CORE_MODULE')),

    '_imp':
        CoreExtensionModule(internal=True),

    'importlib._abc':
        PythonModule(min_version=(3, 10), internal=True,
                deps=('importlib', 'abc', 'importlib._bootstrap', 'warnings')),

    'importlib._adapters':
        PythonModule(version=(3, 10), internal=True,
                deps=('importlib', 'importlib.abc', 'contextlib')),

    'importlib._bootstrap':
        CorePythonModule(internal=True, builtin=True, deps='importlib'),

    'importlib._bootstrap_external': (
        CorePythonModule(version=(3, 7), internal=True, builtin=True,
                deps='importlib'),
        CorePythonModule(min_version=(3, 8), max_version=(3, 8, 9),
                internal=True, builtin=True,
                deps=('importlib', 'importlib.metadata')),
        CorePythonModule(min_version=(3, 8, 10), max_version=(3, 9),
                internal=True, builtin=True,
                deps=('_imp', 'importlib', 'importlib.metadata', '_io',
                        'marshal', 'win#nt', '!win#posix', '_warnings',
                        'win#winreg')),
        CorePythonModule(min_version=(3, 10), internal=True, builtin=True,
                deps=('_imp', 'importlib', 'importlib.metadata',
                        'importlib.readers', '_io', 'marshal', 'win#nt',
                        '!win#posix', '_warnings', 'win#winreg'))),

    'importlib._common': (
        PythonModule(version=(3, 9), internal=True,
                deps=('importlib', 'contextlib', 'functools', 'os', 'pathlib',
                        'tempfile', 'zipfile')),
        PythonModule(version=(3, 10), internal=True,
                deps=('importlib', 'contextlib', 'functools', 'importlib.abc',
                        'importlib._adapters', 'os', 'pathlib', 'tempfile',
                        'types', 'typing'))),

    'importlib.metadata._adapters':
        PythonModule(min_version=(3, 10), internal=True,
                deps=('email', 'importlib.metadata._text', 're', 'textwrap')),

    'importlib.metadata._collections':
        PythonModule(min_version=(3, 10), internal=True, deps='collections'),

    'importlib.metadata._functools':
        PythonModule(min_version=(3, 10), internal=True,
                deps=('functools', 'types')),

    'importlib.metadata._itertools':
        PythonModule(min_version=(3, 10), internal=True, deps='itertools'),

    'importlib.metadata._meta':
        PythonModule(min_version=(3, 10), internal=True, deps='typing'),

    'importlib.metadata._text':
        PythonModule(min_version=(3, 10), internal=True,
                deps=('importlib.metadata._functools', 're')),

    'importlib.readers': (
        PythonModule(version=(3, 10), internal=True,
                deps=('collections', 'importlib.abc', 'pathlib', 'zipfile')),
        PythonModule(min_version=(3, 11), internal=True,
                deps='importlib.resources.readers')),

    'importlib.resources._adapters':
        PythonModule(min_version=(3, 11), internal=True,
                deps=('contextlib', 'importlib.resources.abc', 'io')),

    'importlib.resources._common':
        PythonModule(min_version=(3, 11), internal=True,
                deps=('contextlib', 'functools', 'importlib',
                'importlib.resources._adapters', 'importlib.resources.abc',
                'os', 'pathlib', 'tempfile', 'types', 'typing')),

    'importlib.resources._itertools':
        PythonModule(min_version=(3, 11), internal=True,
                deps=('itertools', 'typing')),

    'importlib.resources._legacy':
        PythonModule(min_version=(3, 11), internal=True,
                deps=('functools', 'importlib.resources._common', 'os',
                        'pathlib', 'types', 'typing', 'warnings')),

    'importlib.resources.readers':
        PythonModule(min_version=(3, 11), internal=True,
                deps=('collections', 'importlib.resources._itertools',
                        'importlib.resources.abc', 'operator', 'pathlib',
                        'zipfile')),

    '_io': (
        CoreExtensionModule(max_version=(3, 9), internal=True,
                deps='_bootlocale'),
        CoreExtensionModule(min_version=(3, 10), internal=True)),

    '_json': (
        ExtensionModule(max_version=(3, 8), internal=True, source='_json.c'),
        ExtensionModule(min_version=(3, 9), internal=True, source='_json.c',
                defines='Py_BUILD_CORE_MODULE')),

    'json.decoder':
        PythonModule(internal=True,
                deps=('json', 'json.scanner', '_json', 're')),

    'json.encoder':
        PythonModule(internal=True, deps=('json', '_json', 're')),

    'json.scanner':
        PythonModule(internal=True, deps=('_json', 're')),

    '_locale':
        CoreExtensionModule(internal=True),

    '_lsprof':
        ExtensionModule(internal=True, source=('_lsprof.c', 'rotatingtree.c')),

    '_lzma':
        ExtensionModule(internal=True, source='_lzmamodule.c',
                deps='LZMA:lzma', pyd='_lzma.pyd'),

    '_markupbase':
        PythonModule(internal=True, deps='re'),

    '_md5': (
        ExtensionModule(internal=True, source='md5module.c')),

    '_msi':
        ExtensionModule(target='win', internal=True, source='../PC/_msi.c',
                libs=('-lfci', '-lmsi', '-lrpcrt4'), pyd='_msi.pyd'),

    '_multibytecodec':
        ExtensionModule(internal=True, source='cjkcodecs/multibytecodec.c'),

    '_multiprocessing':
        ExtensionModule(internal=True,
                source=('_multiprocessing/multiprocessing.c',
                        '_multiprocessing/semaphore.c'),
                includepath='_multiprocessing',
                pyd='_multiprocessing.pyd'),

    'multiprocessing.context':
        PythonModule(internal=True,
                deps=('multiprocessing', 'multiprocessing.connection',
                        '!win#multiprocessing.forkserver',
                        'multiprocessing.managers', 'multiprocessing.pool',
                        '!win#multiprocessing.popen_fork',
                        '!win#multiprocessing.popen_forkserver',
                        '!win#multiprocessing.popen_spawn_posix',
                        'win#multiprocessing.popen_spawn_win32',
                        'multiprocessing.process', 'multiprocessing.queues',
                        'multiprocessing.reduction',
                        'multiprocessing.sharedctypes',
                        'multiprocessing.spawn', 'multiprocessing.synchronize',
                        'multiprocessing.util', 'os', 'threading')),

    'multiprocessing.dummy.connection':
        PythonModule(internal=True, deps=('multiprocessing.dummy', 'queue')),

    'multiprocessing.forkserver': (
        PythonModule(version=(3, 7), target='!win', internal=True,
                deps=('multiprocessing', 'errno', 'multiprocessing.connection',
                        'multiprocessing.context', 'multiprocessing.process',
                        'multiprocessing.semaphore_tracker',
                        'multiprocessing.spawn', 'multiprocessing.util', 'os',
                        'selectors', 'signal', 'socket', 'struct',
                        'threading', 'warnings')),
        PythonModule(min_version=(3, 8), target='!win', internal=True,
                deps=('multiprocessing', 'errno', 'multiprocessing.connection',
                        'multiprocessing.context', 'multiprocessing.process',
                        'multiprocessing.resource_tracker',
                        'multiprocessing.spawn', 'multiprocessing.util', 'os',
                        'selectors', 'signal', 'socket', 'struct',
                        'threading', 'warnings'))),

    'multiprocessing.heap': (
        PythonModule(version=(3, 7), internal=True,
                deps=('multiprocessing', 'bisect', 'multiprocessing.context',
                        'multiprocessing.util', 'mmap', 'tempfile', 'os',
                        'threading', 'win#_winapi')),
        PythonModule(min_version=(3, 8), internal=True,
                deps=('multiprocessing', 'bisect', 'collections',
                        'multiprocessing.context', 'multiprocessing.util',
                        'mmap', 'tempfile', 'os', 'threading',
                        'win#_winapi'))),

    'multiprocessing.popen_fork':
        PythonModule(target='!win', internal=True,
                deps=('multiprocessing', 'multiprocessing.connection',
                        'multiprocessing.util', 'os', 'signal')),

    'multiprocessing.popen_forkserver':
        PythonModule(target='!win', internal=True,
                deps=('multiprocessing', 'io', 'multiprocessing.connection',
                        'multiprocessing.context',
                        'multiprocessing.forkserver',
                        'multiprocessing.popen_fork', 'multiprocessing.spawn',
                        'multiprocessing.util', 'os')),

    'multiprocessing.popen_spawn_posix': (
        PythonModule(version=(3, 7), target='!win', internal=True,
                deps=('multiprocessing', 'io', 'multiprocessing.context',
                        'multiprocessing.popen_fork',
                        'multiprocessing.semaphore_tracker',
                        'multiprocessing.spawn', 'multiprocessing.util',
                        'os')),
        PythonModule(min_version=(3, 8), target='!win', internal=True,
                deps=('multiprocessing', 'io', 'multiprocessing.context',
                        'multiprocessing.popen_fork',
                        'multiprocessing.resource_tracker',
                        'multiprocessing.spawn', 'multiprocessing.util',
                        'os'))),

    'multiprocessing.popen_spawn_win32':
        PythonModule(target='win', internal=True,
                deps=('multiprocessing', 'msvcrt', 'multiprocessing.context',
                        'multiprocessing.spawn', 'multiprocessing.util', 'os',
                        'signal', '_winapi')),

    'multiprocessing.process': (
        PythonModule(version=(3, 7), internal=True,
                deps=('multiprocessing', 'itertools',
                        'multiprocessing.context', 'multiprocessing.util',
                        'os', 'signal', 'threading', 'traceback',
                        '_weakrefset')),
        PythonModule(min_version=(3, 8), internal=True,
                deps=('multiprocessing', 'itertools',
                        'multiprocessing.connection',
                        'multiprocessing.context', 'multiprocessing.util',
                        'os', 'signal', 'threading', 'traceback',
                        '_weakrefset'))),

    'multiprocessing.queues': (
        PythonModule(max_version=(3, 8), internal=True,
                deps=('multiprocessing', 'collections', 'errno',
                        '_multiprocessing', 'multiprocessing.connection',
                        'multiprocessing.context',
                        'multiprocessing.synchronize', 'multiprocessing.util',
                        'os', 'queue', 'threading', 'time', 'traceback',
                        'weakref')),
        PythonModule(min_version=(3, 9), internal=True,
                deps=('multiprocessing', 'collections', 'errno',
                        '_multiprocessing', 'multiprocessing.connection',
                        'multiprocessing.context',
                        'multiprocessing.synchronize', 'multiprocessing.util',
                        'os', 'queue', 'threading', 'time', 'traceback',
                        'types', 'weakref'))),

    'multiprocessing.reduction':
        PythonModule(internal=True,
                deps=('multiprocessing', 'abc', 'array', 'copyreg',
                        'functools', 'io', 'multiprocessing.context',
                        'multiprocessing.resource_sharer', 'os', 'pickle',
                        'socket', 'win#_winapi')),

    'multiprocessing.resource_sharer':
        PythonModule(internal=True,
                deps=('multiprocessing', 'multiprocessing.connection',
                        'multiprocessing.context', 'multiprocessing.process',
                        'multiprocessing.util', 'os', 'signal', 'socket',
                        'threading')),

    'multiprocessing.resource_tracker':
        PythonModule(min_version=(3, 8), internal=True,
                deps=('multiprocessing', '!win#_multiprocessing',
                        '!win#_posixshmem', 'multiprocessing.spawn',
                        'multiprocessing.util', 'os', 'signal', 'threading',
                        'warnings')),

    'multiprocessing.semaphore_tracker':
        PythonModule(version=(3, 7), target='!win', internal=True,
                deps=('multiprocessing', '_multiprocessing',
                        'multiprocessing.spawn', 'multiprocessing.util', 'os',
                        'signal', 'threading', 'warnings')),

    'multiprocessing.spawn': (
        PythonModule(version=(3, 7), internal=True,
                deps=('multiprocessing', 'win#msvcrt',
                        'multiprocessing.context', 'multiprocessing.process',
                        'multiprocessing.util', 'os', 'runpy', 'types')),
        PythonModule(min_version=(3, 8), internal=True,
                deps=('multiprocessing', 'win#_winapi', 'win#msvcrt',
                        'multiprocessing.context', 'multiprocessing.process',
                        '!win#multiprocessing.resource_tracker',
                        'multiprocessing.util', 'os', 'runpy', 'types'))),

    'multiprocessing.synchronize': (
        PythonModule(version=(3, 7), internal=True,
                deps=('multiprocessing', '_multiprocessing',
                        'multiprocessing.context', 'multiprocessing.heap',
                        'multiprocessing.process',
                        '!win#multiprocessing.semaphore_tracker',
                        'multiprocessing.util', 'struct', 'threading', 'time',
                        'tempfile')),
        PythonModule(min_version=(3, 8), internal=True,
                deps=('multiprocessing', '_multiprocessing',
                        'multiprocessing.context', 'multiprocessing.heap',
                        'multiprocessing.process',
                        '!win#multiprocessing.resource_tracker',
                        'multiprocessing.util', 'struct', 'threading', 'time',
                        'tempfile'))),

    'multiprocessing.util':
        PythonModule(internal=True,
                deps=('multiprocessing', 'atexit', 'itertools', 'logging',
                        'multiprocessing.process', 'os',
                        '!win#_posixsubprocess', 'shutil', 'subprocess',
                        'tempfile', 'threading', 'traceback', 'weakref')),

    'nt':
        CoreExtensionModule(target='win', internal=True),

    'ntpath': (
        PythonModule(max_version=(3, 10, 5), internal=True,
                deps=('genericpath', 'win#nt', 'os', 'stat', 'string')),
        PythonModule(min_version=(3, 10, 6), internal=True,
                deps=('genericpath', 'win#nt', 'os', 'stat', 'string',
                        'win#_winapi'))),

    'nturl2path':
        PythonModule(target='win', internal=True,
                deps=('string', 'urllib.parse')),

    'opcode':
        PythonModule(internal=True, deps='_opcode'),

    '_opcode':
        ExtensionModule(internal=True, source='_opcode.c'),

    '_operator':
        CoreExtensionModule(internal=True),

    '_overlapped':
        ExtensionModule(target='win', internal=True, source='overlapped.c',
                pyd='_overlapped.pyd'),

    '_osx_support':
        PythonModule(target='ios|macos', internal=True,
                deps=('contextlib', 'os', 're')),

    '_pickle': (
        ExtensionModule(max_version=(3, 7), internal=True, source='_pickle.c'),
        ExtensionModule(min_version=(3, 8), internal=True, source='_pickle.c',
                defines='Py_BUILD_CORE_MODULE')),

    'posixpath':
        PythonModule(internal=True,
                deps=('genericpath', 'os', '!win#pwd', 're', 'stat',
                        'warnings')),

    '_posixshmem':
        ExtensionModule(min_version=(3, 8), target='!win', internal=True,
                source='_multiprocessing/posixshmem.c', libs='linux#-lrt'),

    '_posixsubprocess': (
        ExtensionModule(max_version=(3, 9), target='!win', internal=True,
                source='_posixsubprocess.c'),
        ExtensionModule(min_version=(3, 10), target='!win', internal=True,
                source='_posixsubprocess.c', defines='Py_BUILD_CORE_MODULE')),

    '_pydecimal':
        PythonModule(internal=True,
                deps=('collections', 'contextvars', 'itertools', 'locale',
                        'math', 'numbers', 're')),

    'pyexpat': (
        ExtensionModule(max_version=(3, 7, 4), internal=True,
                source=('expat/loadlibrary.c', 'expat/xmlparse.c',
                        'expat/xmlrole.c', 'expat/xmltok.c', 'pyexpat.c'),
                defines=('XML_STATIC', 'win#COMPILED_FROM_DSP',
                        '!win#HAVE_EXPAT_CONFIG_H', '!win#XML_DEV_URANDOM'),
                includepath='expat',
                pyd='pyexpat.pyd'),
        ExtensionModule(min_version=(3, 7, 5), internal=True,
                source=('expat/xmlparse.c', 'expat/xmlrole.c',
                        'expat/xmltok.c', 'pyexpat.c'),
                defines=('XML_STATIC', '!win#HAVE_EXPAT_CONFIG_H',
                        '!win#XML_DEV_URANDOM'),
                includepath='expat',
                libs='linux#-lm',
                pyd='pyexpat.pyd')),

    '_queue': (
        ExtensionModule(max_version=(3, 9), internal=True,
                source='_queuemodule.c', pyd='_queue.pyd'),
        ExtensionModule(min_version=(3, 10), internal=True,
                source='_queuemodule.c', defines='Py_BUILD_CORE_MODULE',
                pyd='_queue.pyd')),

    '_random': (
        ExtensionModule(max_version=(3, 8), internal=True,
                source='_randommodule.c'),
        ExtensionModule(min_version=(3, 9), internal=True,
                source='_randommodule.c', defines='Py_BUILD_CORE_MODULE')),

    're._casefix':
        PythonModule(min_version=(3, 11), internal=True),

    're._compiler':
        PythonModule(min_version=(3, 11), internal=True,
                deps=('re._casefix', 're._constants', 're._parser', '_sre')),

    're._constants':
        PythonModule(min_version=(3, 11), internal=True, deps='_sre'),

    're._parser':
        PythonModule(min_version=(3, 11), internal=True,
                deps=('re._constants', 'unicodedata', 'warnings')),

    '_scproxy':
        ExtensionModule(target='macos', internal=True, source='_scproxy.c'),

    '_sha1':
        ExtensionModule(internal=True, source='sha1module.c'),

    '_sha3':
        ExtensionModule(internal=True,
                includepath='_sha3', source='_sha3/sha3module.c'),

    '_sha256': (
        ExtensionModule(max_version=(3, 8), internal=True,
                source='sha256module.c'),
        ExtensionModule(min_version=(3, 9), internal=True,
                source='sha256module.c', defines='Py_BUILD_CORE_MODULE')),

    '_sha512': (
        ExtensionModule(max_version=(3, 8), internal=True,
                source='sha512module.c'),
        ExtensionModule(min_version=(3, 9), internal=True,
                source='sha512module.c', defines='Py_BUILD_CORE_MODULE')),

    '_signal':
        CoreExtensionModule(internal=True),

    '_socket': (
        ExtensionModule(max_version=(3, 8), internal=True,
                source='socketmodule.c', pyd='_socket.pyd'),
        ExtensionModule(min_version=(3, 9), internal=True,
                source='socketmodule.c',
                defines='ios|macos#__APPLE_USE_RFC_3542',
                libs='win#-liphlpapi', pyd='_socket.pyd')),

    '_sqlite3':
        ExtensionModule(internal=True,
                source=('_sqlite/cache.c', '_sqlite/connection.c',
                        '_sqlite/cursor.c', '_sqlite/microprotocols.c',
                        '_sqlite/module.c', '_sqlite/prepare_protocol.c',
                        '_sqlite/row.c', '_sqlite/statement.c',
                        '_sqlite/util.c'),
                defines=('MODULE_NAME=\\\\\\"sqlite3\\\\\\"',
                        'SQLITE_OMIT_LOAD_EXTENSION'),
                includepath='_sqlite', deps='SQLite:sqlite3',
                pyd='_sqlite3.pyd', dlls='sqlite3.dll'),

    'sqlite3.dbapi2':
        PythonModule(internal=True,
                deps=('sqlite3', 'collections.abc', 'datetime', '_sqlite3',
                        'time')),

    '_sre':
        CoreExtensionModule(internal=True),

    'sre_compile':
        PythonModule(max_version=(3, 10), internal=True,
                deps=('_sre', 'sre_constants', 'sre_parse')),

    'sre_constants':
        PythonModule(max_version=(3, 10), internal=True, deps='_sre'),

    'sre_parse': (
        PythonModule(version=(3, 7), internal=True,
                deps=('sre_constants', 'warnings')),
        PythonModule(min_version=(3, 8), max_version=(3, 10), internal=True,
                deps=('sre_constants', 'unicodedata', 'warnings'))),

    '_ssl':
        ExtensionModule(internal=True,
                source='_ssl.c', deps='OpenSSL:openssl', pyd='_ssl.pyd',
                dlls=('libcrypto-1_1.dll', 'libssl-1_1.dll')),

    '_stat':
        CoreExtensionModule(internal=True),

    '_string':
        CoreExtensionModule(internal=True),

    '_strptime':
        PythonModule(internal=True,
                deps=('calendar', 'datetime', 'locale', 're', '_thread',
                        'time')),

    '_struct': (
        ExtensionModule(max_version=(3, 9), internal=True, source='_struct.c'),
        ExtensionModule(min_version=(3, 10), internal=True,
                source='_struct.c', defines='Py_BUILD_CORE_MODULE')),

    '_symtable':
        CoreExtensionModule(internal=True),

    '_sysconfigdata_m_linux_android':
        PythonModule(target='android', internal=True),

    '_sysconfigdata_m_darwin_ios':
        PythonModule(target='ios', internal=True),

    '_sysconfigdata_m_darwin_darwin':
        PythonModule(target='macos', internal=True),

    '_sysconfigdata_m_linux_x86_64-linux-gnu':
        PythonModule(target='linux', internal=True),

    'tomllib._parser':
        PythonModule(min_version=(3, 11), internal=True,
                deps=('collections.abc', 'string', 'tomllib._re',
                        'tomllib._types', 'types', 'typing')),

    'tomllib._re':
        PythonModule(min_version=(3, 11), internal=True,
                deps=('datetime', 'functools', 're', 'tomllib._types',
                        'typing')),

    'tomllib._types':
        PythonModule(min_version=(3, 11), internal=True, deps='typing'),

    '_tracemalloc':
        CoreExtensionModule(internal=True),

    '_uuid': (
        # Android doesn't implement uuid_t in uuid.h.  Windows doesn't have
        # uuid.h.
        ExtensionModule(max_version=(3, 9, 7), target='ios|macos',
                internal=True,
                source='_uuidmodule.c', pyd='_uuid.pyd'),
        ExtensionModule(min_version=(3, 9, 8), target='ios|linux|macos',
                internal=True,
                source='_uuidmodule.c', libs='linux#-luuid', pyd='_uuid.pyd')),

    '_warnings':
        CoreExtensionModule(internal=True),

    '_weakref':
        CoreExtensionModule(internal=True),

    '_weakrefset': (
        PythonModule(max_version=(3, 8), internal=True, deps='_weakref'),
        PythonModule(min_version=(3, 9), internal=True,
                deps=('types', '_weakref'))),

    '_winapi':
        ExtensionModule(target='win', internal=True, source='_winapi.c'),

    'xml.dom.domreg':
        PythonModule(internal=True, deps=('xml.dom', 'os')),

    'xml.dom.expatbuilder':
        PythonModule(internal=True,
                deps=('xml.dom', 'xml.dom.minicompat', 'xml.dom.minidom',
                        'xml.parsers.expat')),

    'xml.dom.minicompat':
        PythonModule(internal=True, deps='xml.dom'),

    'xml.dom.NodeFilter':
        PythonModule(internal=True),

    'xml.dom.xmlbuilder': (
        PythonModule(max_version=(3, 8), internal=True,
                deps=('xml.dom', 'copy', 'posixpath', 'urllib.parse',
                        'urllib.request', 'warnings', 'xml.dom.expatbuilder',
                        'xml.dom.NodeFilter')),
        PythonModule(min_version=(3, 9), internal=True,
                deps=('xml.dom', 'copy', 'posixpath', 'urllib.parse',
                        'urllib.request', 'xml.dom.expatbuilder',
                        'xml.dom.NodeFilter'))),

    'xml.etree.ElementPath':
        PythonModule(internal=True, deps=('xml.etree', 're')),

    'xml.sax._exceptions':
        PythonModule(internal=True, deps='xml.sax'),

    'zoneinfo._common':
        PythonModule(min_version=(3, 9), internal=True,
                deps=('zoneinfo', 'importlib.resources', 'struct')),

    'zoneinfo._tzpath':
        PythonModule(min_version=(3, 9), internal=True,
                deps=('zoneinfo', 'importlib.resources', 'os', 'sysconfig',
                        'warnings')),

    'zoneinfo._zoneinfo': (
        ExtensionModule(version=(3, 9), internal=True,
                source='_zoneinfo.c',
                deps=('zoneinfo', 'io', 'zoneinfo._common',
                        'zoneinfo._tzpath'),
                pyd='_zoneinfo.pyd'),
        ExtensionModule(min_version=(3, 10), internal=True,
                source='_zoneinfo.c', defines='Py_BUILD_CORE_MODULE',
                deps=('zoneinfo', 'io', 'zoneinfo._common',
                        'zoneinfo._tzpath'),
                pyd='_zoneinfo.pyd')),
}
