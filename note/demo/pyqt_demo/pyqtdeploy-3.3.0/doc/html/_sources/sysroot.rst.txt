.. _ref-building-a-sysroot:

.. program:: pyqtdeploy-sysroot

Building a System Root Directory
================================

:program:`pyqtdeploy-sysroot` is used to create a target-specific system root
directory (*sysroot*) containing any *components* required by the application.

:program:`pyqtdeploy-sysroot` is actually a wrapper around a number of
component plugins.  A plugin, written in Python, is responsible for installing
the individual *parts* that make up a component.  A part may be a Python
package, an extension module or a supporting library.

A sysroot is defined by a `TOML <https://github.com/toml-lang/toml>`__
specification file.  This contains a section for each component to install.
The key/value options of a section determine how the component is configured.
Component sections may have target-specific sub-sections so that they can be
configured on a target by target basis.

The components are installed in the correct order irrespective of where they
appear in the specification file.

A component will only be installed in a sysroot if it hasn't already been done.
However if the installed version is different then all components will be
re-installed.  This is done because some components take a long time to
install (building Qt from source being the obvious example) making it very
inconvenient when debugging the installation of a later component.

An API is provided to allow you to develop your own component plugins.  If you
develop a plugin for a commonly used component then please consider
contributing it so that it can be included in a future release of
:program:`pyqtdeploy`.  Defining a component in this way is described in
:ref:`ref-component-plugin`.

Many applications will use third-party packages packaged as wheels and
installed from PyPI.  Rather than require you to write a component plugin in
Python for these, :program:`pyqtdeploy` provides the ``wheel`` plugin which
takes the necessary information about the package from the sysroot
specification file.  Defining a component in this way is described in
:ref:`ref-component-spec-file`.

Standard Component Plugins
--------------------------

The following component plugins are included as standard with
:program:`pyqtdeploy`.

**libffi**
    This provides the libffi library as a DLL for Windows.  On macOS and Linux
    it provides access to the OS supplied library.  It is currently not
    supported on other target architectures.  It is required by the Python
    :mod:`ctypes` module.  In order to build it on Windows Cygwin must be
    installed in :file:`C:\cygwin` (although it does not need to be included in
    :envvar:`PATH`).  Current Python source packages include
    :file:`prepare_libffi.bat` in the :file:`PCbuild` directory which will can
    be run to install an appropriate version of Cygwin.

**OpenSSL**
    This provides the OpenSSL libraries for v1.1.0 and later on Android (as a
    shared library), Linux (using the OS supplied library), macOS (as a static
    library) and Windows (as a static library).  When building from source it
    requires ``perl`` to be installed on :envvar:`PATH`.

**PyQt**
    This provides a static version of the PyQt5 extension modules for all
    target architectures.

**PyQt3D**
    This provides a static version of the PyQt3D extension modules for all
    target architectures.

**PyQtChart**
    This provides a static version of the PyQtChart extension module for all
    target architectures.

**PyQtDataVisualization**
    This provides a static version of the PyQtDataVisualization extension
    module for all target architectures.

**PyQtNetworkAuth**
    This provides a static version of the PyQtNetworkAuth extension module for
    all target architectures.

**PyQtPurchasing**
    This provides a static version of the PyQtPurchasing extension module for
    all target architectures.

**PyQtWebEngine**
    This provides a static version of the PyQtWebEngine extension module for
    all target architectures.

**Python**
    This will provide Python from source, or use an existing installation, for
    both the host and target architectures.  Building the host version from
    source is not supported on Windows.  Installing the host version from an
    existing installation is not supported on Android or iOS.  The target
    version of the Python library and extension modules built from source will
    be built statically.  Installing the target version from an existing
    installation is only supported on Windows.

**QScintilla**
    This provides a static version of the QScintilla library and Python
    extension module for all target architectures.

**Qt**
    This will provide a static version of Qt5 from source (but not for the
    Android and iOS targets).  It will use an existing installation created by
    the standard Qt installer.

**SIP**
    This provides a static version of the :mod:`sip` extension module for all
    target architectures.

**zlib**
    This provides a static version of the zlib library for all target
    architectures.  It can also use an OS supplied library for all targets
    except Windows.


Creating a Sysroot Specification File
-------------------------------------

The following specification file contains a section for each of the standard
component plugins.  (You can also download a copy of the file from
:download:`here</examples/sysroot.toml>`).  Dummy values have been used for all
required configuration options.

.. literalinclude:: /examples/sysroot.toml

Using this file, run the following command::

    pyqtdeploy-sysroot --options sysroot.toml

You will then see a description of each component's configuration options, the
type of value expected and whether or not a value is required.  You can then
add options to the appropriate sections to meet your requirements.

