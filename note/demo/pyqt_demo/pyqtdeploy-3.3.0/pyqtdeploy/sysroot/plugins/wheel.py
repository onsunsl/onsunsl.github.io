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


from ... import Component, ComponentOption, PythonPackage


class wheelPlugin(Component):
    """ The wheel plugin.  This is designed to create multiple components. """

    # The list of components that, if specified, should be installed before
    # this one.
    preinstalls = ['Python']

    # The dict of parts provided by the component.
    @property
    def provides(self):
        return {
            self.name:
                PythonPackage(version=self.version, deps=self.dependencies,
                        exclusions=self.exclusions)
        }

    # The version will be extracted from the name of the wheel.
    version_is_optional = True

    def get_archive_name(self):
        """ Return the filename of the wheel. """

        return self.wheel

    def get_archive_urls(self):
        """ Return the list of URLs where the source archive might be
        downloaded from.
        """

        return self.get_pypi_urls(self.project)

    def get_options(self):
        """ Return a list of ComponentOption objects that define the components
        configurable options.
        """

        options = super().get_options()

        options.append(
                ComponentOption('dependencies', type=list,
                        help="The component:modules that this component "
                                "depends on."))

        options.append(
                ComponentOption('exclusions', type=list,
                        help="The files and directories of this component "
                                "that should be excluded."))

        options.append(
                ComponentOption('project', type=str, default=self.name,
                        help="The name of the PyPI project."))

        options.append(
                ComponentOption('wheel', type=str, required=True,
                        help="The name of the wheel."))

        return options

    def install(self):
        """ Install for the target. """

        self.unpack_wheel(self.get_archive())

    def verify(self):
        """ Verify the component. """

        wheel_version = self.parse_version_number(self.wheel.split('-')[1])

        if self.version is None:
            self.version = wheel_version
        elif self.version != wheel_version:
            self.error(
                    "v{0} is specified but the wheel is v{1}".format(
                            self.version, installed_version))
