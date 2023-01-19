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


class Config:
    """ Encapsulate a configuration value defined in pyconfig.h. """

    def __init__(self, name, py_major=0, default=None, android_api=1,
            **targets):
        """ Define the value allowing target-specific overrides. """

        self.name = name
        self.py_major = py_major
        self._default = default
        self._android_api = android_api
        self._targets = targets

    def value(self, component):
        """ Get the value for a target architecture.  A value of None means the
        configuration value is omitted.
        """

        # Convert the target architecture and platform to valid Python names.
        arch_name = component.target_arch_name.replace('-', '_')
        plat_name = component.target_platform_name

        # Return None if the targetted Android version is earlier than the one
        # for which the value is defined.
        if plat_name == 'android' and component.android_api < self._android_api:
            return None

        # Try the architecture.
        try:
            value = self._targets[arch_name]
        except KeyError:
            # Try the platform.
            try:
                value = self._targets[plat_name]
            except KeyError:
                # Use the default.
                value = self._default

        return value


# The configuration values for all supported versions of Python.  Only those
# that are set for at least one supported platform are specified.
pyconfig = (
    # The normal alignment of `long', in bytes.
    Config('ALIGNOF_LONG', default=8),

    # The normal alignment of `size_t', in bytes.
    Config('ALIGNOF_SIZE_T', default=8),

    # Define if C doubles are 64-bit IEEE 754 binary format, stored with the
    # least significant byte first
    Config('DOUBLE_IS_LITTLE_ENDIAN_IEEE754', ios=1, linux=1, macos=1),

    # Define if --enable-ipv6 is specified
    Config('ENABLE_IPV6', default=1),

    # Define to 1 if you have the 'accept' function.
    Config('HAVE_ACCEPT', default=1),

    # Define to 1 if you have the 'accept4' function.
    Config('HAVE_ACCEPT4', android=1, android_api=21, linux=1),

    # Define to 1 if you have the 'acosh' function.
    Config('HAVE_ACOSH', default=1),

    # struct addrinfo (netdb.h)
    Config('HAVE_ADDRINFO', default=1),

    # Define to 1 if you have the 'alarm' function.
    Config('HAVE_ALARM', default=1),

    # Define to 1 if you have the <alloca.h> header file.
    Config('HAVE_ALLOCA_H', default=1),

    # Define to 1 if you have the 'asinh' function.
    Config('HAVE_ASINH', default=1),

    # Define to 1 if you have the <asm/types.h> header file.
    Config('HAVE_ASM_TYPES_H', android=1, linux=1),

    # Define to 1 if you have the 'atanh' function.
    Config('HAVE_ATANH', default=1),

    # Define to 1 if you have the 'bind' function.
    Config('HAVE_BIND', default=1),

    # Define to 1 if you have the 'bind_textdomain_codeset' function.
    Config('HAVE_BIND_TEXTDOMAIN_CODESET', linux=1),

    # Define to 1 if your sem_getvalue is broken.
    Config('HAVE_BROKEN_SEM_GETVALUE', android=1, ios=1, macos=1),

    # Define if you have builtin '__atomic_load_n' and '__atomic_store_n'
    # functions.
    Config('HAVE_BUILTIN_ATOMIC', default=1),

    # Define to 1 if you have the 'chflags' function.
    Config('HAVE_CHFLAGS', ios=1, macos=1),

    # Define to 1 if you have the 'chmod' function.
    Config('HAVE_CHMOD', default=1),

    # Define to 1 if you have the 'chown' function.
    Config('HAVE_CHOWN', default=1),

    # Define if you have the 'chroot' function.
    Config('HAVE_CHROOT', default=1),

    # Define to 1 if you have the 'clock' function.
    Config('HAVE_CLOCK', default=1),

    # Define to 1 if you have the 'clock_getres' function.
    Config('HAVE_CLOCK_GETRES', default=1),

    # Define to 1 if you have the 'clock_gettime' function.
    Config('HAVE_CLOCK_GETTIME', default=1),

    # Define to 1 if you have the 'clock_nanosleep' function.
    Config('HAVE_CLOCK_NANOSLEEP', linux=1),

    # Define to 1 if you have the 'clock_settime' function.
    Config('HAVE_CLOCK_SETTIME', default=1, ios=None),

    # Define if the C compiler supports computed gotos.
    Config('HAVE_COMPUTED_GOTOS', default=1),

    # Define to 1 if you have the 'confstr' function.
    Config('HAVE_CONFSTR', default=1, android=None),

    # Define to 1 if you have the 'connect' function.
    Config('HAVE_CONNECT', default=1),

    # Define to 1 if you have the 'copysign' function.
    Config('HAVE_COPYSIGN', default=1),

    # Define to 1 if you have the 'copy_file_range' function.
    Config('HAVE_COPY_FILE_RANGE', linux=1),

    # Define to 1 if you have the <crypt.h> header file.
    Config('HAVE_CRYPT_H', linux=1),

    # Define if you have the crypt_r() function.
    Config('HAVE_CRYPT_R', linux=1),

    # Define to 1 if you have the 'ctermid' function.
    Config('HAVE_CTERMID', default=1, android=None),

    # Define if you have the 'ctermid_r' function.
    Config('HAVE_CTERMID_R', ios=1, macos=1),

    # Define if you have the 'filter' function.
    Config('HAVE_CURSES_FILTER', default=1, android=None),

    # Define to 1 if you have the <curses.h> header file.
    Config('HAVE_CURSES_H', default=1, android=None),

    # Define if you have the 'has_key' function.
    Config('HAVE_CURSES_HAS_KEY', default=1, android=None),

    # Define if you have the 'immedok' function.
    Config('HAVE_CURSES_IMMEDOK', default=1, android=None),

    # Define if you have the 'is_pad' function or macro.
    Config('HAVE_CURSES_IS_PAD', linux=1),

    # Define if you have the 'is_term_resized' function.
    Config('HAVE_CURSES_IS_TERM_RESIZED', default=1, android=None),

    # Define if you have the 'resizeterm' function.
    Config('HAVE_CURSES_RESIZETERM', default=1, android=None),

    # Define if you have the 'resize_term' function.
    Config('HAVE_CURSES_RESIZE_TERM', default=1, android=None),

    # Define if you have the 'syncok' function.
    Config('HAVE_CURSES_SYNCOK', default=1, android=None),

    # Define if you have the 'typeahead' function.
    Config('HAVE_CURSES_TYPEAHEAD', default=1, android=None),

    # Define if you have the 'use_env' function.
    Config('HAVE_CURSES_USE_ENV', default=1, android=None),

    # Define if you have the 'wchgat' function.
    Config('HAVE_CURSES_WCHGAT', default=1, android=None),

    # Define to 1 if you have the declaration of 'isfinite'.
    Config('HAVE_DECL_ISFINITE', default=1),

    # Define to 1 if you have the declaration of 'isinf'.
    Config('HAVE_DECL_ISINF', default=1),

    # Define to 1 if you have the declaration of 'isnan'.
    Config('HAVE_DECL_ISNAN', default=1),

	# Define to 1 if you have the declaration of 'RTLD_DEEPBIND'.
    Config('HAVE_DECL_RTLD_DEEPBIND', linux=1),

	# Define to 1 if you have the declaration of 'RTLD_GLOBAL'.
    Config('HAVE_DECL_RTLD_GLOBAL', default=1),

	# Define to 1 if you have the declaration of 'RTLD_LAZY'.
    Config('HAVE_DECL_RTLD_LAZY', default=1),

	# Define to 1 if you have the declaration of 'RTLD_LOCAL'.
    Config('HAVE_DECL_RTLD_LOCAL', default=1),

	# Define to 1 if you have the declaration of 'RTLD_MEMBER'.
    Config('HAVE_DECL_RTLD_MEMBER'),

	# Define to 1 if you have the declaration of 'RTLD_NODELETE'.
    Config('HAVE_DECL_RTLD_NODELETE', default=1, android=None),

	# Define to 1 if you have the declaration of 'RTLD_NOLOAD'.
    Config('HAVE_DECL_RTLD_NOLOAD', default=1),

	# Define to 1 if you have the declaration of 'RTLD_NOW'.
    Config('HAVE_DECL_RTLD_NOW', default=1),

    # Define to 1 if you have the device macros.
    Config('HAVE_DEVICE_MACROS', default=1),

    # Define to 1 if you have the /dev/ptmx device file.
    Config('HAVE_DEV_PTMX', default=1),

    # Define to 1 if the dirent structure has a d_type field.
    Config('HAVE_DIRENT_D_TYPE', default=1),

    # Define to 1 if you have the <dirent.h> header file, and it defines 'DIR'.
    Config('HAVE_DIRENT_H', default=1),

    # Define if you have the 'dirfd' function or macro.
    Config('HAVE_DIRFD', default=1),

    # Define to 1 if you have the <dlfcn.h> header file.
    Config('HAVE_DLFCN_H', default=1),

    # Define to 1 if you have the 'dlopen' function.
    Config('HAVE_DLOPEN', default=1),

    # Define to 1 if you have the 'dup' function.
    Config('HAVE_DUP', default=1),

    # Define to 1 if you have the 'dup2' function.
    Config('HAVE_DUP2', default=1),

    # Define to 1 if you have the 'dup3' function.
    Config('HAVE_DUP3', linux=1),

    # Define if you have the '_dyld_shared_cache_contains_path' function.
    Config('HAVE_DYLD_SHARED_CACHE_CONTAINS_PATH', ios=1, macos=1),

    # Define to 1 if you have the <endian.h> header file.
    Config('HAVE_ENDIAN_H', android=1, linux=1),

    # Define if you have the 'epoll' functions.
    Config('HAVE_EPOLL', android=1, linux=1),

    # Define if you have the 'epoll_create1' function.
    Config('HAVE_EPOLL_CREATE1', linux=1),

    # Define to 1 if you have the 'erf' function.
    Config('HAVE_ERF', default=1),

    # Define to 1 if you have the 'erfc' function.
    Config('HAVE_ERFC', default=1),

    # Define to 1 if you have the <errno.h> header file.
    Config('HAVE_ERRNO_H', default=1),

    # Define to 1 if you have the 'eventfd' function.
    Config('HAVE_EVENTFD', linux=1),

    # Define to 1 if you have the 'execv' function.
    Config('HAVE_EXECV', default=1),

    # Define to 1 if you have the 'explicit_bzero' function.
    Config('HAVE_EXPLICIT_BZERO', linux=1),

    # Define to 1 if you have the 'expm1' function.
    Config('HAVE_EXPM1', default=1),

    # Define to 1 if you have the 'faccessat' function.
    Config('HAVE_FACCESSAT', ios=1, linux=1, macos=1),

    # Define if you have the 'fchdir' function.
    Config('HAVE_FCHDIR', default=1),

    # Define to 1 if you have the 'fchmod' function.
    Config('HAVE_FCHMOD', default=1),

    # Define to 1 if you have the 'fchmodat' function.
    Config('HAVE_FCHMODAT', default=1),

    # Define to 1 if you have the 'fchown' function.
    Config('HAVE_FCHOWN', default=1),

    # Define to 1 if you have the 'fchownat' function.
    Config('HAVE_FCHOWNAT', default=1),

    # Define to 1 if you have the <fcntl.h> header file.
    Config('HAVE_FCNTL_H', default=1),

    # Define if you have the 'fdatasync' function.
    Config('HAVE_FDATASYNC', android=1, linux=1),

    # Define to 1 if you have the 'fdopendir' function.
    Config('HAVE_FDOPENDIR', default=1),

    # Define to 1 if you have the 'fexecve' function.
    Config('HAVE_FEXECVE', linux=1),

    # Define to 1 if you have the 'finite' function.
    Config('HAVE_FINITE', default=1),

    # Define to 1 if you have the 'flock' function.
    Config('HAVE_FLOCK', default=1),

    # Define to 1 if you have the 'fork' function.
    Config('HAVE_FORK', default=1),

    # Define to 1 if you have the 'fork1' function.
    #Config('HAVE_FORK1', default=1),

    # Define to 1 if you have the 'forkpty' function.
    Config('HAVE_FORKPTY', default=1, android=None),

    # Define to 1 if you have the 'fpathconf' function.
    Config('HAVE_FPATHCONF', default=1),

    # Define to 1 if you have the 'fseeko' function.
    Config('HAVE_FSEEKO', default=1),

    # Define to 1 if you have the 'fstatat' function.
    Config('HAVE_FSTATAT', default=1),

    # Define to 1 if you have the 'fstatvfs' function.
    Config('HAVE_FSTATVFS', default=1),

    # Define if you have the 'fsync' function.
    Config('HAVE_FSYNC', default=1),

    # Define to 1 if you have the 'ftello' function.
    Config('HAVE_FTELLO', default=1),

    # Define to 1 if you have the 'ftime' function.
    Config('HAVE_FTIME', default=1, android=None),

    # Define to 1 if you have the 'ftruncate' function.
    Config('HAVE_FTRUNCATE', default=1),

    # Define to 1 if you have the 'futimens' function.
    Config('HAVE_FUTIMENS', ios=1, linux=1, macos=1),

    # Define to 1 if you have the 'futimes' function.
    Config('HAVE_FUTIMES', default=1, android=None),

    # Define to 1 if you have the 'futimesat' function.
    Config('HAVE_FUTIMESAT', linux=1),

    # Define to 1 if you have the 'gai_strerror' function.
    Config('HAVE_GAI_STRERROR', default=1),

    # Define to 1 if you have the 'gamma' function.
    Config('HAVE_GAMMA', default=1),

    # Define if we can use x64 gcc inline assembler
    Config('HAVE_GCC_ASM_FOR_X64', android_64=1, ios_64=1, linux_64=1,
            macos_64=1),

    # Define if we can use gcc inline assembler to get and set x87 control word
    Config('HAVE_GCC_ASM_FOR_X87', default=1, android=None),

    # Define if your compiler provides __uint128_t.
    Config('HAVE_GCC_UINT128_T', android_64=1, ios_64=1, linux_64=1,
            macos_64=1),

    # Define if you have the getaddrinfo function.
    Config('HAVE_GETADDRINFO', default=1),

    # Define this if you have flockfile(), getc_unlocked(), and funlockfile()
    Config('HAVE_GETC_UNLOCKED', default=1),

    # Define this if you have the 'getegid' function.
    Config('HAVE_GETEGID', default=1),

    # Define this if you have the 'getentropy' function.
    Config('HAVE_GETENTROPY', default=1, android_api=28),

    # Define this if you have the 'geteuid' function.
    Config('HAVE_GETEUID', default=1),

    # Define this if you have the 'getgid' function.
    Config('HAVE_GETGID', default=1),

    # Define to 1 if you have the 'getgrgid' function.
    Config('HAVE_GETGRGID', default=1),

    # Define to 1 if you have the 'getgrgid_r' function.
    Config('HAVE_GETGRGID_R', default=1),

    # Define to 1 if you have the 'getgrnam_r' function.
    Config('HAVE_GETGRNAM_R', default=1),

    # Define to 1 if you have the 'getgrouplist' function.
    Config('HAVE_GETGROUPLIST', default=1),

    # Define to 1 if you have the 'getgroups' function.
    Config('HAVE_GETGROUPS', default=1),

    # Define to 1 if you have the 'gethostbyaddr' function.
    Config('HAVE_GETHOSTBYADDR', ios=1, linux=1, macos=1),

    # Define to 1 if you have the 'gethostbyname' function.
    Config('HAVE_GETHOSTBYNAME', ios=1, linux=1, macos=1),

    # Define this if you have some version of gethostbyname_r()
    Config('HAVE_GETHOSTBYNAME_R', android=1, linux=1),

    # Define this if you have the 6-arg version of gethostbyname_r().
    Config('HAVE_GETHOSTBYNAME_R_6_ARG', android=1, linux=1),

    # Define to 1 if you have the 'gethostname' function.
    Config('HAVE_GETHOSTNAME', default=1),

    # Define to 1 if you have the 'getitimer' function.
    Config('HAVE_GETITIMER', default=1),

    # Define to 1 if you have the 'getloadavg' function.
    Config('HAVE_GETLOADAVG', default=1, android=None),

    # Define to 1 if you have the 'getlogin' function.
    Config('HAVE_GETLOGIN', default=1),

    # Define to 1 if you have the 'getnameinfo' function.
    Config('HAVE_GETNAMEINFO', default=1),

    # Define if you have the 'getpagesize' function.
    Config('HAVE_GETPAGESIZE', android=1, linux=1),

    # Define to 1 if you have the 'getpeername' function.
    Config('HAVE_GETPEERNAME', default=1),

    # Define to 1 if you have the 'getpgid' function.
    Config('HAVE_GETPGID', default=1),

    # Define to 1 if you have the 'getpgrp' function.
    Config('HAVE_GETPGRP', default=1),

    # Define to 1 if you have the 'getpid' function.
    Config('HAVE_GETPID', default=1),

    # Define to 1 if you have the 'getppid' function.
    Config('HAVE_GETPPID', default=1),

    # Define to 1 if you have the 'getpriority' function.
    Config('HAVE_GETPRIORITY', default=1),

    # Define to 1 if you have the 'getprotobyname' function.
    Config('HAVE_GETPROTOBYNAME', default=1),

    # Define to 1 if you have the 'getpwent' function.
    Config('HAVE_GETPWENT', default=1, android_api=26),

    # Define to 1 if you have the 'getpwnam_r' function.
    Config('HAVE_GETPWNAM_R', default=1, android_api=26),

    # Define to 1 if you have the 'getpwuid' function.
    Config('HAVE_GETPWUID', default=1, android_api=26),

    # Define to 1 if you have the 'getpwuid_r' function.
    Config('HAVE_GETPWUID_R', default=1, android_api=26),

    # Define to 1 if the getrandom() function is available.
    Config('HAVE_GETRANDOM', linux=1),

    # Define to 1 if the Linux getrandom() syscall is available.
    Config('HAVE_GETRANDOM_SYSCALL', linux=1),

    # Define to 1 if you have the 'getresgid' function.
    Config('HAVE_GETRESGID', android=1, linux=1),

    # Define to 1 if you have the 'getresuid' function.
    Config('HAVE_GETRESUID', android=1, linux=1),

    # Define to 1 if you have the 'getrusage' function.
    Config('HAVE_GETRUSAGE', default=1),

    # Define to 1 if you have the 'getservbyname' function.
    Config('HAVE_GETSERVBYNAME', default=1),

    # Define to 1 if you have the 'getservbyport' function.
    Config('HAVE_GETSERVBYPORT', default=1),

    # Define to 1 if you have the 'getsid' function.
    Config('HAVE_GETSID', default=1, android_api=21),

    # Define to 1 if you have the 'getsockname' function.
    Config('HAVE_GETSOCKNAME', default=1),

    # Define to 1 if you have the 'getspent' function.
    Config('HAVE_GETSPENT', android=1, linux=1),

    # Define to 1 if you have the 'getspnam' function.
    Config('HAVE_GETSPNAM', android=1, linux=1),

    # Define to 1 if you have the 'getuid' function.
    Config('HAVE_GETUID', default=1),

    # Define to 1 if you have the 'gettimeofday' function.
    Config('HAVE_GETTIMEOFDAY', default=1),

    # Define to 1 if you have the 'getwd' function.
    Config('HAVE_GETWD', default=1),

    # Define to 1 if you have the <grp.h> header file.
    Config('HAVE_GRP_H', default=1),

    # Define if you have the 'hstrerror' function.
    Config('HAVE_HSTRERROR', default=1),

    # Define this if you have le64toh()
    Config('HAVE_HTOLE64', android=1, linux=1),

    # Define to 1 if you have the 'hypot' function.
    Config('HAVE_HYPOT', default=1),

    # Define to 1 if you have the 'if_nameindex' function.
    Config('HAVE_IF_NAMEINDEX', default=1, android=None),

    # Define if you have the 'inet_aton' function.
    Config('HAVE_INET_ATON', default=1),

    # Define if you have the 'inet_ntoa' function.
    Config('HAVE_INET_NTOA', default=1),

    # Define if you have the 'inet_pton' function.
    Config('HAVE_INET_PTON', default=1),

    # Define to 1 if you have the 'initgroups' function.
    Config('HAVE_INITGROUPS', default=1),

    # Define to 1 if you have the <inttypes.h> header file.
    Config('HAVE_INTTYPES_H', default=1),

    # Define to 1 if you have the 'kill' function.
    Config('HAVE_KILL', default=1),

    # Define to 1 if you have the 'killpg' function.
    Config('HAVE_KILLPG', default=1),

    # Define if you have the 'kqueue' functions.
    Config('HAVE_KQUEUE', ios=1, macos=1),

    # Define to 1 if you have the <langinfo.h> header file.
    Config('HAVE_LANGINFO_H', default=1, android=None),

    # Defined to enable large file support when an off_t is bigger than a long
    # and long long is available and at least as big as an off_t. You may need
    # to add some flags for configuration and compilation to enable this mode.
    # (For Solaris and Linux, the necessary defines are already defined.),
    Config('HAVE_LARGEFILE_SUPPORT', linux_32=1),

    # Define to 1 if you have the 'lchflags' function.
    Config('HAVE_LCHFLAGS', ios=1, macos=1),

    # Define to 1 if you have the 'lchmod' function.
    Config('HAVE_LCHMOD', ios=1, macos=1),

    # Define to 1 if you have the 'lchown' function.
    Config('HAVE_LCHOWN', default=1),

    # Define to 1 if you have the 'lgamma' function.
    Config('HAVE_LGAMMA', default=1),

    # Define to 1 if you have the 'dl' library (-ldl).
    Config('HAVE_LIBDL', default=1),

    # Define to 1 if you have the <libintl.h> header file.
    Config('HAVE_LIBINTL_H', linux=1),

    # Define if you have the 'readline' library (-lreadline).
    Config('HAVE_LIBREADLINE', default=1, android=None),

    # Define if you have libuuid.
    Config('HAVE_LIBUUID', linux=1),

    # Define if you have the 'link' function.
    Config('HAVE_LINK', default=1),

    # Define to 1 if you have the 'linkat' function.
    Config('HAVE_LINKAT', ios=1, linux=1, macos=1),

    # Define to 1 if you have the <linux/auxvec.h> header file.
    Config('HAVE_LINUX_AUXVEC_H', linux=1),

    # Define to 1 if you have the <linux/can/bcm.h> header file.
    Config('HAVE_LINUX_CAN_BCM_H', android=1, linux=1),

    # Define to 1 if you have the <linux/can.h> header file.
    Config('HAVE_LINUX_CAN_H', android=1, linux=1),

    # Define to 1 if you have the <linux/can/j1939.h> header file.
    Config('HAVE_LINUX_CAN_J1939_H', linux=1),

    # Define if compiling using Linux 3.6 or later.
    Config('HAVE_LINUX_CAN_RAW_FD_FRAMES', android=1, linux=1),

    # Define to 1 if you have the <linux/can/raw.h> header file.
    Config('HAVE_LINUX_CAN_RAW_H', android=1, linux=1),

    # Define to 1 if compiling using Linux 4.1 or later.
    Config('HAVE_LINUX_CAN_RAW_JOIN_FILTERS', android=1, linux=1),

    # Define to 1 if you have the <linux/netlink.h> header file.
    Config('HAVE_LINUX_NETLINK_H', android=1, linux=1),

    # Define to 1 if you have the <linux/qrtr.h> header file.
    Config('HAVE_LINUX_QRTR_H', linux=1),

    # Define to 1 if you have the <linux/random.h> header file.
    Config('HAVE_LINUX_RANDOM_H', linux=1),

    # Define to 1 if you have the <linux/soundcard.h> header file.
    Config('HAVE_LINUX_SOUNDCARD_H', linux=1),

    # Define to 1 if you have the <linux/tipc.h> header file.
    Config('HAVE_LINUX_TIPC_H', android=1, linux=1),

    # Define to 1 if you have the <linux/vm_sockets.h> header file.
    Config('HAVE_LINUX_VM_SOCKETS_H', linux=1),

    # Define to 1 if you have the <linux/wait.h> header file.
    Config('HAVE_LINUX_WAIT_H', linux=1),

    # Define to 1 if you have the 'listen' function.
    Config('HAVE_LISTEN', default=1),

    # Define to 1 if you have the 'lockf' function.
    Config('HAVE_LOCKF', ios=1, linux=1, macos=1),

    # Define to 1 if you have the 'log1p' function.
    Config('HAVE_LOG1P', default=1),

    # Define to 1 if you have the 'log2' function.
    Config('HAVE_LOG2', default=1, android_api=18),

    # Define to 1 if you have the 'login_tty' function.
    Config('HAVE_LOGIN_TTY', default=1),

    # Define this if you have the type long double.
    Config('HAVE_LONG_DOUBLE', default=1),

    # Define to 1 if you have the 'lstat' function.
    Config('HAVE_LSTAT', default=1),

    # Define to 1 if you have the 'lutimes' function.
    Config('HAVE_LUTIMES', default=1, android=None),

    # Define this if you have the 'madvise' macro.
    Config('HAVE_MADVISE', default=1),

    # Define this if you have the 'makedev' macro.
    Config('HAVE_MAKEDEV', default=1),

    # Define to 1 if you have the 'mbrtowc' function.
    Config('HAVE_MBRTOWC', default=1, android_api=21),

    # Define to 1 if you have the 'memfd_create' function.
    Config('HAVE_MEMFD_CREATE', linux=1),

    # Define to 1 if you have the <memory.h> header file.
    Config('HAVE_MEMORY_H', default=1),

    # Define to 1 if you have the 'memrchr' function.
    Config('HAVE_MEMRCHR', android=1, linux=1),

    # Define to 1 if you have the 'mkdirat' function.
    Config('HAVE_MKDIRAT', default=1),

    # Define to 1 if you have the 'mkfifo' function.
    Config('HAVE_MKFIFO', default=1),

    # Define to 1 if you have the 'mkfifoat' function.
    Config('HAVE_MKFIFOAT', linux=1),

    # Define to 1 if you have the 'mknod' function.
    Config('HAVE_MKNOD', default=1),

    # Define to 1 if you have the 'mknodat' function.
    Config('HAVE_MKNODAT', linux=1),

    # Define to 1 if you have the 'mktime' function.
    Config('HAVE_MKTIME', default=1),

    # Define to 1 if you have the 'mmap' function.
    Config('HAVE_MMAP', default=1),

    # Define to 1 if you have the 'mremap' function.
    Config('HAVE_MREMAP', android=1, linux=1),

    # Define to 1 if you have the 'nanosleep' function.
    Config('HAVE_NANOSLEEP', default=1),

    # Define to 1 if you have the <ncurses.h> header file.
    Config('HAVE_NCURSES_H', default=1, android=None),

    # Define to 1 if you have the <netpacket/packet.h> header file.
    Config('HAVE_NETPACKET_PACKET_H', android=1, linux=1),

    # Define to 1 if you have the <net/if.h> header file.
    Config('HAVE_NET_IF_H', default=1),

    # Define to 1 if you have the <netdb.h> header file.
    Config('HAVE_NETDB_H', default=1),

    # Define to 1 if you have the <netinet/in.h> header file.
    Config('HAVE_NETINET_IN_H', default=1),

    # Define to 1 if you have the 'nice' function.
    Config('HAVE_NICE', default=1),

    # Define to 1 if you have the 'openat' function.
    Config('HAVE_OPENAT', default=1),

    # Define to 1 if you have the 'opendir' function.
    Config('HAVE_OPENDIR', default=1),

    # Define to 1 if you have the 'openpty' function.
    Config('HAVE_OPENPTY', default=1, android=None),

    # Define to 1 if you have the 'pathconf' function.
    Config('HAVE_PATHCONF', default=1),

    # Define to 1 if you have the 'pause' function.
    Config('HAVE_PAUSE', default=1),

    # Define to 1 if you have the 'pipe' function.
    Config('HAVE_PIPE', default=1),

    # Define to 1 if you have the 'pipe2' function.
    Config('HAVE_PIPE2', android=1, linux=1),

    # Define to 1 if you have the 'poll' function.
    Config('HAVE_POLL', default=1),

    # Define to 1 if you have the <poll.h> header file.
    Config('HAVE_POLL_H', default=1),

    # Define to 1 if you have the 'posix_fadvise' function.
    Config('HAVE_POSIX_FADVISE', linux=1),

    # Define to 1 if you have the 'posix_fallocate' function.
    Config('HAVE_POSIX_FALLOCATE', linux=1),

    # Define to 1 if you have the 'posix_spawn' function.
    Config('HAVE_POSIX_SPAWN', default=1, android_api=28),

    # Define to 1 if you have the 'posix_spawnp' function.
    Config('HAVE_POSIX_SPAWNP', default=1, android_api=28),

    # Define to 1 if you have the 'pread' function.
    Config('HAVE_PREAD', default=1),

    # Define to 1 if you have the 'preadv' function.
    Config('HAVE_PREADV', ios=1, linux=1, macos=1),

    # Define to 1 if you have the 'preadv2' function.
    Config('HAVE_PREADV2', linux=1),

    # Define if you have the 'prlimit' functions.
    Config('HAVE_PRLIMIT', android=1, linux=1),

    # Define if your compiler supports function prototype
    Config('HAVE_PROTOTYPES', default=1),

    # Define to 1 if you have the 'pthread_condattr_setclock' function.
    Config('HAVE_PTHREAD_CONDATTR_SETCLOCK', linux=1),

    # Define to 1 if you have the 'pthread_getcpuclockid' function.
    Config('HAVE_PTHREAD_GETCPUCLOCKID', linux=1),

    # Define to 1 if you have the <pthread.h> header file.
    Config('HAVE_PTHREAD_H', default=1),

    # Define to 1 if you have the 'pthread_kill' function.
    Config('HAVE_PTHREAD_KILL', default=1),

    # Define to 1 if you have the 'pthread_sigmask' function.
    Config('HAVE_PTHREAD_SIGMASK', default=1),

    # Define if platform requires stubbed pthreads support.
    #Config('HAVE_PTHREAD_STUBS', default=0),

    # Define to 1 if you have the <pty.h> header file.
    Config('HAVE_PTY_H', linux=1),

    # Define to 1 if you have the 'putenv' function.
    Config('HAVE_PUTENV', default=1),

    # Define to 1 if you have the 'pwrite' function.
    Config('HAVE_PWRITE', default=1),

    # Define to 1 if you have the 'pwritev' function.
    Config('HAVE_PWRITEV', default=1),

    # Define to 1 if you have the 'pwritev2' function.
    Config('HAVE_PWRITEV2', linux=1),

    # Define to 1 if you have the 'readlink' function.
    Config('HAVE_READLINK', default=1),

    # Define to 1 if you have the 'readlinkat' function.
    Config('HAVE_READLINKAT', default=1),

    # Define to 1 if you have the 'readv' function.
    Config('HAVE_READV', default=1),

    # Define to 1 if you have the 'realpath' function.
    Config('HAVE_REALPATH', default=1),

    # Define to 1 if you have the 'recvfrom' function.
    Config('HAVE_RECVFROM', default=1),

    # Define to 1 if you have the 'renameat' function.
    Config('HAVE_RENAMEAT', default=1),

    # Define if readline supports append_history.
    Config('HAVE_RL_APPEND_HISTORY', linux=1),

    # Define if you can turn off readline's signal handling.
    Config('HAVE_RL_CATCH_SIGNAL', linux=1),

    # Define if you have readline 2.2
    Config('HAVE_RL_COMPLETION_APPEND_CHARACTER', default=1, android=None),

    # Define if you have readline 4.0
    Config('HAVE_RL_COMPLETION_DISPLAY_MATCHES_HOOK', default=1, android=None),

    # Define if you have readline 4.2
    Config('HAVE_RL_COMPLETION_MATCHES', default=1, android=None),

    # Define if you have rl_completion_suppress_append
    Config('HAVE_RL_COMPLETION_SUPPRESS_APPEND', linux=1),

    # Define if you have readline 4.0
    Config('HAVE_RL_PRE_INPUT_HOOK', default=1, android=None),

    # Define if you have readline 4.0
    Config('HAVE_RL_RESIZE_TERMINAL', linux=1, android=None),

    # Define to 1 if you have the 'round' function.
    Config('HAVE_ROUND', default=1),

    # Define to 1 if you have the <rpc/rpc.h> header file.
    Config('HAVE_RPC_RPC_H', default=1),

    # Define to 1 if you have the 'sched_get_priority_max' function.
    Config('HAVE_SCHED_GET_PRIORITY_MAX', default=1),

    # Define to 1 if you have the <sched.h> header file.
    Config('HAVE_SCHED_H', default=1),

    # Define to 1 if you have the 'sched_rr_get_interval' function.
    Config('HAVE_SCHED_RR_GET_INTERVAL', android=1, linux=1),

    # Define to 1 if you have the 'sched_setaffinity' function.
    Config('HAVE_SCHED_SETAFFINITY', android=1, linux=1),

    # Define to 1 if you have the 'sched_setparam' function.
    Config('HAVE_SCHED_SETPARAM', android=1, linux=1),

    # Define to 1 if you have the 'sched_setscheduler' function.
    Config('HAVE_SCHED_SETSCHEDULER', android=1, linux=1),

    # Define to 1 if you have the 'sem_clockwait' function.
    Config('HAVE_SEM_CLOCKWAIT', linux=1),

    # Define to 1 if you have the 'sem_getvalue' function.
    Config('HAVE_SEM_GETVALUE', default=1),

    # Define to 1 if you have the 'sem_open' function.
    Config('HAVE_SEM_OPEN', default=1),

    # Define to 1 if you have the 'sem_timedwait' function.
    Config('HAVE_SEM_TIMEDWAIT', android=1, linux=1),

    # Define to 1 if you have the 'sem_unlink' function.
    Config('HAVE_SEM_UNLINK', default=1),

    # Define to 1 if you have the 'sendfile' function.
    Config('HAVE_SENDFILE', default=1),

    # Define to 1 if you have the 'sendto' function.
    Config('HAVE_SENDTO', default=1),

    # Define to 1 if you have the 'setegid' function.
    Config('HAVE_SETEGID', default=1),

    # Define to 1 if you have the 'seteuid' function.
    Config('HAVE_SETEUID', default=1),

    # Define to 1 if you have the 'setgid' function.
    Config('HAVE_SETGID', default=1),

    # Define if you have the 'setgroups' function.
    Config('HAVE_SETGROUPS', default=1),

    # Define to 1 if you have the 'sethostname' function.
    Config('HAVE_SETHOSTNAME', default=1, android=None),

    # Define to 1 if you have the 'setitimer' function.
    Config('HAVE_SETITIMER', default=1),

    # Define to 1 if you have the <setjmp.h> header file.
    Config('HAVE_SETJMP_H', default=1),

    # Define to 1 if you have the 'setlocale' function.
    Config('HAVE_SETLOCALE', default=1),

    # Define to 1 if you have the 'setpgid' function.
    Config('HAVE_SETPGID', default=1),

    # Define to 1 if you have the 'setpgrp' function.
    Config('HAVE_SETPGRP', default=1),

    # Define to 1 if you have the 'setpriority' function.
    Config('HAVE_SETPRIORITY', default=1),

    # Define to 1 if you have the 'setregid' function.
    Config('HAVE_SETREGID', default=1),

    # Define to 1 if you have the 'setresgid' function.
    Config('HAVE_SETRESGID', android=1, linux=1),

    # Define to 1 if you have the 'setresuid' function.
    Config('HAVE_SETRESUID', android=1, linux=1),

    # Define to 1 if you have the 'setreuid' function.
    Config('HAVE_SETREUID', default=1),

    # Define to 1 if you have the 'setsid' function.
    Config('HAVE_SETSID', default=1),

    # Define to 1 if you have the 'setsockopt' function.
    Config('HAVE_SETSOCKOPT', default=1),

    # Define to 1 if you have the 'setuid' function.
    Config('HAVE_SETUID', default=1),

    # Define to 1 if you have the 'setvbuf' function.
    Config('HAVE_SETVBUF', default=1),

    # Define to 1 if you have the <shadow.h> header file.
    Config('HAVE_SHADOW_H', android=1, linux=1),

    # Define to 1 if you have the 'shm_open' function.
    Config('HAVE_SHM_OPEN', default=1),

    # Define to 1 if you have the 'shm_unlink' function.
    Config('HAVE_SHM_UNLINK', default=1),

    # Define to 1 if you have the 'shutdown' function.
    Config('HAVE_SHUTDOWN', default=1),

    # Define to 1 if you have the 'sigaction' function.
    Config('HAVE_SIGACTION', default=1),

    # Define to 1 if you have the 'sigaltstack' function.
    Config('HAVE_SIGALTSTACK', default=1),

    # Define to 1 if you have the 'sigfillset' function.
    Config('HAVE_SIGFILLSET', default=1),

    # Define to 1 if 'si_band' is a member of 'siginfo_t'.
    Config('HAVE_SIGINFO_T_SI_BAND', default=1),

    # Define to 1 if you have the 'siginterrupt' function.
    Config('HAVE_SIGINTERRUPT', default=1),

    # Define to 1 if you have the <signal.h> header file.
    Config('HAVE_SIGNAL_H', default=1),

    # Define to 1 if you have the 'sigpending' function.
    Config('HAVE_SIGPENDING', default=1),

    # Define to 1 if you have the 'sigrelse' function.
    Config('HAVE_SIGRELSE', default=1),

    # Define to 1 if you have the 'sigtimedwait' function.
    Config('HAVE_SIGTIMEDWAIT', linux=1),

    # Define to 1 if you have the 'sigwait' function.
    Config('HAVE_SIGWAIT', default=1),

    # Define to 1 if you have the 'sigwaitinfo' function.
    Config('HAVE_SIGWAITINFO', linux=1),

    # Define to 1 if you have the 'snprintf' function.
    Config('HAVE_SNPRINTF', default=1),

    # Define to 1 if you have the sockaddr_alg structure.
    Config('HAVE_SOCKADDR_ALG', linux=1),

    # Define if sockaddr has sa_len member
    Config('HAVE_SOCKADDR_SA_LEN', ios=1, macos=1),

    # struct sockaddr_storage (sys/socket.h),
    Config('HAVE_SOCKADDR_STORAGE', default=1),

    # Define if you have the 'socket' function.
    Config('HAVE_SOCKET', default=1),

    # Define if you have the 'socketpair' function.
    Config('HAVE_SOCKETPAIR', default=1),

    # Define to 1 if you have the <spawn.h> header file.
    Config('HAVE_SPAWN_H', default=1),

    # Define to 1 if you have the 'splice' function.
    Config('HAVE_SPLICE', linux=1),

    # Define if your compiler provides ssize_t
    Config('HAVE_SSIZE_T', default=1),

    # Define to 1 if you have the 'statvfs' function.
    Config('HAVE_STATVFS', default=1),

    # Define if you have struct stat.st_mtim.tv_nsec
    Config('HAVE_STAT_TV_NSEC', linux=1),

    # Define if you have struct stat.st_mtimensec
    Config('HAVE_STAT_TV_NSEC2', ios=1, macos=1),

    # Define if your compiler supports variable length function prototypes
    # (e.g.  void fprintf(FILE *, char *, ...);) *and* <stdarg.h>
    Config('HAVE_STDARG_PROTOTYPES', default=1),

    # Define to 1 if you have the <stdint.h> header file.
    Config('HAVE_STDINT_H', default=1),

    # Define to 1 if you have the <stdlib.h> header file.
    Config('HAVE_STDLIB_H', default=1),

    # Define if you have stdatomic.h and atomic_int and _Atomic void* types
    # work.  Note that Android ABI v4.9 has stdatomic.h but Qt uses v4.8.  RHEL
    # v7.2 uses GCC 4.8 but stdatomic.h was added in GCC 4.9.
    Config('HAVE_STD_ATOMIC', ios=1, linux=1, macos=1),

    # Define to 1 if you have the 'strdup' function.
    Config('HAVE_STRDUP', default=1),

    # Define to 1 if you have the 'strftime' function.
    Config('HAVE_STRFTIME', default=1),

    # Define to 1 if you have the <strings.h> header file.
    Config('HAVE_STRINGS_H', default=1),

    # Define to 1 if you have the <string.h> header file.
    Config('HAVE_STRING_H', default=1),

    # Define to 1 if you have the 'strlcpy' function.
    Config('HAVE_STRLCPY', ios=1, macos=1),

    # Define to 1 if you have the 'strsignal' function.
    Config('HAVE_STRSIGNAL', default=1),

    # Define to 1 if 'pw_gecos' is a member of 'struct passwd'.
    Config('HAVE_STRUCT_PASSWD_PW_GECOS', default=1, android=None),

    # Define to 1 if 'pw_passwd' is a member of 'struct passwd'.
    Config('HAVE_STRUCT_PASSWD_PW_PASSWD', default=1),

    # Define to 1 if 'st_birthtime' is a member of 'struct stat'.
    Config('HAVE_STRUCT_STAT_ST_BIRTHTIME', ios=1, macos=1),

    # Define to 1 if 'st_blksize' is a member of 'struct stat'.
    Config('HAVE_STRUCT_STAT_ST_BLKSIZE', default=1),

    # Define to 1 if 'st_blocks' is a member of 'struct stat'.
    Config('HAVE_STRUCT_STAT_ST_BLOCKS', default=1),

    # Define to 1 if 'st_flags' is a member of 'struct stat'.
    Config('HAVE_STRUCT_STAT_ST_FLAGS', ios=1, macos=1),

    # Define to 1 if 'st_gen' is a member of 'struct stat'.
    Config('HAVE_STRUCT_STAT_ST_GEN', ios=1, macos=1),

    # Define to 1 if 'st_rdev' is a member of 'struct stat'.
    Config('HAVE_STRUCT_STAT_ST_RDEV', default=1),

    # Define to 1 if 'tm_zone' is a member of 'struct tm'.
    Config('HAVE_STRUCT_TM_TM_ZONE', default=1),

    # Define if you have the 'symlink' function.
    Config('HAVE_SYMLINK', default=1),

    # Define to 1 if you have the 'symlinkat' function.
    Config('HAVE_SYMLINKAT', default=1),

    # Define to 1 if you have the 'sync' function.
    Config('HAVE_SYNC', default=1),

    # Define to 1 if you have the 'sysconf' function.
    Config('HAVE_SYSCONF', default=1),

    # Define to 1 if you have the <sysexits.h> header file.
    Config('HAVE_SYSEXITS_H', default=1, android=None),

    # Define to 1 if you have the 'system' function.
    Config('HAVE_SYSTEM', default=1, ios=None),

    # Define to 1 if you have the <sys/auxv.h> header file.
    Config('HAVE_SYS_AUXV_H', linux=1),

    # Define to 1 if you have the <sys/epoll.h> header file.
    Config('HAVE_SYS_EPOLL_H', android=1, linux=1),

    # Define to 1 if you have the <sys/eventfd.h> header file.
    Config('HAVE_SYS_EVENTFD_H', linux=1),

    # Define to 1 if you have the <sys/event.h> header file.
    Config('HAVE_SYS_EVENT_H', ios=1, macos=1),

    # Define to 1 if you have the <sys/file.h> header file.
    Config('HAVE_SYS_FILE_H', default=1),

    # Define to 1 if you have the <sys/ioctl.h> header file.
    Config('HAVE_SYS_IOCTL_H', default=1),

    # Define to 1 if you have the <sys/kern_control.h> header file.
    Config('HAVE_SYS_KERN_CONTROL_H', macos=1),

    # Define to 1 if you have the <sys/lock.h> header file.
    Config('HAVE_SYS_LOCK_H', ios=1, macos=1),

    # Define to 1 if you have the <sys/mman.h> header file.
    Config('HAVE_SYS_MMAN_H', default=1),

    # Define to 1 if you have the <sys/param.h> header file.
    Config('HAVE_SYS_PARAM_H', default=1),

    # Define to 1 if you have the <sys/poll.h> header file.
    Config('HAVE_SYS_POLL_H', default=1),

    # Define to 1 if you have the <sys/random.h> header file.
    Config('HAVE_SYS_RANDOM_H', default=1, ios=None, android_api=28),

    # Define to 1 if you have the <sys/resource.h> header file.
    Config('HAVE_SYS_RESOURCE_H', default=1),

    # Define to 1 if you have the <sys/select.h> header file.
    Config('HAVE_SYS_SELECT_H', default=1),

    # Define to 1 if you have the <sys/sendfile.h> header file.
    Config('HAVE_SYS_SENDFILE_H', android=1, linux=1),

    # Define to 1 if you have the <sys/socket.h> header file.
    Config('HAVE_SYS_SOCKET_H', default=1),

    # Define to 1 if you have the <sys/soundcard.h> header file.
    Config('HAVE_SYS_SOUNDCARD_H', linux=1),

    # Define to 1 if you have the <sys/statvfs.h> header file.
    Config('HAVE_SYS_STATVFS_H', ios=1, linux=1, macos=1),

    # Define to 1 if you have the <sys/stat.h> header file.
    Config('HAVE_SYS_STAT_H', default=1),

    # Define to 1 if you have the <sys/syscall.h> header file.
    Config('HAVE_SYS_SYSCALL_H', default=1),

    # Define to 1 if you have the <sys/sysmacros.h> header file.
    Config('HAVE_SYS_SYSMACROS_H', android=1, linux=1),

    # Define to 1 if you have the <sys/sys_domain.h> header file.
    Config('HAVE_SYS_SYS_DOMAIN_H', macos=1),

    # Define to 1 if you have the <sys/times.h> header file.
    Config('HAVE_SYS_TIMES_H', default=1),

    # Define to 1 if you have the <sys/time.h> header file.
    Config('HAVE_SYS_TIME_H', default=1),

    # Define to 1 if you have the <sys/types.h> header file.
    Config('HAVE_SYS_TYPES_H', default=1),

    # Define to 1 if you have the <sys/uio.h> header file.
    Config('HAVE_SYS_UIO_H', default=1),

    # Define to 1 if you have the <sys/un.h> header file.
    Config('HAVE_SYS_UN_H', default=1),

    # Define to 1 if you have the <sys/utsname.h> header file.
    Config('HAVE_SYS_UTSNAME_H', default=1),

    # Define to 1 if you have the <sys/wait.h> header file.
    Config('HAVE_SYS_WAIT_H', default=1),

    # Define to 1 if you have the <sys/xattr.h> header file.
    Config('HAVE_SYS_XATTR_H', default=1),

    # Define to 1 if you have the <syslog.h> header file.
    Config('HAVE_SYSLOG_H', default=1),

    # Define to 1 if you have the 'tcgetpgrp' function.
    Config('HAVE_TCGETPGRP', default=1),

    # Define to 1 if you have the 'tcsetpgrp' function.
    Config('HAVE_TCSETPGRP', default=1),

    # Define to 1 if you have the 'tempnam' function.
    Config('HAVE_TEMPNAM', default=1),

    # Define to 1 if you have the <termios.h> header file.
    Config('HAVE_TERMIOS_H', default=1),

    # Define to 1 if you have the <term.h> header file.
    Config('HAVE_TERM_H', default=1),

    # Define to 1 if you have the 'tgamma' function.
    Config('HAVE_TGAMMA', default=1),

    # Define to 1 if you have the 'timegm' function.
    Config('HAVE_TIMEGM', default=1),

    # Define to 1 if you have the 'times' function.
    Config('HAVE_TIMES', default=1),

    # Define to 1 if you have the 'tmpfile' function.
    Config('HAVE_TMPFILE', default=1),

    # Define to 1 if you have the 'tmpnam' function.
    Config('HAVE_TMPNAM', default=1),

    # Define to 1 if you have the 'tmpnam_r' function.
    Config('HAVE_TMPNAM_R', linux=1),

    # Define to 1 if you have the 'truncate' function.
    Config('HAVE_TRUNCATE', default=1),

    # Define to 1 if you have the 'ttyname' function.
    Config('HAVE_TTYNAME', default=1),

    # Define to 1 if you have the 'umask' function.
    Config('HAVE_UMASK', default=1),

    # Define to 1 if you have the 'uname' function.
    Config('HAVE_UNAME', default=1),

    # Define to 1 if you have the <unistd.h> header file.
    Config('HAVE_UNISTD_H', default=1),

    # Define to 1 if you have the 'unlinkat' function.
    Config('HAVE_UNLINKAT', default=1),

    # Define to 1 if you have the 'unsetenv' function.
    Config('HAVE_UNSETENV', default=1),

    # Define if you have a useable wchar_t type defined in wchar.h; useable
    # means wchar_t must be an unsigned type with at least 16 bits. (see
    # Include/unicodeobject.h).
    Config('HAVE_USABLE_WCHAR_T', ios=1, macos=1),

    # Define to 1 if you have the <util.h> header file.
    Config('HAVE_UTIL_H', ios=1, macos=1),

    # Define to 1 if you have the 'utimensat' function.
    Config('HAVE_UTIMENSAT', default=1),

    # Define to 1 if you have the 'utimes' function.
    Config('HAVE_UTIMES', default=1),

    # Define to 1 if you have the <utime.h> header file.
    Config('HAVE_UTIME_H', default=1),

    # Define to 1 if you have the <utmp.h> header file.
    Config('HAVE_UTMP_H', default=1),

    # Define if uuid_generate_time_safe() exists.
    Config('HAVE_UUID_GENERATE_TIME_SAFE', linux=1),

    # Define to 1 if you have the <uuid.h> header file.
    Config('HAVE_UUID_H', android=1),

    # Define to 1 if you have the <uuid/uuid.h> header file.
    Config('HAVE_UUID_UUID_H', ios=1, linux=1, macos=1),

    # Define to 1 if you have the 'vfork' function.
    Config('HAVE_VFORK', default=1),

    # Define to 1 if you have the 'wait' function.
    Config('HAVE_WAIT', default=1),

    # Define to 1 if you have the 'wait3' function.
    Config('HAVE_WAIT3', default=1, android=None),

    # Define to 1 if you have the 'wait4' function.
    Config('HAVE_WAIT4', default=1),

    # Define to 1 if you have the 'waitid' function.
    Config('HAVE_WAITID', default=1),

    # Define to 1 if you have the 'waitpid' function.
    Config('HAVE_WAITPID', default=1),

    # Define if the compiler provides a wchar.h header file.
    Config('HAVE_WCHAR_H', default=1),

    # Define to 1 if you have the 'wcscoll' function.
    Config('HAVE_WCSCOLL', default=1),

    # Define to 1 if you have the 'wcsftime' function.
    Config('HAVE_WCSFTIME', default=1),

    # Define to 1 if you have the 'wcsxfrm' function.
    Config('HAVE_WCSXFRM', default=1),

    # Define to 1 if you have the 'wmemcmp' function.
    Config('HAVE_WMEMCMP', default=1),

    # Define if tzset() actually switches the local timezone in a meaningful
    # way.
    Config('HAVE_WORKING_TZSET', default=1),

    # Define to 1 if you have the 'writev' function.
    Config('HAVE_WRITEV', default=1),

    # Define if libssl has X509_VERIFY_PARAM_set1_host and related function.
    Config('HAVE_X509_VERIFY_PARAM_SET1_HOST', android=1, linux=1),

    # Define if the zlib library has inflateCopy
    Config('HAVE_ZLIB_COPY', default=1),

    # Define to 1 if you have the <zlib.h> header file.
    Config('HAVE_ZLIB_H', default=1),

    # Define to 1 if 'major', 'minor', and 'makedev' are declared in
    # <sysmacros.h>.
    Config('MAJOR_IN_SYSMACROS', linux=1),

    # Define if mvwdelch in curses.h is an expression.
    Config('MVWDELCH_IS_EXPRESSION', default=1, android=None),

    # Define if pthread_key_t is compatible with int.
    Config('PTHREAD_KEY_T_IS_COMPATIBLE_WITH_INT', android=1, linux=1),

    # Defined if PTHREAD_SCOPE_SYSTEM supported.
    Config('PTHREAD_SYSTEM_SCHED_SUPPORTED', android=1, linux=1),

    # Define if you want to coerce the C locale to a UTF-8 based locale.
    Config('PY_COERCE_C_LOCALE', default=1),

    # Define to printf format modifier for Py_ssize_t
    Config('PY_FORMAT_SIZE_T', default='"z"'),

    # Default cipher suites list for ssl module. 1: Python's preferred
    # selection, 2: leave OpenSSL defaults untouched, 0: custom string
    Config('PY_SSL_DEFAULT_CIPHERS', default=1),

    # PEP 11 Support tier (1, 2, 3 or 0 for unsupported).
    Config('PY_SUPPORT_TIER', default=1),

    # Define if i>>j for signed int i does not extend the sign bit when i < 0
    Config('SIGNED_RIGHT_SHIFT_ZERO_FILLS', ios=1, macos=1),

    # The size of 'double', as computed by sizeof.
    Config('SIZEOF_DOUBLE', default=8),

    # The size of 'float', as computed by sizeof.
    Config('SIZEOF_FLOAT', default=4),

    # The size of 'fpos_t', as computed by sizeof.
    Config('SIZEOF_FPOS_T', android_32=4, android_64=8, ios=8, linux=16,
            macos=8),

    # The size of 'int', as computed by sizeof.
    Config('SIZEOF_INT', default=4),

    # The size of 'long', as computed by sizeof.
    Config('SIZEOF_LONG', android_32=4, android_64=8, ios_64=8, linux_32=4,
            linux_64=8, macos_64=8),

    # The size of 'long double', as computed by sizeof.
    Config('SIZEOF_LONG_DOUBLE', android=8, ios=16, linux_32=12, linux_64=16,
            macos=16),

    # The size of 'long long', as computed by sizeof.
    Config('SIZEOF_LONG_LONG', default=8),

    # The size of 'off_t', as computed by sizeof.
    Config('SIZEOF_OFF_T', android_32=4, android_64=8, ios=8, linux=8,
            macos=8),

    # The size of 'pid_t', as computed by sizeof.
    Config('SIZEOF_PID_T', default=4),

    # The size of 'pthread_key_t', as computed by sizeof.
    Config('SIZEOF_PTHREAD_KEY_T', default=4, ios_64=8, macos_64=8),

    # The size of 'pthread_t', as computed by sizeof.
    Config('SIZEOF_PTHREAD_T', android_32=4, android_64=8, ios_64=8,
            linux_32=4, linux_64=8, macos_64=8),

    # The size of 'short', as computed by sizeof.
    Config('SIZEOF_SHORT', default=2),

    # The size of 'size_t', as computed by sizeof.
    Config('SIZEOF_SIZE_T', android_32=4, android_64=8, ios_64=8, linux_32=4,
            linux_64=8, macos_64=8),

    # The size of 'time_t', as computed by sizeof.
    Config('SIZEOF_TIME_T', android_32=4, android_64=8, ios_64=8, linux_32=4,
            linux_64=8, macos_64=8),

    # The size of 'uintptr_t', as computed by sizeof.
    Config('SIZEOF_UINTPTR_T', android_32=4, android_64=8, ios_64=8,
            linux_32=4, linux_64=8, macos_64=8),

    # The size of 'void *', as computed by sizeof.
    Config('SIZEOF_VOID_P', android_32=4, android_64=8, ios_64=8, linux_32=4,
            linux_64=8, macos_64=8),

    # The size of 'wchar_t', as computed by sizeof.
    Config('SIZEOF_WCHAR_T', default=4),

    # The size of '_Bool', as computed by sizeof.
    Config('SIZEOF__BOOL', default=1),

    # Define to 1 if you have the ANSI C header files.
    Config('STDC_HEADERS', default=1),

    # Define if you can safely include both <sys/select.h> and <sys/time.h>
    # (which you can't on SCO ODT 3.0).
    Config('SYS_SELECT_WITH_SYS_TIME', default=1),

    # Define if you want build the _decimal module using a coroutine-local
    # rather than a thread-local context.
    Config('WITH_DECIMAL_CONTEXTVAR', default=1),

    # Define if tanh(-0.) is -0., or if platform doesn't have signed zeros
    Config('TANH_PRESERVES_ZERO_SIGN', default=1, android=None),

    # Define to 1 if you can safely include both <sys/time.h> and <time.h>.
    Config('TIME_WITH_SYS_TIME', default=1),

    # Define if WINDOW in curses.h offers a field _flags.
    Config('WINDOW_HAS_FLAGS', ios=1, linux=1, macos=1),

    # Define if you want to compile in Python-specific mallocs.
    Config('WITH_PYMALLOC', default=1),

    # Define if you want to compile in object freelists optimization.
    Config('WITH_FREELISTS', default=1),

    # Define on Darwin to activate all library features
    Config('_DARWIN_C_SOURCE', default=1),

    # This must be set to 64 on some systems to enable large file support.
    Config('_FILE_OFFSET_BITS', default=64),

    # Activate UNIX variant library extensions.
    Config('__EXTENSIONS__', default=1),
    Config('_ALL_SOURCE', default=1),
    Config('_GNU_SOURCE', default=1),
    Config('_POSIX_PTHREAD_SEMANTICS', default=1),
    Config('_TANDEM_SOURCE', default=1),

    # This must be defined on some systems to enable large file support.
    Config('_LARGEFILE_SOURCE', default=1),

    # Define on NetBSD to activate all library features
    Config('_NETBSD_SOURCE', default=1),

    # Define to activate features from IEEE Stds 1003.1-2008
    Config('_POSIX_C_SOURCE', default='200809L'),

    # macOS, iOS framework name.
    Config('_PYTHONFRAMEWORK', default='""'),

    # Define to force use of thread-safe errno, h_errno, and other functions
    Config('_REENTRANT', android=1, ios=1, macos=1),

    # Define to the level of X/Open that your system supports
    Config('_XOPEN_SOURCE', default=700),

    # Define to activate Unix95-and-earlier features
    Config('_XOPEN_SOURCE_EXTENDED', default=1),

    # Define on FreeBSD to activate all library features
    Config('__BSD_VISIBLE', default=1),

    # Define on Apple.
    Config('THREAD_STACK_SIZE', ios=0x1000000, macos=0x1000000),
)


