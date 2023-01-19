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


import glob
import os

from ... import Component, ComponentOption, ExtensionModule


class SIPComponent(Component):
    """ The SIP component (ie. the sip module). """

    # The list of components that, if specified, should be installed before
    # this one.
    preinstalls = ['Python', 'Qt']

    # The version will be determined dynamically.
    version_is_optional = True

    def get_archive(self):
        """ Return the pathname of a local copy of the source archive. """

        # Create the archive in the current directory.
        self.run('sip-module', '--sdist', self.module_name, '--abi-version',
                str(self.abi_major_version))

        # Work out what the name was.
        pattern = '{}-{}.*.tar.gz'.format(
                self.module_name.replace('.', '_'), self.abi_major_version)
        archives = glob.glob(pattern)

        if len(archives) == 0:
            self.error("sip-module didn't create an sdist")

        if len(archives) > 1:
            self.error("Several possible sdists found: " + ', '.join(archives))

        return archives[0]

    def get_options(self):
        """ Return a list of ComponentOption objects that define the components
        configurable options.
        """

        options = super().get_options()

        options.append(
                ComponentOption('abi_major_version', required=True, type=int,
                        help="The major number of the ABI of the sip module."))

        options.append(
                ComponentOption('module_name', required=True,
                        help="The qualified name of the sip module."))

        return options

    def install(self):
        """ Install for the target. """

        archive = self.get_archive()
        self.unpack_archive(archive)

        # Gather the name of the source and header files
        sources = []
        headers = []

        for fname in os.listdir():
            if fname.endswith('.c') or fname.endswith('.cpp'):
                sources.append(fname)
            elif fname.endswith('.h'):
                headers.append(fname)

        # Create a .pro file to build the module.
        python = self.get_component('Python')

        if self.target_platform_name == 'android':
            android_abi = self.android_abi
        else:
            android_abi = ''

        module_dir = os.sep.join(self.module_name.split('.')[:-1])

        pro = _SIP_PRO.format(android_abis=android_abi,
                includepath=python.target_py_include_dir,
                sitepackages=os.path.join(python.target_sitepackages_dir,
                        module_dir),
                sources=' '.join(sources), headers=' '.join(headers))

        with self.create_file('sip.pro') as f:
            f.write(pro)

        # Run qmake and make to install it.
        self.run(self.get_component('Qt').host_qmake)
        self.run(self.host_make)
        self.run(self.host_make, 'install')

    @property
    def provides(self):
        """ The dict of parts provided by the component. """

        lib_dir = self.get_component('Python').target_sitepackages_dir

        parts = self.module_name.split('.')
        if len(parts) > 1:
            lib_dir = os.path.join(lib_dir, os.path.join(*parts[:-1]))

        # Note that there is no dependency on the containing package because we
        # don't know the name of the component that provides it.
        return {
            self.module_name: ExtensionModule(
                    deps=('Python:atexit', 'Python:enum', 'Python:gc'),
                    libs=('-L' + lib_dir, '-lsip'))
        }

    def verify(self):
        """ Verify the component. """

        installed_version = self.parse_version_number(
                self.run('sip-module', '--version', capture=True))

        if self.version is None:
            self.version = installed_version
        elif self.version != installed_version:
            self.error(
                    "v{0} is specified but the host installation is "
                            "v{1}".format(self.version, installed_version))

        # SIP v6.2 is the minimum version required as it is the first that
        # doesn't implement multiple minor versions of the same major version
        # of the ABI.
        if self.version < (6, 2):
            sip.unsupported()


# The skeleton .pro file for the sip module.
_SIP_PRO = """TEMPLATE = lib
TARGET = sip
CONFIG -= qt
CONFIG += warn_on exceptions_off staticlib release
ANDROID_ABIS = {android_abis}

INCLUDEPATH += {includepath}

target.path = {sitepackages}
INSTALLS += target

SOURCES = {sources}
HEADERS = {headers}
"""
