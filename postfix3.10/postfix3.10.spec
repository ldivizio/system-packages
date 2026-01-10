# plugins have unresolvable symbols in compile time
%undefine _strict_symbol_defs_build

%define real_name postfix
%define pflogsumm_ver 1.1.13

%global debug_package   %{nil}
%define _build_id_links none

%bcond_with db
%bcond_without mysql
%bcond_without pgsql
%bcond_without sqlite
%bcond_without mongodb
%bcond_without ldap
%bcond_without pcre
%bcond_without sasl
%bcond_without tls
%bcond_without smtputf8
%bcond_with tlsrpt
%bcond_without tools

# hardened build if not overrided
%{!?_hardened_build:%global _hardened_build 1}

# Postfix requires one exlusive uid/gid and a 2nd exclusive gid for its own
# use.  Let me know if the second gid collides with another package.
# Be careful: Redhat's 'mail' user & group isn't unique!
# It's now handled by systemd-sysusers.
%define postfix_user	postfix
%define maildrop_group	postdrop

%define postfix_config_dir  %{_sysconfdir}/postfix
%define postfix_daemon_dir  %{_libexecdir}/postfix
%define postfix_shlib_dir   %{_libdir}/postfix
%define postfix_command_dir %{_sbindir}
%define postfix_queue_dir   %{_var}/spool/postfix
%define postfix_data_dir    %{_var}/lib/postfix

# Filter private libraries
%global _privatelibs libpostfix-.+\.so.*
%global __provides_exclude ^(%{_privatelibs})$
%global __requires_exclude ^(%{_privatelibs})$

Name: postfix3.10
Summary: Postfix Mail Transport Agent
Version: 3.10.7
Release: 1%{?dist}
URL: http://www.postfix.org
License: (IBM and GPLv2+) or (EPL-2.0 and GPLv2+)

Provides:  %{real_name} = 3:%{version}-%{release}
Requires:  %{name}-lmdb%{?_isa} = %{version}-%{release}
%if %{with tlsrpt}
Requires:  libtlsrpt
%endif


Provides: MTA smtpd smtpdaemon server(smtp)
Source0:  https://de.postfix.org/ftpmirror/official/%{real_name}-%{version}.tar.gz
Source1:  https://jimsun.linxnet.com/downloads/pflogsumm-%{pflogsumm_ver}.tar.gz
Source2:  main.cf
Source3:  master.cf
Source4:  postfix.service
Source5:  postfix.tmpfilesd
Source6:  postfix.sysusers

# Patches
Patch2:  postfix-3.9.0-files.patch
Patch3:  postfix-3.9.0-alternatives.patch
Patch4:  postfix-3.8.0-large-fs.patch
Patch11: postfix-3.4.4-chroot-example-fix.patch
Patch12: postfix-3.10-bool.patch

Patch90: postfix-3.8.6-rh-gcc.patch

# Determine the different packages required for building postfix
BuildRequires: make
BuildRequires: perl-generators
BuildRequires: pkgconfig
BuildRequires: zlib-devel
BuildRequires: systemd-units
BuildRequires: lmdb-devel
BuildRequires: gcc
BuildRequires: m4
BuildRequires: findutils
BuildRequires: systemd-rpm-macros
BuildRequires: sed

%{?with_ldap:BuildRequires: openldap-devel}
%{?with_pcre:BuildRequires: pcre2-devel}
%{?with_mysql:BuildRequires: mariadb-connector-c-devel}
%{?with_pgsql:BuildRequires: libpq-devel}
%{?with_sqlite:BuildRequires: sqlite-devel}
%{?with_mongodb:BuildRequires: mongo-c-driver-devel}
%{?with_smtputf8:BuildRequires: libicu-devel}
%{?with_tlsrpt:BuildRequires: libtlsrpt-devel}
%{?with_tls:BuildRequires: openssl-devel}

Requires(post): systemd hostname
Requires(post): %{_sbindir}/alternatives
Requires(preun): %{_sbindir}/alternatives
Requires(preun): systemd
Requires(postun): systemd
Requires: diffutils
Requires: findutils
Requires: policycoreutils

%{?sysusers_requires_compat}

%description
Postfix is a Mail Transport Agent (MTA).

%if %{with tools}
%package tools
Summary: Postfix utilities
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description tools
This package contains perl scripts pflogsumm and qshape.
 
Pflogsumm is a log analyzer/summarizer for the Postfix MTA. It is
designed to provide an over-view of Postfix activity. Pflogsumm
generates summaries and, in some cases, detailed reports of mail
server traffic volumes, rejected and bounced email, and server
warnings, errors and panics.
 