def generate_pyconfig_h(pyconfig_h_name, component):
    """ Create the pyconfig.h file for a specific target variant. """

    pyconfig_h = component.create_file(pyconfig_h_name)

    pyconfig_h.write('''#ifndef Py_PYCONFIG_H
#define Py_PYCONFIG_H

''')

    if component.target_platform_name == 'android':
        pyconfig_h.write(
                '#define ANDROID_API_LEVEL {0}\n'.format(
                        component.android_api))

    if component.dynamic_loading:
        pyconfig_h.write('#define HAVE_DYNAMIC_LOADING 1\n')

    py_major = 0

    for config in pyconfig:
        if py_major != config.py_major:
            py_major = config.py_major

            if py_major == 0:
                pyconfig_h.write('#endif\n')
            else:
                pyconfig_h.write(
                        '#if PY_MAJOR_VERSION == {0}\n'.format(py_major))

        value = config.value(component)

        if value is None:
            # We provide an commented out #define to make it easier to modify
            # the file by hand later.
            pyconfig_h.write('/* #define {0} */\n'.format(config.name))
        else:
            pyconfig_h.write('#define {0} {1}\n'.format(config.name, value))

    if py_major != 0:
        pyconfig_h.write('#endif\n')

    pyconfig_h.write('''
#endif
''')

    pyconfig_h.close()
