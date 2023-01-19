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


from importlib import resources

from .user_exception import UserException
from .version_number import VersionNumber


def create_file(file_name):
    """ Create a text file and return the file object.  file_name is the name
    of the file.
    """

    try:
        return open(file_name, 'wt', encoding='UTF-8')
    except Exception as e:
        raise UserException("unable to create file {0}".format(file_name),
                str(e))


def get_versioned_file(package, component):
    """ Return the name of a file in a package appropriate for a component or
    None if there wasn't one.
    """

    candidate = None
    candidate_version = None

    for fn in resources.contents(package):
        if fn.startswith('__'):
            continue

        # There must be one '-' separator.
        name, version = fn.rsplit('-', maxsplit=1)

        for ext in ('.py', '.h', '.c', '.cpp'):
            if version.endswith(ext):
                version = version[:-len(ext)]
                break

        try:
            version = VersionNumber.parse_version_number(version)
        except UserException:
            continue

        if version > component.version:
            # This is for a later version so we can ignore it.
            continue

        if candidate is None or candidate_version < version:
            # This is a better candidate than we have so far.
            candidate = fn
            candidate_version = version

    return candidate


def open_file(file_name):
    """ Open a text file and return the file object.  file_name is the name of
    the file.
    """

    try:
        return open(file_name, 'rt')
    except Exception as e:
        raise UserException("unable to open file {0}".format(file_name),
                str(e))