If your application does not require all of the standard components then simply
remove the corresponding sections from the specification file.  If your
application requires additional components then you need to create appropriate
component plugins and add corresponding sections to the specification file.

At any time you can verify your specification file.  This will check that all
required options have a value and that all components have supported versions
that are mutually compatible.  It will also warn you if you have specified
versions that are untested (but should work).  To do this run::

    pyqtdeploy-sysroot --verify sysroot.toml

To build a native sysroot (i.e. for the host architecture) from a fully
configured specification file, run::

    pyqtdeploy-sysroot sysroot.toml


The :program:`pyqt-demo` Sysroot
--------------------------------

In this section we walk through the sysroot specification file for
:program:`pyqt-demo`, component by component.

OpenSSL
.......

::

    [OpenSSL]
    version = "1.1.1m"
    disabled_targets = ["ios"]

    [OpenSSL.linux]
    version = ""
    install_from_source = false

On iOS we choose to not support SSL from Python and use Qt's SSL support
instead (which will use Apple's Secure Transport).

On Linux we will use the OS supplied OpenSSL libraries and make no assumption
about what version might be installed.


Python
......

::

    [Python]
    version = "3.10.4"
    install_host_from_source = true

    [Python.win]
    install_host_from_source = false

The Python component plugin handles installation for both host and target
architectures.  For the host we choose to install from source except on Windows
where the registry is searched for the location of an existing installation.
For all target architecures we choose to build Python from source.

:program:`pyqt-demo` is a very simple application that does not need to
dynamically load extension modules.  If this was needed then the
``dynamic_loading`` option would be set to ``true``.


PyQt
....

::

    [PyQt]
    version = "5.15.6"

    [PyQt.android]
    disabled_features = ["PyQt_Desktop_OpenGL", "PyQt_Printer"]
    installed_modules = ["QtCore", "QtGui", "QtNetwork", "QtWidgets",
            "QtAndroidExtras"]

    [PyQt.ios]
    disabled_features = ["PyQt_Desktop_OpenGL", "PyQt_MacOSXOnly",
            "PyQt_MacCocoaViewContainer", "PyQt_Printer", "PyQt_Process",
            "PyQt_NotBootstrapped"]
    installed_modules = ["QtCore", "QtGui", "QtNetwork", "QtWidgets",
            "QtMacExtras"]

    [PyQt.linux]
    installed_modules = ["QtCore", "QtGui", "QtNetwork", "QtWidgets",
            "QtX11Extras"]

    [PyQt.macos]
    installed_modules = ["QtCore", "QtGui", "QtNetwork", "QtWidgets",
            "QtMacExtras"]

    [PyQt.win]
    disabled_features = ["PyQt_Desktop_OpenGL"]
    installed_modules = ["QtCore", "QtGui", "QtNetwork", "QtWidgets",
            "QtWinExtras"]

The two options used to tailor the build of PyQt are ``disabled_features``
and ``installed_modules``.

Unfortunately the list of features that can be disabled is not properly
documented and relate to how Qt is configured.  However how
``disabled_features`` is set in the above will be appropriate for most cases.

The ``installed_modules`` option is used to specify the names of the individual
PyQt extension modules to be installed.  We choose to build only those
extension modules needed by :program:`pyqt-demo`.


PyQt3D
......

::

    [PyQt3D]
    version = "5.15.5"

It is only necessary to specifiy the version to install.


PyQtChart
.........

::

    [PyQtChart]
    version = "5.15.5"

It is only necessary to specifiy the version to install.


PyQtDataVisualization
.....................

::

    [PyQtDataVisualization]
    version = "5.15.5"

It is only necessary to specifiy the version to install.


PyQtNetworkAuth
...............

::

    [PyQtNetworkAuth]
    version = "5.15.5"

It is only necessary to specifiy the version to install.


PyQtPurchasing
..............

::

    [PyQtPurchasing]
    version = "5.15.5"

It is only necessary to specifiy the version to install.


QScintilla
..........

::

    [QScintilla]
    version = "2.13.2"

It is only necessary to specifiy the version to install.


Qt
..

::

    [Qt]
    version = "5.15.2"
    edition = "opensource"
    configure_options = ["-opengl", "desktop", "-no-dbus", "-qt-pcre"]
    skip = ["qtactiveqt", "qtconnectivity", "qtdoc", "qtgamepad", "qtlocation",
            "qtmultimedia", "qtnetworkauth", "qtquickcontrols",
            "qtquickcontrols2", "qtremoteobjects", "qtscript", "qtscxml",
            "qtsensors", "qtserialbus", "qtserialport", "qtspeech", "qtsvg",
            "qttools", "qttranslations", "qtwayland", "qtwebchannel",
            "qtwebengine", "qtwebsockets", "qtwebview", "qtxmlpatterns"]

    [Qt.android]
    install_from_source = false
    ssl = "openssl-linked"

    [Qt.ios]
    install_from_source = false
    ssl = "securetransport"

    [Qt.linux]
    ssl = "openssl-runtime"

    [Qt.macos]
    ssl = "openssl-linked"

    [Qt.win]
    ssl = "openssl-linked"
    static_msvc_runtime = true

We have chosen to install Qt from source except for Android and iOS where we
will use an existing installation.  In the context of the demo this is defined
by the ``--qmake`` option of the ``build-demo.py`` script.

We use the ``configure_options`` and ``skip`` options to tailor the Qt build in
order to reduce the time taken to do the build.

The ``ssl`` option specifies how Qt's SSL support is to be implemented.

On Android we have chosen to link against the shared OpenSSL libraries
installed by the ``OpenSSL`` component plugin which are bundled automaticallly
with the application executable.

On iOS Qt is dynamically linked to the Secure Transport libraries.

On Linux we have chosen to dynamically load the OS supplied OpenSSL libraries
at runtime.

On macOS and Windows we have chosen to link against the static OpenSSL
libraries installed by the ``OpenSSL`` component plugin.

Finally we have specified that (on Windows) we will link to static versions of
the MSVC runtime libraries.


SIP
...

::

    [SIP]
    abi_major_version = 12
    module_name = "PyQt5.sip"

Note that the version number of SIP does not need to be specified.  A suitable
versions of PyQt-builder must be installed for the same Python installation
being used to run :program:`pyqtdeploy`.


zlib
....

::

    [zlib]
    install_from_source = false

    [zlib.win]
    version = "1.2.12"
    install_from_source = true
    static_msvc_runtime = true

On all targets, except for Windows, we choose to use the zlib library provided
by the OS.

On Windows we choose to build from the latest version of the source and link to
static versions of the MSVC runtime libraries.


The Command Line
----------------

The full set of command line options is:

.. option:: -h, --help

    This will display a summary of the command line options.

.. option:: -V, --version

    This specifies that the version number should be displayed on ``stdout``.
    The program will then terminate.

.. option:: --build-dir DIR

    .. versionadded:: 3.3.0

    ``DIR`` is the name of the temporary build directory used to build each
    component.  By default a directory called ``build`` in the target-specific
    sysroot directory is used.

.. option:: --component COMPONENT

    ``COMPONENT`` is the name of the component that will be installed.  It may
    be used more than once to install multiple components.  If the option is
    not specified then all components specified in the sysroot specification
    file will be installed.

.. option:: --force

    This causes all components to be installed even if components with the
    required versions have already been installed.

.. option:: --jobs NUMBER

    .. versionadded:: 3.3.0

    This specifies the number of :program:`make` jobs that will be run in
    parallel.  It only has an affect on Linux and macOS hosts.

.. option:: --no-clean

    A temporary build directory (by default called ``build`` in the sysroot) is
    created in order to build the required components.  Normally this is
    removed automatically after all components have been built.
    Specifying this option leaves the build directory in place to make
    debugging component plugins easier.

.. option:: --options

    This causes the configurable options of each component specified in the
    sysroot specification file to be displayed on ``stdout``.  The program will
    then terminate.

.. option:: --python EXECUTABLE

    ``EXECUTABLE`` is the full path name of the host Python interpreter.  It
    overrides any value provided by the sysroot but the version must be
    compatible with that specified in the sysroot specification file.

.. option:: --qmake EXECUTABLE

    ``EXECUTABLE`` is the full path name of the host :program:`qmake`.  It
    overrides any value provided by the sysroot but the version must be
    compatible with that specified in the sysroot specification file.

.. option:: --source-dir DIR

    ``DIR`` is the name of a directory containing any local copies of source
    archives used to install the components specified in the sysroot
    specification file.  It may be specified any number of times and each
    directory will be searched in turn.  If a local copy cannot be found then
    the component plugin will attempt to download it.

.. option:: --sysroots-dir DIR

    ``DIR`` is the name of the directory where the target-specific sysroot
    directory will be created.  A sysroot directory will be called ``sysroot-``
    followed by a target-specific suffix.  If all components are to be
    re-installed then any existing sysroot will first be removed and
    re-created.

.. option:: --target TARGET

    ``TARGET`` is the target architecture.  By default the host architecture is
    used.  On Windows the default is determined by the target architecture of
    the currently configured compiler.

.. option:: --quiet

    This specifies that progress messages should be disabled.

.. option:: --verbose

    This specifies that additional progress messages should be enabled.

.. option:: specification

    ``specification`` is the name of the sysroot specification file that
    defines each component to be included in the sysroot and how each is to be
    configured.


.. _ref-component-spec-file:

Defining a Component Using the Sysroot Specification File
---------------------------------------------------------

.. versionadded:: 3.2.0

As an example we will define a component for the
`certifi <https://pypi.org/project/certifi/>`__ project on PyPI.  It contains
a small number of :file:`.py` files and a data file, and only imports modules
from the Python standard library.

A component defined in the sysroot specification file makes use of the
``wheel`` component plugin that is included with :program:`pyqtdeploy`.

The following is the complete component definition::

    [certifi]
    plugin = "wheel"
    wheel = "certifi-2021.10.8-py2.py3-none-any.whl"
    dependencies = ["Python:importlib.resources", "Python:os"]
    exclusions = ["__main__.py"]

``plugin`` specifies that ``wheel`` is the component plugin to use.  For
components that have a dedicated plugin it is not normally required as it
defaults to the name of the component.

``wheel`` specifies the name of the wheel file that will be installed in the
sysroot.

``dependencies`` specifies a list of packages that the component depends on,
i.e. packages that are imported by the component.  A dependency is specified as
a component name and package name separated by ``:``.  In this case
:mod:`certifi` imports :mod:`importlib.resources` and :mod:`os` from the Python
standard library.

``exclusions`` specifies a list of files in the wheel that should not be
included as part of the deployed application.  In this case the
:file:`__main__.py` file is not used and therefore excluded.

.. note::

    :mod:`certifi` reads it's data file (:file:`cacert.pem`) using Python's
    resources mechanism (i.e. :mod:`importlib.resources`).  This means that it
    can read the file even though it will be embedded in the executable created
    by :program:`pyqtdeploy`.


.. _ref-component-plugin:

Defining a Component Using a Plugin
-----------------------------------

While using the sysroot specification file to define a component is convenient
in simple cases, it is often better to define a component using a component
plugin.  For example:

- you may need to check the component's version number to determine its exact
  dependencies and what it provides

- you may need to check the version numbers of any components on which it
  depends

- you may need to check that other requirements have been met, such as the
  correct version of an SDK.

Using a component plugin also makes it easier to build up a library of plugins
to be used in multiple projects.

A component plugin is a Python module that defines a sub-class of
:py:class:`pyqtdeploy.Component`.  Normally the name of the module is the name
used in the sysroot specification file (although ``plugin`` can be used to
change this).  It doesn't matter what the name of the sub-class is.

The following is a complete implementation of a component plugin for the
`certifi <https://pypi.org/project/certifi/>`__ project on PyPI.

::

    from pyqtdeploy import Component, PythonPackage

    class certifiComponent(Component):

        # The list of components that should be installed before this one.
        preinstalls = ['Python']

        # The dictionary of parts provided by the component keyed by the name
        # of the part.  In this case there is a single part which is a Python
        # package (ie. a directory containing a __init__.py file).
        provides = {
            'certifi': PythonPackage(
                    deps=['Python:importlib.resources', 'Python:os'],
                    exclusions='__main__.py')
        }

        def get_archive_name(self):
            """ Get the version dependent name of the wheel. """

            return 'certifi-{}-py2.py3-none-any.whl'.format(self.version)

        def get_archive_urls(self):
            """ Get the list of URLs where the wheel might be downloaded from.
            """

            # Return the PyPI URLs for the project.
            return self.get_pypi_urls('certifi')

        def install(self):
            """ Install the component. """

            # Unpack the wheel into the target Python installation's
            # site-packages directory.
            self.unpack_wheel(self.get_archive())

Hopefully the comments in the code are self explainatory.

The complete would be used as follows::

    [certifi]
    version = "2021.10.8"

Component plugins (other than those bundled with :program:`pyqtdeploy`) are
expected to be found in the directory containing the sysroot specification
file.

The following is the complete API available to a plugin.

.. py:module:: pyqtdeploy

.. py:class:: Component

    This is the base class of all component plugins.

    .. py:attribute:: android_abi

        The Android architecture-specific ABI being used.

    .. py:attribute:: android_api

        The integer Android API level being used.

    .. py:attribute:: android_ndk_root

        The path of the root of the Android NDK.

    .. py:attribute:: android_ndk_sysroot

        The path of the Android NDK's sysroot directory.

    .. py:attribute:: android_ndk_version

        The the version number of the Android NDK.

    .. py:attribute:: android_sdk_version

        The version number of the Android SDK.

    .. py:attribute:: android_toolchain_bin

        The path of the Android toolchain's bin directory.

    .. py:attribute:: android_toolchain_cc

        The name of the Android toolchain's C compiler.

    .. py:attribute:: android_toolchain_prefix

        The name of the Android toolchain's prefix.

    .. py:attribute:: apple_sdk

        The Apple SDK being used.

    .. py:attribute:: apple_sdk_version

        The version number of the Apple SDK.

    .. py:attribute:: building_for_target

        This is set to ``True`` by the component plugin to configure building
        (i.e. compiling and linking) for the target (rather than the host)
        architecture.  The default value is ``True``.

    .. py:method:: copy_dir(src, dst, ignore=None)

        A directory is copied, optionally excluding file and sub-directories
        that match a number of glob patterns.  If the destination directory
        already exists then it is first removed.  Any errors are handled
        automatically.

        :param str src: the name of the source directory.
        :param str dst: the name of the destination directory.
        :param list[str] ignore: an optional sequence of glob patterns that
            specify files and sub-directories that should be ignored.

    .. py:method:: copy_file(src, dst, macros=None)

        A file is copied while expanding and optional dict of macros.  Any
        errors are handled automatically.

        :param str src: the name of the source file.
        :param str dst: the name of the destination file.
        :param dict macros: the dict of name/value pairs.

    .. py:method:: create_dir(name, empty=False)

        A new directory is created if it does not already exist.  If it does
        already exist then it is optionally emptied.  Any errors are handled
        automatically.

        :param str name: the name of the directory.
        :param bool empty: ``True`` if an existing directory should be emptied.

    .. py:method:: create_file(name)

        A new text file is created and its file object returned.  Any errors
        are handled automatically.

        :param str name: the name of the file.
        :return: the file object of the created file.

    .. py:method:: delete_dir(name)

        A directory and any contents are deleted.  Any errors are handled
        automatically.

        :param str name: the name of the directory.

    .. py:method:: error(message, detail='')

        An error message is displayed to the user and the program immediately
        terminates.

        :param str message: the message.
        :param str detail: additional detail displayed if the
            :option:`--verbose <pyqtdeploy-sysroot --verbose>` option was
            specified.

    .. py:method:: find_exe(name, required=True)

        The absolute path name of an executable located on :envvar:`PATH` is
        returned.

        :param str name: the generic executable name.
        :param bool required: ``True`` if the executable is required and it is
            an error if it could not be found.
        :return: the absolute path name of the executable.

    .. py:method:: get_archive(name):

        The pathname of a local copy of the component's source archive is
        returned.  The directories specified by the
        :option:`--source-dir <pyqtdeploy-sysroot --source-dir>` option are
        searched first.  If the archive is not found then it is downloaded if
        the component supports it.

        :return: the pathname of the archive.

    .. py:method:: get_archive_name():
        :abstractmethod:

        This must be re-implemented to return the version-specific name of the
        component's source archive.

        :return: the name of the archive.

    .. py:method:: get_archive_urls():

        This is re-implemented to return a sequence of URLs (excluding the
        source archive name) from which the component's source archive may be
        downloaded from.

        :return: the sequence of URLs.

    .. py:method:: get_component(name, required=True)

        The :py:class:`~pyqtdeploy.Component` instance for a component is
        returned.

        :param str name: the name of the component.
        :param bool required: ``True`` if the component is required and it is
            an error if it was not specified.
        :return: the component instance.

    .. py:method:: get_file(name)

        The absolute path name of a file or directory in a directory specified
        by a :option:`--source-dir <pyqtdeploy-sysroot --source-dir>` option is
        returned.

        :param str name: the name of the file or directory.
        :return: the absolute path name of the file or directory or ``None`` if
            it wasn't found.

    .. py:method:: get_options()

        A sequence of :py:class:`~pyqtdeploy.ComponentOption` instances
        describing the component's configurable options is returned.

        :return: the sequence of option instances.

    .. py:method:: get_pypi_urls(pypi_project):

        This can be called from a re-implementation of
        :py:meth:`~pyqtdeploy.Component.get_archive_urls` to return a sequence
        of URLs (excluding the source archive name) from which the component's
        source archive may be downloaded from a PyPI project.

        :param str pypi_project: the name of the PyPI project.
        :return: the sequence of URLs.

    .. py:method:: get_python_install_path(major, minor)

        The name of the directory containing the root of a Python installation
        on Windows is returned.  It must only be called by a Windows host.

        :param int major: the major version number.
        :param int minor: the major version number.
        :return: the absolute path of the installation directory.

    .. py:method:: get_version_from_file(identifier, filename)

        A file is read and a (stripped) line containing an identifier
        (typically a pre-processor macro defining a version number) is
        returned.  it is an error if the identifier could not be found.

        :param str identifer: the identifier to find.
        :param str filename: the name of the file to read.
        :return: the stripped line containing the identifier.

    .. py:method:: get_versioned_file(package)

        .. versionadded:: 3.3.0

        A resource package is searched for a file with a version number
        embedded in the name.  The name of the most appropriate file for the
        version of the component is returned or ``None`` if there wasn't one.
        The format of the name must be ``name-version[.extension]`` where the
        optional ``extension`` must be one of ``.py``, ``.h``, ``.c`` or
        ``.cpp``.

        :param module package: the package to search.
        :return: the name of the file or ``None``.

    .. py:attribute:: host_dir

        The name of the directory where components built for the host
        architecture should be installed.

    .. py:method:: host_exe(name)

        A generic executable name is converted to a host-specific version.

        :param str name: the generic name.
        :return: the host-specific name.

    .. py:attribute:: host_make

        The name of the host :program:`make` executable.

    .. py:attribute:: host_platform_name

        The name of the host platform.

    .. py:attribute:: host_python

        The name of the host :program:`python` executable.  This is only
        implemented by the ``Python`` component plugin.

    .. py:attribute:: host_qmake

        The name of the host :program:`qmake` executable.  This is only
        implemented by the ``Qt`` component plugin.

    .. py:attribute:: host_sip

        The name of the host :program:`sip` executable.  This is only
        implemented by the ``SIP`` component plugin.

    .. py:method:: install()
        :abstractmethod:

        This must be re-implemented to install the component.

    .. py:attribute:: must_install_from_source

        .. deprecated:: 3.2.0
            Use :py:attr:`option_install_from_source` instead.

        This is set by the component if it must be installed from a source
        archive.

    .. py:method:: open_file(name)

        An existing text file is opened and its file object returned.  Any
        errors are handled automatically.

        :param str name: the name of the file.
        :return: the file object of the opened file.

    .. py:attribute:: option_install_from_source

        .. versionadded:: 3.2.0

        This is set by the component if it supports the ``install_from_source``
        component option.

    .. py:method:: parse_version_number(version_nr)
        :staticmethod:

        A version number is converted to a :class:`~pyqtdeploy.VersionNumber`
        instance.  It may be a string, an encoded integer or a tuple.

        :param name: the version number to parse.
        :type name: str, int, or tuple
        :return: the version number.

    .. py:method:: patch_file(name, patcher)

        Patch a file.

        :param str name: the name of the file to patch
        :param callable patcher: invoked for each line of the file and passed
            the line and a file object to which the (possibly) modified line
            should be written to.

    .. py:attribute:: preinstalls

        The list of components that this component is dependent on.

    .. py:method:: progress(message)

        A progress message is displayed to the user.  It will be suppressed if
        the :option:`--quiet <pyqtdeploy-sysroot --quiet>` option was
        specified.

        :param str message: the message.

    .. py:attribute:: provides

        The dict of parts, keyed by the name of the part, provided by this
        component.

    .. py:method:: run(*args, capture=False)

        An external command is run.  The command's stdout can be optionally
        captured.

        :param \*args: the name of the command and its arguments.
        :param bool capture: ``True`` if the command's stdout should be
            captured and returned.
        :return: the stdout of the command if requested, otherwise ``None``.

    .. py:method:: sdk_configure(platform_name)

        This should be implemented to perform any SDK-specific configuration
        prior to installing the component.

        :param str platform_name: the target platform name.

    .. py:method:: sdk_deconfigure(platform_name)

        This should be implemented to remove any SDK-specific configuration
        after to installing the component.

        :param str platform_name: the target platform name.

    .. py:attribute:: sysroot_dir

        The full pathname of the system root directory.

    .. py:attribute:: target_arch_name

        The name of the target architecture.

    .. py:attribute:: target_include_dir

        The name of the directory where header files built for the target
        architecture should be installed.

    .. py:attribute:: target_lib_dir

        The name of the directory where libraries built for the target
        architecture should be installed.

    .. py:attribute:: target_platform_name

        The name of the target platform.

    .. py:attribute:: target_py_include_dir

        The pathname of the directory containing the target Python header
        files.  This is only implemented by the ``Python`` component plugin.

    .. py:attribute:: target_py_lib

        The name of the target Python library.  This is only implemented by the
        ``Python`` component plugin.

    .. py:attribute:: target_sip_dir

        The pathname of the directory containing the target ``.sip`` files.
        This is only implemented by the ``SIP`` component plugin.

    .. py:attribute:: target_sitepackages_dir

        The pathname of the target Python ``site-packages`` directory.  This is
        only implemented by the ``Python`` component plugin.

    .. py:attribute:: target_src_dir

        The name of the directory where source files can be found.  Note that
        these are sources left by components for the use of other components
        and not the sources used to build a component.

    .. py:method:: unpack_archive(archive, chdir=True)

        A source archive is unpacked in the current directory and the name of
        the archive directory (not its pathname) is returned.

        :param str archive: the pathname of the source archive.
        :param bool chdir: ``True`` if the current directory is changed to be
            the archive directory.
        :return: the name of the archive directory.

    .. py:method:: unpack_wheel(wheel_path)

        .. versionadded:: 3.2.0

        A wheel is unpacked in the target Python installation's
        ``site-packages`` directory.

        :param str wheel_path: the pathname of the wheel file.

    .. py:method:: unsupported(detail=None)

        Issue an error message that the version of the component is
        unsupported.

        :param str detail: additional detail to append to the message.

    .. py:method:: untested()

        Issue a warning message that the version of the component is untested.

    .. py:method:: verify()

        This can be re-implemented to verify the component.  A component
        will always be verified even if it does not get installed.  The plugin
        should check that everything is available (e.g. other components,
        external tools) using the specified versions for a successful
        installation.

        .. versionadded:: 3.2.0

        If the version number is optional for the component and it has been
        omitted then the ``version`` attribute will be ``None``.  In this case
        the component must determine the version number and set the ``version``
        attribute accordingly.

    .. py:method:: verbose(message)

        A verbose progress message is displayed to the user.  It will be
        suppressed unless the
        :option:`--verbose <pyqtdeploy-sysroot --verbose>` option was
        specified.

        :param str message: the message.

    .. py:attribute:: verbose_enabled

        This is set if the :option:`--verbose <pyqtdeploy-sysroot --verbose>`
        option was specified.

    .. py:attribute:: version_is_optional

        .. versionadded:: 3.2.0

        This is set by the component if the version number specified in the
        sysroot specification file is optional.

    .. py:method:: warning(message)

        A warning progress message is displayed to the user.

        :param str message: the message.


.. py:class:: ComponentOption(name, type=str, required=False, default=None, values=None, help='')

    This class implements an option used to configure the component.  An option
    can be specified as an attribute of the component's object in the sysroot
    specification file.  An instance of the component plugin will contain an
    attribute for each option whose value is that specified in the sysroot
    specification file (or an appropriate default if it was omitted).

    :param str name: the name of the option.
    :param type: the type of a value of the option.
    :type type: bool, int, list or str
    :param bool required: ``True`` if a value for the option is required.
    :param default: the default value of the option.
    :param values: the possible values of the option.
    :param str help: the help text displayed by the
        :option:`--options <pyqtdeploy-sysroot --options>` option of
        :program:`pyqtdeploy-sysroot`.


.. py:class:: VersionNumber

    This class encapsulates a version number in the form ``M[.m[.p]][suffix]``
    where ``M`` is an integer major version number, ``m`` is an optional
    integer minor version number, ``p`` is an optional integer patch version
    number and ``suffix`` is an optional string suffix.

    Instances may be compared with other instances, integers or tuples to
    determine equality or relative chronology.  An integer is interpreted as a
    major version number.  A tuple may have between one and four elements and
    the number of elements determines the precision of the comparison.  For
    example, if a 2-tuple is specified then only the major and minor version
    numbers are considered and the patch version numbers and suffixes are
    ignored.

    .. py:method:: __str__()

        Convert the version number to a user friendly representation.

        :return: the version number as a string.

    .. py:attribute:: major

        The major version number.

    .. py:attribute:: minor

        The minor version number.

    .. py:attribute:: patch

        The patch version number.

    .. py:attribute:: suffix

        The suffix.


Defining Component Parts
........................

The following classes are used to define the different types of part that a
component can provide.

A part is provided by a range of versions of the component.  The optional
``min_version`` is the minimum version of the component that provides the part.
The optional ``max_version`` is the maximum version of the component that
provides the part.  The optional ``version`` can be used to specify an exact
version of the component that provides the part and is the equivalent of
specifying the same value for both ``min_version`` and ``max_version``.  A
version can be specified as either an integer major version number, a 2-tuple
of major and minor version numbers or a 3-tuple of major, minor and patch
version numbers.

Several attributes of different parts are described as sequences of *scoped
values*.  A scoped value is a *scope* and a *value* separated by ``#``.  A
scope defines one or more targets.  If the current target is defined by the
scope then the value is used, otherwise it is ignored.  A scope may be one or
more architecture or platform names separated by ``|`` meaning that the scope
defines all the the specified architectures or platforms.  An individual name
may be preceded by ``!`` which excludes the name from the scope.  For example
``ios|macos`` defines the value for the iOS and macOS platforms and ``!win-32``
defines the value for all targets except for 32-bit Windows.

Some parts may be dependent on other parts, possibly parts provided by
different components.  A dependency may be specified as a component name and a
part name separated by ``:``.  If the component name is omitted then the
current component is assumed.


.. py:class:: ComponentLibrary(min_version=None, version=None, max_version=None, target='', defines=None, libs=None, includepath=None, bundle_shared_libs=False)

    This class encapsulates a library that is usually a dependency of an
    extension module.

    :param min_version: the minimum version of the component providing the
        part.
    :type min_version: int, 2-tuple or 3-tuple
    :param version: the exact version of the component providing the part.
    :type version: int, 2-tuple or 3-tuple
    :param max_version: the maximum version of the component providing the
        part.
    :type max_version: int, 2-tuple or 3-tuple
    :param str target: the target platform for which the part is provided.
    :param sequence defines: the scoped pre-processor macros to be added to the
        ``DEFINES`` :program:`qmake` variable.
    :param sequence libs: the scoped library names to be added to the ``LIBS``
        :program:`qmake` variable.
    :param sequence includepath: the scoped directory names to be added to the
        ``INCLUDEPATH`` :program:`qmake` variable.
    :param bool bundle_shared_libs: ``True`` if the libraries are shared and
        need to be bundled with the application.  Current this only applies to
        Android and Windows targets.  In the case of Windows the component's
        DLLs are copied to the same directory as the final executable so that
        it will run in situ, however it is up to the developer to ensure that
        the DLLs are included with the executable when the application is
        actually deployed.


.. py:class:: DataFile(name, min_version=None, version=None, max_version=None, target='')

    This class encapsulates a data file.

    :param str name: the name of the file.
    :param min_version: the minimum version of the component providing the
        part.
    :type min_version: int, 2-tuple or 3-tuple
    :param version: the exact version of the component providing the part.
    :type version: int, 2-tuple or 3-tuple
    :param max_version: the maximum version of the component providing the
        part.
    :type max_version: int, 2-tuple or 3-tuple
    :param str target: the target platform for which the part is provided.


.. py:class:: ExtensionModule(min_version=None, version=None, max_version=None, target='', min_android_api=None, deps=(), defines=None, libs=None, includepath=None, source=None, qmake_config=None, qmake_cpp11=False, qmake_qt=None)

    This class encapsulates an extension module.

    :param min_version: the minimum version of the component providing the
        part.
    :type min_version: int, 2-tuple or 3-tuple
    :param version: the exact version of the component providing the part.
    :type version: int, 2-tuple or 3-tuple
    :param max_version: the maximum version of the component providing the
        part.
    :type max_version: int, 2-tuple or 3-tuple
    :param str target: the target platform for which the part is provided.
    :param int min_android_api: the minimum Android API level required.
    :param sequence deps: the scoped names of other parts that this part is
        dependent on.
    :param sequence defines: the scoped pre-processor macros to be added to the
        ``DEFINES`` :program:`qmake` variable.
    :param sequence libs: the scoped library names to be added to the ``LIBS``
        :program:`qmake` variable.
    :param sequence includepath: the scoped directory names to be added to the
        ``INCLUDEPATH`` :program:`qmake` variable.
    :param source: the name of the source file(s) of the extension module.
    :type source: str or sequence
    :param qmake_config: the value(s) to be added to the ``CONFIG``
        :program:`qmake` variable.
    :type qmake_config: str or sequence
    :param bool qmake_cpp11: ``True`` if the extension module requires support
        for C++11.
    :param qmake_qt: the value(s) to be added to the ``QT`` :program:`qmake`
        variable.
    :type qmake_qt: str or sequence


.. py:class:: PythonModule(min_version=None, version=None, max_version=None, target='', min_android_api=None, deps=())

    This class encapsulates a Python module (i.e. a single ``.py`` file).

    :param min_version: the minimum version of the component providing the
        part.
    :type min_version: int, 2-tuple or 3-tuple
    :param version: the exact version of the component providing the part.
    :type version: int, 2-tuple or 3-tuple
    :param max_version: the maximum version of the component providing the
        part.
    :type max_version: int, 2-tuple or 3-tuple
    :param str target: the target platform for which the part is provided.
    :param int min_android_api: the minimum Android API level required.
    :param sequence deps: the scoped names of other parts that this part is
        dependent on.


.. py:class:: PythonPackage(min_version=None, version=None, max_version=None, target='', min_android_api=None, deps=(), exclusions=())

    This class encapsulates a Python package (i.e. a directory containing an
    ``__init__.py`` file and other ``.py`` files).

    :param min_version: the minimum version of the component providing the
        part.
    :type min_version: int, 2-tuple or 3-tuple
    :param version: the exact version of the component providing the part.
    :type version: int, 2-tuple or 3-tuple
    :param max_version: the maximum version of the component providing the
        part.
    :type max_version: int, 2-tuple or 3-tuple
    :param str target: the target platform for which the part is provided.
    :param int min_android_api: the minimum Android API level required.
    :param sequence deps: the scoped names of other parts that this part is
        dependent on.
    :param sequence exclusions: the names of any files or directories, relative
        to the package, that should be excluded.