qshape prints Postfix queue domain and age distribution.
%endif


%if %{with mysql}
%package mysql
Summary: Postfix MySQL map support
Requires: %{name} = %{version}-%{release}

%description mysql
This provides support for MySQL maps in Postfix. If you plan to use MySQL
maps with Postfix, you need this.
%endif

%if %{with pgsql}
%package pgsql
Summary: Postfix PostgreSQL map support
Requires: %{name} = %{version}-%{release}

%description pgsql
This provides support for PostgreSQL  maps in Postfix. If you plan to use
PostgreSQL maps with Postfix, you need this.
%endif

%if %{with sqlite}
%package sqlite
Summary: Postfix SQLite map support
Requires: %{name} = %{version}-%{release}

%description sqlite
This provides support for SQLite maps in Postfix. If you plan to use SQLite
maps with Postfix, you need this.
%endif

%if %{with mongodb}
%package mongodb
Summary: Postfix MongoDB map support
Requires: %{name} = %{version}-%{release}

%description mongodb
This provides support for MongoDB maps in Postfix. If you plan to use MongoDB
maps with Postfix, you need this.
%endif

%if %{with ldap}
%package ldap
Summary: Postfix LDAP map support
Requires: %{name} = %{version}-%{release}

%description ldap
This provides support for LDAP maps in Postfix. If you plan to use LDAP
maps with Postfix, you need this.
%endif

%package lmdb
Summary: Postfix LDMB map support
Requires: %{name} = %{version}-%{release}

%description lmdb
This provides support for LMDB maps in Postfix. If you plan to use LMDB
maps with Postfix, you need this.

%if %{with pcre}
%package pcre
Summary: Postfix PCRE map support
Requires: %{name} = %{version}-%{release}

%description pcre
This provides support for PCRE maps in Postfix. If you plan to use PCRE
maps with Postfix, you need this.
%endif

%prep
%setup -n %{real_name}-%{version} -q

# Apply obligatory patches
%patch -P2 -p1 -b .files
%patch -P3 -p1 -b .alternatives
%patch -P4 -p1 -b .large-fs
	
%patch -P11 -p1 -b .chroot-example-fix
%patch -P12 -p1 -b .bool

#%patch -P14 -p1 -b .openssl-no-engine

%patch -P90 -p1 -b .rh-gcc

# Change DEF_SHLIB_DIR according to build host
sed -i \
's|^\(\s*#define\s\+DEF_SHLIB_DIR\s\+\)"/usr/lib/postfix"|\1"%{_libdir}/postfix"|' \
src/global/mail_params.h

# Extract pflogsumm
gzip -dc %{SOURCE1} | tar xf -
pushd pflogsumm-%{pflogsumm_ver}
popd

# Backport 3.8-20221006 fix for uname -r detection
sed -i makedefs -e '\@Linux\.@s|345|3456|'
sed -i src/util/sys_defs.h -e 's@defined(LINUX5)@defined(LINUX5) || defined(LINUX6)@'

%build
%set_build_flags
unset AUXLIBS AUXLIBS_LDAP AUXLIBS_LMDB AUXLIBS_PCRE AUXLIBS_MYSQL AUXLIBS_PGSQL AUXLIBS_SQLITE
CCARGS="-fPIC -fcommon -std=gnu17"
export OPT="%{__global_cflags} -fno-strict-aliasing -fstack-reuse=none"
AUXLIBS=""

# Legacy options
CCARGS="${CCARGS} -DNO_DB -DNO_NIS -DNO_NISPLUS"

# Set LMDB as default db
CCARGS="${CCARGS} -DHAS_LMDB -DDEF_DB_TYPE=\\\"lmdb\\\""
AUXLIBS_LMDB="-llmdb"

%if %{without smtputf8}
  CCARGS="${CCARGS} -DNO_EAI"
%endif

%if %{with ldap}
  CCARGS="${CCARGS} -DHAS_LDAP"
  AUXLIBS_LDAP="-lldap -llber"
%endif

%if %{with pcre}
  CCARGS="${CCARGS} -DHAS_PCRE=2 $(pcre2-config --cflags)"
  AUXLIBS_PCRE=$(pcre2-config --libs8)
%endif

%if %{with mysql}
  CCARGS="${CCARGS} -DHAS_MYSQL -I%{_includedir}/mysql"
  #AUXLIBS_MYSQL="-L%{_libdir}/mariadb -lmysqlclient -lm"
  AUXLIBS_MYSQL="-L%{_libdir}/mysql -lmysqlclient -lm"
