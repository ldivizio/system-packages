%global __provides_exclude_from %{_docdir}
%global __requires_exclude_from %{_docdir}

%global debug_package   %{nil}
%define _build_id_links none

%define real_name dovecot
%define major_version 2.4
%define minor_version 2

Summary:  Secure IMAP and POP3 server
Name:     dovecot%{major_version}
Version:  %{major_version}.%{minor_version}
Release:  1%{?dist}
License:  MIT AND LGPL-2.1-only 
URL:      http://www.dovecot.org
Source:   %{url}/releases/%{major_version}/%{real_name}-%{version}.tar.gz
Source1:  dovecot.sysusers

# Official patches
Patch16: dovecot-2.4.1-opensslhmac3.patch
Patch23: dovecot-2.4.1-nolibotp.patch
Patch24: dovecot-2.4.2-fixbuild.patch

BuildRequires:  gcc-toolset-15
BuildRequires:  gcc-toolset-15-gcc
BuildRequires:  gcc-toolset-15-gcc-c++
BuildRequires:  gcc-toolset-15-gcc-plugin-annobin
BuildRequires:  openssl-devel
BuildRequires:  mariadb-connector-c-devel
BuildRequires:  libpq-devel
BuildRequires:  sqlite-devel
BuildRequires:  openldap-devel
BuildRequires:  libtool, autoconf, automake, pkgconfig, gettext-devel
BuildRequires:  libcap-devel
BuildRequires:  libzstd-devel
BuildRequires:  lua-devel
BuildRequires:  libstemmer-devel
BuildRequires:  xapian-core-devel
BuildRequires:  systemd-devel

%description
Dovecot is an IMAP server for Linux/UNIX-like systems, written with security
primarily in mind.  It also contains a small POP3 server.  It supports mail
in either of maildir or mbox formats.

The SQL drivers and authentication plug-ins are in their subpackages.

%package sql
Requires: %{name} = %{version}-%{release}
Summary: Common SQL library

%description sql
Common SQL library to MySQL/PostgreSQL/SQLite back ends

%package mysql
Requires: %{name}-sql = %{version}-%{release}
Summary: MySQL back end for dovecot

%description mysql
This package provides the MySQL back end for dovecot-auth etc.

%package pgsql
Requires: %{name}-sql = %{version}-%{release}
Summary: PostgreSQL back end for dovecot

%description pgsql
This package provides the PostgreSQL back end for dovecot-auth etc.

%package sqlite
Requires: %{name}-sql = %{version}-%{release}
Summary: SQLite ostgres SQL back end for dovecot

%description sqlite
This package provides the SQLite back end for dovecot-auth etc.

%package lua
Requires: %{name} = %{version}-%{release}
Summary: Lua back end for dovecot

%description lua
This package provides the Lua back end for dovecot-auth

%package ldap
Requires: %{name} = %{version}-%{release}
Summary: LDAP back end for dovecot

%description ldap
This package provides the LDAP back end for dovecot-auth

%package submission
Requires: %{name} = %{version}-%{release}
Summary: Mail submission agent

%description submission
Mail submission agent

%package pop3
Requires: %{name} = %{version}-%{release}
Summary: POP3 daemon

%description pop3
POP3 daemon

%package imap
Requires: %{name} = %{version}-%{release}
Summary: IMAP daemon

%description imap
IMAP daemon

%package lda
Requires: %{name} = %{version}-%{release}
Summary: LDA and LMTP daemon

%description lda
LDA and LMTP daemon

%package plugin-lazy_expunge
Requires: %{name} = %{version}-%{release}
Summary: lazy-expunge plugin

%description plugin-lazy_expunge

%package plugin-pop3_migration
Requires: %{name} = %{version}-%{release}
Summary: pop3-migration plugin

%description plugin-pop3_migration

%package plugin-last_login
Requires: %{name} = %{version}-%{release}
Summary: last-login plugin

%description plugin-last_login

%package plugin-trash
Requires: %{name} = %{version}-%{release}
Summary: trash plugin

%description plugin-trash

%package plugin-notify
Requires: %{name} = %{version}-%{release}
Summary: notify plugin

%description plugin-notify

%package plugin-mail_log
Requires: %{name}-plugin-notify = %{version}-%{release}
Summary: mail-log plugin

