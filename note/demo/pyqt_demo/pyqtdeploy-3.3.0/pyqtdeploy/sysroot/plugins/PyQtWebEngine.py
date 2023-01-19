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


from ... import Component, ExtensionModule


class PyQtWebEngineComponent(Component):
    """ The PyQtWebEngine component. """

    # The list of components that, if specified, should be installed before
    # this one.
    preinstalls = ['Python', 'PyQt', 'Qt', 'SIP']

    def get_archive_name(self):
        """ Return the filename of the source archive. """

        if self._commercial:
            return 'PyQtWebEngine_commercial-{}.tar.gz'.format(self.version)

        return 'PyQtWebEngine-{}.tar.gz'.format(self.version)

    def get_archive_urls(self):
        """ Return the list of URLs where the source archive might be
        downloaded from.
        """

        if self._commercial:
            return super().get_archive_urls()

        return self.get_pypi_urls('PyQtWebEngine')

    def install(self):
        """ Install for the target. """

        # See if it is the commercial version.
        self._commercial = (self.get_file('pyqt-commercial.sip') is not None)

        # Unpack the source.
        self.unpack_archive(self.get_archive())

        # Install.
        pyqt = self.get_component('PyQt')
        pyqt.install_pyqt_component(self)

    @property
    def provides(self):
        """ The dict of parts provided by the component. """

        widgets_deps = ('PyQt5.QtWebEngineCore', 'PyQt:PyQt5.QtNetwork',
                'PyQt:PyQt5.QtPrintSupport', 'PyQt:PyQt5.QtWidgets')

        if 'QtWebChannel' in self.get_component('PyQt').installed_modules:
            widgets_deps += ('PyQt:PyQt5.QtWebChannel', )

        return {
            'PyQt5.QtWebEngine':
                ExtensionModule(deps='PyQt5.QtWebEngineCore',
                        libs='-lQtWebEngine', qmake_qt='webengine'),
            'PyQt5.QtWebEngineCore':
                ExtensionModule(
                        deps=('PyQt:PyQt5.QtNetwork', 'PyQt:PyQt5.QtGui'),
                        libs='-lQtWebEngineCore', qmake_qt='webenginecore'),
            'PyQt5.QtWebEngineWidgets':
                ExtensionModule(deps=widgets_deps, libs='-lQtWebEngineWidgets',
                        qmake_cpp11=True, qmake_qt='webenginewidgets'),
        }

    def verify(self):
        """ Verify the component. """

        # v5.14 is the first version supported by SIP v5.
        if self.version < (5, 14):
            self.unsupported()

        if self.version > (5, 15):
            self.untested()

        if self.target_platform_name in ('android', 'ios'):
            self.error(
                    "PyQtWebEngine is not supported on {0}".format(
                            self.target_platform_name))

        pyqt = self.get_component('PyQt')
        pyqt.verify_pyqt_component(self.version, min_sipbuild_version=(5, 4),
                min_pyqtbuild_version=(1, 9))