%endif

%if %{with pgsql}
  CCARGS="${CCARGS} -DHAS_PGSQL -I%{_includedir}/pgsql"
  AUXLIBS_PGSQL="-lpq"
%endif

%if %{with sqlite}
  CCARGS="${CCARGS} -DHAS_SQLITE `pkg-config --cflags sqlite3`"
  AUXLIBS_SQLITE="`pkg-config --libs sqlite3`"
%endif

%if %{with mongodb}
  CCARGS="${CCARGS} -DHAS_MONGODB `pkg-config --cflags libmongoc-1.0`"
  AUXLIBS_SQLITE="`pkg-config --libs libmongoc-1.0`"
%endif

%if %{with sasl}
  CCARGS="${CCARGS} -DUSE_SASL_AUTH -DDEF_SERVER_SASL_TYPE=\\\"dovecot\\\""
%endif

%if %{with tls}
  if pkg-config openssl ; then
    CCARGS="${CCARGS} -DUSE_TLS $(pkg-config --cflags openssl)"
    AUXLIBS="${AUXLIBS} $(pkg-config --libs openssl)"
  fi
%if %{with tlsrpt}
  CCARGS="${CCARGS} -DUSE_TLSRPT"
  AUXLIBS="${AUXLIBS} -ltlsrpt"
%endif
%endif

CCARGS="${CCARGS} -DDEF_CONFIG_DIR=\\\"%{postfix_config_dir}\\\""
CCARGS="${CCARGS} $(getconf LFS_CFLAGS)"

LDFLAGS="$LDFLAGS %{?_hardened_build:-Wl,-z,relro,-z,now}"

# SHLIB_RPATH is needed to find private libraries
# LDFLAGS are added to SHLIB_RPATH because the postfix build system
# ignores them. Adding LDFLAGS to SHLIB_RPATH is currently the only
# way how to get them in
make -f Makefile.init makefiles shared=yes dynamicmaps=yes \
  %{?_hardened_build:pie=yes} CCARGS="${CCARGS}" AUXLIBS="${AUXLIBS}" \
  AUXLIBS_LDAP="${AUXLIBS_LDAP}" AUXLIBS_LMDB="${AUXLIBS_LMDB}" \
  AUXLIBS_PCRE="${AUXLIBS_PCRE}" AUXLIBS_MYSQL="${AUXLIBS_MYSQL}" \
  AUXLIBS_PGSQL="${AUXLIBS_PGSQL}" AUXLIBS_SQLITE="${AUXLIBS_SQLITE}"
  DEBUG="" SHLIB_RPATH="-Wl,-rpath,%{postfix_shlib_dir} $LDFLAGS"
  POSTFIX_INSTALL_OPTS=-keep-build-mtime

%make_build

%install

