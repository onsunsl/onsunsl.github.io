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


class PyQtChartComponent(Component):
    """ The PyQtChart component. """

    # The list of components that, if specified, should be installed before
    # this one.
    preinstalls = ['Python', 'PyQt', 'Qt', 'SIP']

    # The dict of parts provided by the component.
    provides = {
        'PyQt5.QtChart':
            ExtensionModule(deps='PyQt:PyQt5.QtWidgets', libs='-lQtChart',
                    qmake_qt='charts')
    }

    def get_archive_name(self):
        """ Return the filename of the source archive. """

        if self._commercial:
            return 'PyQtChart_commercial-{}.tar.gz'.format(self.version)

        return 'PyQtChart-{}.tar.gz'.format(self.version)

    def get_archive_urls(self):
        """ Return the list of URLs where the source archive might be
        downloaded from.
        """

        if self._commercial:
            return super().get_archive_urls()

        return self.get_pypi_urls('PyQtChart')

    def install(self):
        """ Install for the target. """

        # See if it is the commercial version.
        self._commercial = (self.get_file('pyqt-commercial.sip') is not None)

        # Unpack the source.
        self.unpack_archive(self.get_archive())

        # Install.
        pyqt = self.get_component('PyQt')
        pyqt.install_pyqt_component(self)

    def verify(self):
        """ Verify the component. """

        # v5.14 is the first version supported by SIP v5.
        if self.version < (5, 14):
            self.unsupported()

        if self.version > (5, 15):
            self.untested()

        pyqt = self.get_component('PyQt')
        pyqt.verify_pyqt_component(self.version, min_sipbuild_version=(5, 4),
                min_pyqtbuild_version=(1, 9))