%description plugin-mail_log

%package plugin-notify_status
Requires: %{name}-plugin-notify = %{version}-%{release}
Summary: notify-status plugin

%description plugin-notify_status

%package plugin-virtual
Requires: %{name} = %{version}-%{release}
Summary: virtual plugin

%description plugin-virtual

%package plugin-welcome
Requires: %{name} = %{version}-%{release}
Summary: welcome plugin

%description plugin-welcome

%package plugin-push_notification
Requires: %{name} = %{version}-%{release}
Summary: push-notification plugin

%description plugin-push_notification

%package plugin-push_notification_lua
Requires: %{name}-plugin-push_notification = %{version}-%{release}
Requires: %{name}-lua = %{version}-%{release}
Summary: push-notification Lua plugin

%description plugin-push_notification_lua

%package plugin-quota
Requires: %{name} = %{version}-%{release}
Summary: quota plugin

%description plugin-quota

%package plugin-quota_clone
Requires: %{name}-plugin-quota = %{version}-%{release}
Summary: quota-clone plugin

%description plugin-quota_clone

%package plugin-imap_quota
Requires: %{name}-plugin-quota = %{version}-%{release}
Summary: imap-quota plugin

%description plugin-imap_quota

%package plugin-mail_crypt
Requires: %{name} = %{version}-%{release}
Summary: mail-crypt plugin

%description plugin-mail_crypt

%package plugin-acl
Requires: %{name} = %{version}-%{release}
Summary: acl plugin

%description plugin-acl

%package plugin-imap_acl
Requires: %{name}-plugin-acl = %{version}-%{release}
Summary: imap-acl plugin

%description plugin-imap_acl

%package plugin-fts
Requires: %{name} = %{version}-%{release}
Summary: fts plugin

%description plugin-fts

%package plugin-mail_compress
Requires: %{name} = %{version}-%{release}
Summary: mail-compress plugin

%description plugin-mail_compress

%package plugin-charset_alias
Requires: %{name} = %{version}-%{release}
Summary: charset-alias plugin

%description plugin-charset_alias

%package plugin-mail_lua
Requires: %{name}-lua = %{version}-%{release}
Summary: mail-lua plugin

%description plugin-mail_lua

%package plugin-fts-flatcurve
Requires: %{name}-plugin-fts = %{version}-%{release}
Summary: fts-flatcurve plugin

%description plugin-fts-flatcurve

%package plugin-fs_compress
Requires: %{name} = %{version}-%{release}
Summary: fs-compress plugin

%description plugin-fs_compress

%package devel
Requires: %{name} = %{version}-%{release}
Summary: Development files for dovecot
%description devel

%prep
%setup -q -n %{real_name}-%{version}

%build
%if 0%{?rhel} < 10
source /opt/rh/gcc-toolset-15/enable
%else
source /usr/lib/gcc-toolset/15-env.source
%endif

%global _hardened_build 1
export CFLAGS="%{__global_cflags} -fno-strict-aliasing -fstack-reuse=none"
export LDFLAGS="-Wl,-z,now -Wl,-z,relro %{?__global_ldflags}"
mkdir -p m4
autoreconf -I . -fiv #required for aarch64 support
%configure                       \
    INSTALL_DATA="install -c -p -m644" \
    --enable-maintainer-mode     \
    --disable-static             \
    --disable-rpath              \
    --without-nss                \
    --without-pam                \
    --with-gssapi=no             \
    --with-lua=plugin            \
    --with-sql=plugin            \
    --with-mysql                 \
    --with-pgsql                 \
    --with-sqlite                \
    --with-ldap=plugin           \
    --without-cassandra          \
    --without-zlib               \
    --without-bzlib              \
    --without-lzma               \
    --without-lz4                \
    --with-zstd                  \
    --with-libcap                \
    --with-ssl=openssl           \
    --without-solr               \
    --with-stemmer               \
    --with-flatcurve             \
    --without-docs               \
    --with-systemd

%make_build

%install
rm -rf $RPM_BUILD_ROOT

%make_install

#remove the libtool archives
find $RPM_BUILD_ROOT%{_libdir}/%{real_name}/ -name '*.la' | xargs rm -f

