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


import os

from ... import Component, ComponentLibrary, ComponentOption


class libffiComponent(Component):
    """ The libffi component. """

    # Add the 'install_from_source' option.
    option_install_from_source = True

    # The list of components that, if specified, should be installed before
    # this one.
    preinstalls = ['Python']

    # The version will be determined dynamically if the system provided version
    # is being used.
    version_is_optional = True

    def get_archive_name(self):
        """ Return the filename of the source archive. """

        return 'libffi-{}.tar.gz'.format(self.version)

    def get_archive_urls(self):
        """ Return the list of URLs where the source archive might be
        downloaded from.
        """

        return ['https://github.com/libffi/libffi/releases/download/v{}/'.format(self.version)]

    def install(self):
        """ Install for the target. """

        if not self.install_from_source:
            return

        # Unpack the source.
        self.unpack_archive(self.get_archive())

        # Use the script included with Python to do the build.
        if self.target_arch_name == 'win-64':
            arch_flag = '-x64'
            arch_subdir = 'amd64'
        else:
            arch_flag = '-x86'
            arch_subdir = 'win32'

        prep = os.path.join(self.target_src_dir,
                'Python-{}'.format(self.get_component('Python').version),
                'PCbuild', 'prepare_libffi.bat')

        src_dir = os.getcwd()
        out_dir = os.path.join(src_dir, 'out')
        arch_dir = os.path.join(out_dir, arch_subdir)

        os.environ['LIBFFI_SOURCE'] = src_dir
        os.environ['LIBFFI_OUT'] = out_dir

        self.run(prep, arch_flag)

        del os.environ['LIBFFI_SOURCE']
        del os.environ['LIBFFI_OUT']

        # Install in the target sysroot.
        for ext in ('.dll', '.lib'):
            self.copy_file(os.path.join(arch_dir, self._lib_name + ext),
                    self.target_lib_dir)

        for hdr in ('ffi.h', 'fficonfig.h', 'ffitarget.h'):
            self.copy_file(os.path.join(arch_dir, 'include', hdr),
                    self.target_include_dir)

    @property
    def provides(self):
        """ The dict of parts provided by the component. """

        bundle_shared_libs = (self.target_platform_name == 'win')

        return {
                'libffi': ComponentLibrary(
                        libs=('win#-l{}'.format(self._lib_name), '!win#-lffi'),
                        bundle_shared_libs=bundle_shared_libs)
        }

    def verify(self):
        """ Verify the component. """

        if self.target_platform_name in ('android', 'ios'):
            self.error(
                    "'{0}' is not a supported target platform".format(
                            self.target_platform_name))

        if self.install_from_source:
            if self.version is None:
                self.error(
                        "'version' must be specified when installing from "
                        "source")

            # Check Cygwin is installed.
            if not os.path.isdir('C:\\cygwin'):
                self.error("Cygwin must be installed in C:\\cygwin")
        else:
            installed_version = self._get_installed_version()

            if self.version is None:
                self.version = installed_version
            elif self.version != installed_version:
                self.error(
                        "v{0} is specified but the host installation is "
                                "v{1}".format(self.version, installed_version))

        if (3, 3) > self.version >= (3, 5):
            self.unsupported("use v3.3 or v3.4")

    def _get_installed_version(self):
        """ Get the installed version. """

        if self.target_platform_name == 'win':
            self.error(
                    "using an existing installation is not supported for "
                    "Windows targets")

        if self.target_platform_name == 'macos':
            ffi_h_dir = self.apple_sdk + '/usr/include/ffi'
        elif self.target_platform_name == 'linux':
            ffi_h_dir = '/usr/include/x86_64-linux-gnu'

        version_file = ffi_h_dir + '/ffi.h'
        version_line = self.get_version_from_file('libffi', version_file)

        # The version number seems to be the second 'word' of the line.
        version_str = version_line.split()[1]

        return self.parse_version_number(version_str)

    @property
    def _lib_name(self):
        """ The name of the Windows library, excluding the extension. """

        lib_version = 7 if self.version == (3, 3) else 8

        return 'libffi-{}'.format(lib_version)