# Move stuff around so we don't conflict with sendmail
for i in man1/mailq.1 man1/newaliases.1 man1/sendmail.1 man5/aliases.5 man8/smtp{,d}.8; do
  dest=$(echo $i | sed 's|\.[1-9]$|.postfix\0|')
  mv man/$i man/$dest
  sed -i "s|^\.so $i|\.so $dest|" man/man?/*.[1-9]
done

make non-interactive-package \
       install_root=$RPM_BUILD_ROOT \
       config_directory=%{postfix_config_dir} \
       meta_directory=%{postfix_config_dir} \
       shlib_directory=%{postfix_shlib_dir} \
       daemon_directory=%{postfix_daemon_dir} \
       command_directory=%{postfix_command_dir} \
       queue_directory=%{postfix_queue_dir} \
       data_directory=%{postfix_data_dir} \
       sendmail_path=%{postfix_command_dir}/sendmail.postfix \
       newaliases_path=%{_bindir}/newaliases.postfix \
       mailq_path=%{_bindir}/mailq.postfix \
       mail_owner=%{postfix_user} \
       setgid_group=%{maildrop_group} \
       manpage_directory=%{_mandir} || exit 1

# Install minimal config files
install -p -D -m 0644 %{SOURCE2} %{buildroot}%{postfix_config_dir}
install -p -D -m 0644 %{SOURCE3} %{buildroot}%{postfix_config_dir}

for i in active bounce corrupt defer deferred flush incoming private saved maildrop public pid saved trace; do
    mkdir -p $RPM_BUILD_ROOT%{postfix_queue_dir}/$i
done

## RPM compresses man pages automatically.
## - Edit postfix-files to reflect this, so post-install won't get confused
##   when called during package installation.
sed -i -r "s#(/man[158]/.*.[158]):f#\1.gz:f#" $RPM_BUILD_ROOT%{postfix_config_dir}/postfix-files

cat $RPM_BUILD_ROOT%{postfix_config_dir}/postfix-files

rm -f $RPM_BUILD_ROOT%{postfix_config_dir}/{TLS_,}LICENSE

# install qshape and pflogsumm
install -c auxiliary/qshape/qshape.pl $RPM_BUILD_ROOT%{postfix_command_dir}/qshape
install -c pflogsumm-%{pflogsumm_ver}/pflogsumm $RPM_BUILD_ROOT%{postfix_command_dir}/pflogsumm
install -c pflogsumm-%{pflogsumm_ver}/pflogsumm $RPM_BUILD_ROOT%{postfix_command_dir}/pffrombyto
install -c pflogsumm-%{pflogsumm_ver}/pflogsumm $RPM_BUILD_ROOT%{postfix_command_dir}/pftobyfrom

# remove alias file
rm -f $RPM_BUILD_ROOT%{postfix_config_dir}/aliases

# prepare alternatives ghosts
for i in %{postfix_command_dir}/sendmail %{_bindir}/{mailq,newaliases}
do
	touch $RPM_BUILD_ROOT$i
done

# helper for splitting content of dynamicmaps.cf and postfix-files
function split_file
{
# "|| :" to silently skip non existent records
  grep "$1" "$3" >> "$3.d/$2" || :
  sed -i "\|$1| d" "$3" || :
}

# split global dynamic maps configuration to individual sub-packages
pushd $RPM_BUILD_ROOT%{postfix_config_dir}
for map in %{?with_mysql:mysql} %{?with_pgsql:pgsql} %{?with_sqlite:sqlite} \
%{?with_mongodb:mongodb} %{?with_ldap:ldap} lmdb %{?with_pcre:pcre}; do
  rm -f dynamicmaps.cf.d/"$map" "postfix-files.d/$map"
  split_file "^\s*$map\b" "$map" dynamicmaps.cf
  sed -i "s|postfix-$map\\.so|%{postfix_shlib_dir}/\\0|" "dynamicmaps.cf.d/$map"
  split_file "^\$shlib_directory/postfix-$map\\.so:" "$map" postfix-files
  split_file "^\$manpage_directory/man5/${map}_table\\.5" "$map" postfix-files
  map_upper=`echo $map | tr '[:lower:]' '[:upper:]'`
done
popd

%post -e 

%{_sbindir}/alternatives --install %{postfix_command_dir}/sendmail mta %{postfix_command_dir}/sendmail.postfix 60 \
	--slave %{_bindir}/mailq mta-mailq %{_bindir}/mailq.postfix \
	--slave %{_bindir}/newaliases mta-newaliases %{_bindir}/newaliases.postfix

%files
%defattr(-, root, root, -)
 
%dir %attr(0755, root, root) %{postfix_config_dir}
%dir %attr(0755, root, root) %{postfix_daemon_dir}
%dir %attr(0755, root, root) %{postfix_shlib_dir}

%exclude %{postfix_config_dir}/access
%exclude %{postfix_config_dir}/canonical
%exclude %{postfix_config_dir}/generic
%exclude %{postfix_config_dir}/header_checks
%exclude %{postfix_config_dir}/main.cf.proto
%exclude %{postfix_config_dir}/master.cf.proto
%exclude %{postfix_config_dir}/relocated
%exclude %{postfix_config_dir}/transport
%exclude %{postfix_config_dir}/virtual

%exclude %{_mandir}/*

%dir %attr(0700, %{postfix_user}, root) %{postfix_data_dir}
%config(noreplace) %attr(0644, root, root) %{postfix_config_dir}/main.cf
%config(noreplace) %attr(0644, root, root) %{postfix_config_dir}/master.cf
%dir %attr(0755, root, root) %{postfix_config_dir}/dynamicmaps.cf.d
%dir %attr(0755, root, root) %{postfix_config_dir}/postfix-files.d
 
%exclude %{postfix_daemon_dir}/oqmgr
%exclude %{postfix_daemon_dir}/nqmgr

%attr(0755, root, root) %{postfix_command_dir}/postalias
%attr(0755, root, root) %{postfix_command_dir}/postcat
%attr(0755, root, root) %{postfix_command_dir}/postconf
%attr(2755, root, %{maildrop_group}) %{postfix_command_dir}/postdrop
%attr(0755, root, root) %{postfix_command_dir}/postfix
%attr(0755, root, root) %{postfix_command_dir}/postkick
%attr(0755, root, root) %{postfix_command_dir}/postlock
%attr(0755, root, root) %{postfix_command_dir}/postlog
%attr(0755, root, root) %{postfix_command_dir}/postmap
%attr(0755, root, root) %{postfix_command_dir}/postmulti
%attr(2755, root, %{maildrop_group}) %{postfix_command_dir}/postqueue
%attr(0755, root, root) %{postfix_command_dir}/postsuper
%attr(0644, root, root) %{postfix_config_dir}/dynamicmaps.cf
%attr(0755, root, root) %{postfix_daemon_dir}/[^mp]*
%attr(0755, root, root) %{postfix_daemon_dir}/master
%attr(0755, root, root) %{postfix_daemon_dir}/pickup
%attr(0755, root, root) %{postfix_daemon_dir}/pipe
%attr(0755, root, root) %{postfix_daemon_dir}/post-install
%attr(0644, root, root) %{postfix_config_dir}/postfix-files
%attr(0755, root, root) %{postfix_daemon_dir}/postfix-script
%attr(0755, root, root) %{postfix_daemon_dir}/postfix-tls-script
%attr(0755, root, root) %{postfix_daemon_dir}/postfix-wrapper
%attr(0755, root, root) %{postfix_daemon_dir}/postmulti-script
%attr(0755, root, root) %{postfix_daemon_dir}/postscreen
%attr(0755, root, root) %{postfix_daemon_dir}/postlogd
%attr(0755, root, root) %{postfix_daemon_dir}/proxymap
%attr(0755, root, root) %{postfix_shlib_dir}/libpostfix-*.so
%{_bindir}/mailq.postfix
%{_bindir}/newaliases.postfix
%attr(0755, root, root) %{_sbindir}/sendmail.postfix
 
%ghost %attr(0755, root, root) %{_bindir}/mailq
%ghost %attr(0755, root, root) %{_bindir}/newaliases
%ghost %attr(0755, root, root) %{_sbindir}/sendmail
 
%if %{with mysql}
%files mysql
%attr(0644, root, root) %{postfix_config_dir}/dynamicmaps.cf.d/mysql
%attr(0644, root, root) %{postfix_config_dir}/postfix-files.d/mysql
%attr(0755, root, root) %{postfix_shlib_dir}/postfix-mysql.so
%endif
 
%if %{with pgsql}
%files pgsql
%attr(0644, root, root) %{postfix_config_dir}/dynamicmaps.cf.d/pgsql
%attr(0644, root, root) %{postfix_config_dir}/postfix-files.d/pgsql
%attr(0755, root, root) %{postfix_shlib_dir}/postfix-pgsql.so
%endif
 
%if %{with sqlite}
%files sqlite
%attr(0644, root, root) %{postfix_config_dir}/dynamicmaps.cf.d/sqlite
%attr(0644, root, root) %{postfix_config_dir}/postfix-files.d/sqlite
%attr(0755, root, root) %{postfix_shlib_dir}/postfix-sqlite.so
%endif
 
%if %{with mongodb}
%files mongodb
%attr(0644, root, root) %{postfix_config_dir}/dynamicmaps.cf.d/mongodb
%attr(0644, root, root) %{postfix_config_dir}/postfix-files.d/mongodb
%attr(0755, root, root) %{postfix_shlib_dir}/postfix-mongodb.so
%endif

%if %{with ldap}
%files ldap
%attr(0644, root, root) %{postfix_config_dir}/dynamicmaps.cf.d/ldap
%attr(0644, root, root) %{postfix_config_dir}/postfix-files.d/ldap
%attr(0755, root, root) %{postfix_shlib_dir}/postfix-ldap.so
%endif
 
%files lmdb
%attr(0644, root, root) %{postfix_config_dir}/dynamicmaps.cf.d/lmdb
%attr(0644, root, root) %{postfix_config_dir}/postfix-files.d/lmdb
%attr(0755, root, root) %{postfix_shlib_dir}/postfix-lmdb.so
 
%if %{with pcre}
%files pcre
%attr(0644, root, root) %{postfix_config_dir}/dynamicmaps.cf.d/pcre
%attr(0644, root, root) %{postfix_config_dir}/postfix-files.d/pcre
%attr(0755, root, root) %{postfix_shlib_dir}/postfix-pcre.so
%endif

%files tools
%attr(0755, root, root) %{postfix_command_dir}/qshape
%attr(0755, root, root) %{postfix_command_dir}/pflogsumm
%attr(0755, root, root) %{postfix_command_dir}/pffrombyto
%attr(0755, root, root) %{postfix_command_dir}/pftobyfrom

%changelog