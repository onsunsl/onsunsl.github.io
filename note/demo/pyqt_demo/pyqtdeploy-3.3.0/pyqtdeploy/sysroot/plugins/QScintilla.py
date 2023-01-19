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

from ... import Component, ExtensionModule


class QScintillaComponent(Component):
    """ The QScintilla component. """

    # The list of components that, if specified, should be installed before
    # this one.
    preinstalls = ['Python', 'PyQt', 'Qt', 'SIP']

    def get_archive_name(self):
        """ Return the filename of the source archive. """

        if self._commercial:
            return 'QScintilla_commercial-{}.tar.gz'.format(
                    self._version_str)

        if self.version <= (2, 11, 2):
            return 'QScintilla_gpl-{}.tar.gz'.format(self._version_str)

        return 'QScintilla-{}.tar.gz'.format(self._version_str)

    def get_archive_urls(self):
        """ Return the list of URLs where the source archive might be
        downloaded from.
        """

        if self._commercial:
            return super().get_archive_urls()

        if self.version <= (2, 11):
            return ['https://www.riverbankcomputing.com/static/Downloads/QScintilla/{}/'.format(self._version_str)]

        return self.get_pypi_urls('QScintilla')

    def install(self):
        """ Install for the target. """

        pyqt = self.get_component('PyQt')

        # See if it is the commercial version.
        self._commercial = (self.get_file('pyqt-commercial.sip') is not None)

        # Unpack the source.
        self.unpack_archive(self.get_archive())

        if self.version <= (2, 11):
            # Build the static C++ library.
            os.chdir('Qt4Qt5')

            # Somewhere between Qt v5.13 and v5.15 'printsupport' was removed
            # from the iOS mkspecs.  We patch the .pro and feature files rather
            # than require a fixed version of QScintilla.
            if self.target_platform_name == 'ios':
                self.patch_file('qscintilla.pro', self._patch_pro_for_ios)
                self.patch_file(
                        os.path.join('features_staticlib', 'qscintilla2.prf'),
                        self._patch_pro_for_ios)

            qmake_args = [self.get_component('Qt').host_qmake,
                    'CONFIG+=staticlib', 'DEFINES+=SCI_NAMESPACE']

            if self.target_platform_name == 'android':
                qmake_args.append('ANDROID_ABIS={}'.format(self.android_abi))

            # PyQt-builder explcitly specifies the release/debug mode and
            # we can't make assumptions about the default.
            qmake_args.append('CONFIG+=release')

            self.run(*qmake_args)

            self.run(self.host_make)
            self.run(self.host_make, 'install')
            os.chdir('..')

        # Build the static Python bindings.  If there is no printer support
        # then make sure we don't try and import it.
        if self._is_print_support:
            bindings_config = None
        else:
            bindings_config = {
                'disabled-features': ['PyQt_Printer']
            }

        # The QScintilla pyproject.toml file doesn't have a bindings
        # section so we need to explicitly specify the enabled modules.
        pyqt.install_pyqt_component(self, bindings=bindings_config,
                enable=['Qsci'])

    @property
    def provides(self):
        """ The dict of parts provided by the component. """

        deps = 'PyQt:PyQt5.QtWidgets'

        if self._is_print_support:
            deps = (deps, 'PyQt:PyQt5.QtPrintSupport')

        return {
            'PyQt5.Qsci':
                ExtensionModule(deps=deps, libs='-lQsci',
                        qmake_config='qscintilla2')
        }

    def verify(self):
        """ Verify the component. """

        # We don't want to support old versions.
        if self.version < (2, 11):
            self.unsupported("use v2.11 or later")

        # A bug in these versions broke builds for iOS.
        if self.target_platform_name == 'ios' and (2, 12) <= self.version <= (2, 13, 1):
            self.unsupported("use v2.13.2 or later")

        if self.version > (2, 13, 3):
            self.untested()

        # The Scintilla code uses C++ library functions that are missing prior
        # to NDK v14.
        if self.target_platform_name == 'android' and self.android_ndk_version < 14:
            self.error("Android NDK r14 or later is required")

        pyqt = self.get_component('PyQt')
        pyqt.verify_pyqt_component(pyqt.version, min_sipbuild_version=(5, 4),
                min_pyqtbuild_version=(1, 9))

    @property
    def _is_print_support(self):
        """ Return True if print support is available. """

        return 'QtPrintSupport' in self.get_component('PyQt').installed_modules

    @staticmethod
    def _patch_pro_for_ios(line, patch_file):
        """ Disable all support for printing in the .pro file. """

        if 'qsciprinter' in line:
            pass
        else:
            patch_file.write(line.replace('printsupport', ''))

    @property
    def _version_str(self):
        """ Return the version number as a string. """

        # The current convention for .0 releases began after v2.11.0.
        return '2.11' if self.version == (2, 11, 0) else str(self.version)