#remove what we don't want
rm -f $RPM_BUILD_ROOT%{_sysconfdir}/dovecot/README

install -p -D -m 0644 %{S:1} $RPM_BUILD_ROOT%{_sysusersdir}/dovecot.sysusers

%pre
#dovecot uid and gid are reserved, see /usr/share/doc/setup-*/uidgid
%sysusers_create_compat %{S:1}

%files
%{_sbindir}/dovecot

%{_bindir}/doveadm
%{_bindir}/doveconf

%exclude %{_sysconfdir}/%{real_name}
%exclude %{_docdir}/%{real_name}/*
%exclude %{_mandir}
%exclude %{_unitdir}

%exclude %{_bindir}/dovecot-sysreport
%exclude %{_libexecdir}/%{real_name}/settings-history.py
%exclude %{_libexecdir}/%{real_name}/gdbhelper
%exclude %{_libexecdir}/%{real_name}/quota-status

%exclude %{_libexecdir}/%{real_name}/submission
%exclude %{_libexecdir}/%{real_name}/submission-login

%exclude %{_libexecdir}/%{real_name}/pop3
%exclude %{_libexecdir}/%{real_name}/pop3-login

%exclude %{_libdir}/%{real_name}/auth/libauthdb_imap.so
%exclude %{_libexecdir}/%{real_name}/imap
%exclude %{_libexecdir}/%{real_name}/imap-hibernate
%exclude %{_libexecdir}/%{real_name}/imap-login
%exclude %{_libexecdir}/%{real_name}/imap-urlauth
%exclude %{_libexecdir}/%{real_name}/imap-urlauth-login
%exclude %{_libexecdir}/%{real_name}/imap-urlauth-worker

%exclude %{_libexecdir}/%{real_name}/dovecot-lda
%exclude %{_libexecdir}/%{real_name}/deliver
%exclude %{_libexecdir}/%{real_name}/lmtp

%exclude %{_libdir}/%{real_name}/libdovecot-sql.so*

%{_sysusersdir}/dovecot.sysusers

%dir %{_libdir}/%{real_name}
%dir %{_libdir}/%{real_name}/auth
%dir %{_libdir}/%{real_name}/doveadm
%{_libdir}/%{real_name}/libdovecot.so*
%{_libdir}/%{real_name}/libdovecot-dsync.so*
%{_libdir}/%{real_name}/libdovecot-login.so*
%{_libdir}/%{real_name}/libdovecot-gssapi.so*
%{_libdir}/%{real_name}/libdovecot-storage.so*

%{_libdir}/%{real_name}/libssl_iostream_openssl.so
%{_libdir}/%{real_name}/libdcrypt_openssl.so
%{_libdir}/%{real_name}/var_expand_crypt.so

%{_libexecdir}/%{real_name}

%exclude %{_libexecdir}/%{real_name}/decode2text.sh
%exclude %{_libexecdir}/%{real_name}/xml2text

%files devel
%{_includedir}/dovecot
%{_datadir}/aclocal/dovecot*.m4
%{_libdir}/%{real_name}/dovecot-config

%files sql
%{_libdir}/%{real_name}/libdovecot-sql.so*

%files mysql
%{_libdir}/%{real_name}/libdriver_mysql.so
%{_libdir}/%{real_name}/auth/libdriver_mysql.so
%{_libdir}/%{real_name}/dict/libdriver_mysql.so

%files pgsql
%{_libdir}/%{real_name}/libdriver_pgsql.so
%{_libdir}/%{real_name}/auth/libdriver_pgsql.so
%{_libdir}/%{real_name}/dict/libdriver_pgsql.so

%files sqlite
%{_libdir}/%{real_name}/auth/libdriver_sqlite.so
%{_libdir}/%{real_name}/dict/libdriver_sqlite.so
%{_libdir}/%{real_name}/libdriver_sqlite.so

%files lua
%{_libdir}/%{real_name}/auth/libauthdb_lua.so
%{_libdir}/%{real_name}/libdovecot-lua.so*

%files ldap
%{_libdir}/%{real_name}/libdovecot-ldap.so*
%{_libdir}/%{real_name}/auth/libauthdb_ldap.so
%{_libdir}/%{real_name}/dict/libdict_ldap.so

%files submission
%{_libexecdir}/%{real_name}/submission
%{_libexecdir}/%{real_name}/submission-login

%files pop3
%{_libexecdir}/%{real_name}/pop3
%{_libexecdir}/%{real_name}/pop3-login

%files imap
%{_libdir}/%{real_name}/auth/libauthdb_imap.so
%{_libexecdir}/%{real_name}/imap
%{_libexecdir}/%{real_name}/imap-hibernate
%{_libexecdir}/%{real_name}/imap-login
%{_libexecdir}/%{real_name}/imap-urlauth
%{_libexecdir}/%{real_name}/imap-urlauth-login
%{_libexecdir}/%{real_name}/imap-urlauth-worker

%files lda
%{_libdir}/%{real_name}/libdovecot-lda.so*
%{_libexecdir}/%{real_name}/dovecot-lda
%{_libexecdir}/%{real_name}/deliver
%{_libexecdir}/%{real_name}/lmtp

%files plugin-lazy_expunge
%{_libdir}/%{real_name}/lib02_lazy_expunge_plugin.so

%files plugin-pop3_migration
%{_libdir}/%{real_name}/lib05_pop3_migration_plugin.so

%files plugin-last_login
%{_libdir}/%{real_name}/lib10_last_login_plugin.so

%files plugin-trash
%{_libdir}/%{real_name}/lib11_trash_plugin.so

%files plugin-notify
%{_libdir}/%{real_name}/lib15_notify_plugin.so

%files plugin-mail_log
%{_libdir}/%{real_name}/lib20_mail_log_plugin.so

%files plugin-notify_status
%{_libdir}/%{real_name}/lib20_notify_status_plugin.so

%files plugin-quota_clone
%{_libdir}/%{real_name}/lib20_quota_clone_plugin.so

%files plugin-virtual
%{_libdir}/%{real_name}/lib20_virtual_plugin.so

%files plugin-welcome
%{_libdir}/%{real_name}/lib99_welcome_plugin.so

%files plugin-push_notification
%{_libdir}/%{real_name}/lib20_push_notification_plugin.so

%files plugin-push_notification_lua
%{_libdir}/%{real_name}/lib22_push_notification_lua_plugin.so

%files plugin-quota
%{_libdir}/%{real_name}/doveadm/lib10_doveadm_quota_plugin.so
%{_libdir}/%{real_name}/lib10_quota_plugin.so

%files plugin-imap_quota
%{_libdir}/%{real_name}/lib11_imap_quota_plugin.so

%files plugin-mail_crypt
%{_libdir}/%{real_name}/libfs_crypt.so
%{_libdir}/%{real_name}/doveadm/libdoveadm_mail_crypt_plugin.so
%{_libdir}/%{real_name}/lib10_mail_crypt_plugin.so
%{_libdir}/%{real_name}/lib05_mail_crypt_acl_plugin.so

%files plugin-acl
%{_libdir}/%{real_name}/doveadm/lib10_doveadm_acl_plugin.so
%{_libdir}/%{real_name}/lib01_acl_plugin.so

%files plugin-imap_acl
%{_libdir}/%{real_name}/lib02_imap_acl_plugin.so

%files plugin-mail_compress
%{_libdir}/%{real_name}/lib20_mail_compress_plugin.so

%files plugin-charset_alias
%{_libdir}/%{real_name}/lib20_charset_alias_plugin.so

%files plugin-mail_lua
%{_libdir}/%{real_name}/lib01_mail_lua_plugin.so
%{_libdir}/%{real_name}/libdovecot-storage-lua.so*

%files plugin-fts
%{_libdir}/%{real_name}/libdovecot-language.so*
%{_datadir}/%{real_name}/stopwords
%{_libdir}/%{real_name}/doveadm/lib20_doveadm_fts_plugin.so
%{_libdir}/%{real_name}/lib20_fts_plugin.so

%files plugin-fts-flatcurve
%{_libdir}/%{real_name}/doveadm/libdoveadm_fts_flatcurve_plugin.so
%{_libdir}/%{real_name}/lib21_fts_flatcurve_plugin.so

%files plugin-fs_compress
%{_libdir}/%{real_name}/libdovecot-compression.so*
%{_libdir}/%{real_name}/libfs_compress.so
