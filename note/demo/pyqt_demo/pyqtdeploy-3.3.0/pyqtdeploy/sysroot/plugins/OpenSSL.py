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
import shutil

from ... import Component, ComponentLibrary


# OpenSSL currently has 2 relevent 'releases': v1.1.0 and v1.1.1.
#
# Python v3.7.0 to v3.7.3 uses v1.1.0 and later versions use v1.1.1.
#
# Qt v5.15 requires OpenSSL v1.1.1, earlier versions only require OpenSSL
# v1.0.0.  The binary installers of Qt v5.12.4 and later are built against
# OpenSSL v1.1.1.


class OpenSSLComponent(Component):
    """ The OpenSSL component. """

    # Add the 'install_from_source' option.
    option_install_from_source = True

    # The version will be determined dynamically if the system provided version
    # is being used.
    version_is_optional = True

    def get_archive_name(self):
        """ Return the filename of the source archive. """

        return 'openssl-{}.tar.gz'.format(self.version)

    def get_archive_urls(self):
        """ Return the list of URLs where the source archive might be
        downloaded from.
        """

        # The URLs depend on the version number.
        if self.version >= (1, 1, 1):
            sub_url = '1.1.1'
        else:
            sub_url = '1.1.0'

        return ['https://www.openssl.org/source/old/{}/'.format(sub_url),
                'https://www.openssl.org/source/']

    def install(self):
        """ Install for the target. """

        if not self.install_from_source:
            return

		# Unpack the source.
        self.unpack_archive(self.get_archive())

        # Set common options.
        common_options = ['--prefix=' + self.sysroot_dir, 'no-engine']

        if self.host_platform_name == 'win' and self.find_exe('nasm', required=False) is None:
            self.verbose(
                    "disabling assembler optimisations as nasm isn't "
                            "installed")
            common_options.append('no-asm')

        self._install_1_1(common_options)

    @property
    def provides(self):
        """ The dict of parts provided by the component. """

        bundle_shared_libs = self.target_platform_name == 'android'

        part = ComponentLibrary(
                libs=('win#-llibcrypto', '!win#-lcrypto', 'win#-llibssl',
                        '!win#-lssl'),
                bundle_shared_libs=bundle_shared_libs)

        return {'openssl': part}

    def sdk_configure(self, platform_name):
        """ Perform any platform-specific SDK configuration. """

        if platform_name == 'android':
            # OpenSSL v1.1.1 expects ANDROID_NDK_HOME to be set rather than
            # ANDROID_NDK_ROOT.
            if 'ANDROID_NDK_HOME' not in os.environ:
                os.environ['ANDROID_NDK_HOME'] = self.android_ndk_root
                setattr(self, '_android_ndk_home_set', True)

    def sdk_deconfigure(self, platform_name):
        """ Remove any platform-specific SDK configuration applied by a
        previous call to sdk_configure().
        """

        if platform_name == 'android':
            if getattr(self, '_android_ndk_home_set', False):
                del os.environ['ANDROID_NDK_HOME']
                delattr(self, '_android_ndk_home_set')

    def verify(self):
        """ Verify the component. """

        if self.install_from_source:
            if self.version is None:
                self.error(
                        "'version' must be specified when installing from "
                        "source")

            # We only cross-compile to Android.
            host = self.host_platform_name
            target = self.target_platform_name

            if target != host and target != 'android':
                self.error(
                        "installing for {0} on {1} is not supported".format(
                                target, host))

            # Check the required host tools are available.
            self.find_exe('perl')
        else:
            installed_version = self._get_installed_version()

            if self.version is None:
                self.version = installed_version
            elif self.version != installed_version:
                self.error(
                        "v{0} is specified but the host installation is "
                                "v{1}".format(self.version, installed_version))

        # We only support v1.1.0 and later.
        if (1, 1, 0) > self.version > (1, 1, 1):
            self.unsupported()

    def _install_1_1(self, common_options):
        """ Install v1.1 for supported platforms. """

        if self.target_platform_name == self.host_platform_name:
            # We are building natively.

            if self.target_platform_name == 'win':
                self._install_1_1_win(common_options)
            else:
                args = ['./config', 'no-shared']
                args.extend(common_options)

                self.run(*args)
                self.run(self.host_make)
                self.run(self.host_make, 'install')
        else:
            # We are cross-compiling.

            if self.target_platform_name == 'android':
                self._install_1_1_android(common_options)

    def _install_1_1_android(self, common_options):
        """ Install v1.1 for Android on either Linux or MacOS hosts. """

        # Configure the environment.
        original_path = self.add_to_path(self.android_toolchain_bin)

        configure_args = ['perl', 'Configure']

        configure_args.extend(common_options)

        configure_args.append('shared')
        configure_args.append('-D__ANDROID_API__={}'.format(self.android_api))

        if self.target_arch_name == 'android-32':
            os_compiler = 'android-arm'
        else:
            os_compiler = 'android-arm64'

        configure_args.append(os_compiler)

        self.run(*configure_args)

        self.run(self.host_make, 'SHLIB_VERSION_NUMBER=', 'SHLIB_EXT=_1_1.so',
                'build_libs')

        # Install the shared libraries.  Qt requires the versioned name and
        # Python requires the unversioned symbolic link.
        for lib in ('libcrypto', 'libssl'):
            versioned = lib + '_1_1.so'

            shutil.copy(versioned, self.target_lib_dir)

            link = os.path.join(self.target_lib_dir, lib + '.so')
            try:
                os.remove(link)
            except:
                pass

            os.symlink(versioned, link)

        # Install the header files.
        headers_dir = os.path.join(self.target_include_dir, 'openssl')
        shutil.rmtree(headers_dir, ignore_errors=True)
        shutil.copytree(os.path.join('include', 'openssl'), headers_dir)

        # Restore the environment.
        os.environ['PATH'] = original_path

    def _install_1_1_win(self, common_options):
        """ Install v1.1 for Windows. """

        # Set the architecture-specific values.
        if self.target_arch_name.endswith('-64'):
            target = 'VC-WIN64A'
        else:
            target = 'VC-WIN32'

        args = ['perl', 'Configure', target, 'no-shared',
                '--openssldir=' + self.sysroot_dir + '\\ssl']
        args.extend(common_options)

        self.run(*args)
        self.run(self.host_make)
        self.run(self.host_make, 'install')

    def _get_installed_version(self):
        """ Get the installed version. """

        # We only support Linux native versions.
        if self.target_platform_name != 'linux':
            self.error(
                    "using an existing installation is only supported for "
                    "Linux targets.")

        version_line = self.get_version_from_file('OPENSSL_VERSION_NUMBER',
                '/usr/include/openssl/opensslv.h')

        # Extract the version number from the line.
        version = version_line.split()[-1]
        if version.startswith('0x'):
            version = version[2:]
        if version.endswith('L'):
            version = version[:-1]

        try:
            version = int(version, base=16)
        except ValueError:
            self.error("unable to extract the version number")

        major = (version >> 28) & 0xff
        minor = (version >> 20) & 0xff
        patch = (version >> 12) & 0xff
        suffix = chr(((version >> 4) & 0x0f) + ord('a') - 1)

        return self.parse_version_number((major, minor, patch, suffix))
