Name:     rspamd
Version:  3.14.3
Release:  1%{?dist}
Summary:  Rapid spam filtering system
License:  ASL 2.0 and LGPLv3 and BSD and MIT and CC0 and zlib
URL:      https://www.rspamd.com/
Source0:  https://github.com/%{name}/%{name}/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:  rspamd.sysusers
Source2:  rspamd.tmpfiles

# see https://bugzilla.redhat.com/show_bug.cgi?id=2043092
%undefine _package_note_flags

%{!?gcc_toolset_enable:
%if 0%{?rhel} && 0%{?rhel} < 10
%global gcc_toolset_enable source /opt/rh/gcc-toolset-15/enable
%else
%global gcc_toolset_enable source /usr/lib/gcc-toolset/15-env.source
%endif
}

BuildRequires: cmake
BuildRequires: gcc-toolset-15-gcc
BuildRequires: gcc-toolset-15-gcc-c++
BuildRequires: gcc-toolset-15-gcc-plugin-annobin
BuildRequires: file-devel
BuildRequires: glib2-devel
BuildRequires: vectorscan-devel
BuildRequires: libcurl-devel
BuildRequires: libicu-devel
BuildRequires: libsodium-devel
BuildRequires: openblas-devel
BuildRequires: lapack-devel
BuildRequires: openssl-devel
BuildRequires: pcre2-devel
BuildRequires: libzstd-devel
BuildRequires: ragel-devel
BuildRequires: fasttext-devel
BuildRequires: perl
BuildRequires: perl-Digest-MD5
BuildRequires: systemd-units
BuildRequires: systemd-rpm-macros
BuildRequires: sqlite-devel
BuildRequires: zlib-devel
BuildRequires: libarchive-devel

Requires: vectorscan
Requires: openblas
Requires: zlib
Requires: fasttext-libs

%{?systemd_requires}
%{?sysusers_requires_compat}

%description
Rspamd is a rapid, modular and lightweight spam filter. It is designed to work
with big amount of mail and can be easily extended with own filters written in
lua.

%prep
%{gcc_toolset_enable}

%setup -n %{name}-%{version} -q

rm -rf centos
rm -rf debian
rm -rf docker
rm -rf freebsd

rm -fr %{_builddir}/luajit-src || true
rm -fr %{_builddir}/luajit-build || true
git clone -b v2.1 https://luajit.org/git/luajit-2.0.git %{_builddir}/luajit-src

pushd %{_builddir}/luajit-src && make clean && make %{?_smp_mflags} CC="gcc -fPIC" PREFIX=%{_builddir}/luajit-build && make install PREFIX=%{_builddir}/luajit-build
popd
rm -f %{_builddir}/luajit-build/lib/*.so || true

%cmake \
  -DDEBIAN_BUILD=0 \
  -DCMAKE_BUILD_TYPE=RelWithDebInfo \
  -DENABLE_LTO=ON \
  -DLINKER_NAME=/usr/bin/ld.bfd \
  -DNO_SHARED=ON \
  -DCONFDIR=%{_sysconfdir}/%{name} \
  -DMANDIR=%{_mandir} \
  -DDBDIR=%{_localstatedir}/lib/rspamd \
  -DRUNDIR=%{_rundir}/%{name} \
  -DLOGDIR=%{_localstatedir}/log/%{name} \
  -DSHAREDIR=%{_datadir}/%{name} \
  -DLIBDIR=%{_libdir}/%{name}/ \
  -DSYSTEMDDIR=%{_unitdir} \
  -DWANT_SYSTEMD_UNITS=OFF \
  -DRSPAMD_USER=%{name} \
  -DRSPAMD_GROUP=%{name} \
  -DENABLE_HYPERSCAN=ON \
  -DENABLE_LUAJIT=ON \
  -DLUA_ROOT=%{_builddir}/luajit-build \
  -DENABLE_FASTTEXT=ON \
  -DENABLE_JEMALLOC=ON \
  -DENABLE_OPTIMIZATION=ON \
  -DENABLE_PCRE2=ON \
  -DSYSTEM_ZSTD=ON \
  -DENABLE_BLAS=ON \
  -DINSTALL_WEBUI=OFF \
  -DRSPAMD_USER=%{name}
%cmake_build

%pre
%sysusers_create_compat %{SOURCE1}

%install
%cmake_install
# The tests install some files we don't want so ship
rm -f %{buildroot}%{_libdir}/debug/usr/bin/rspam*
#mkdir -p %{buildroot}{%{_localstatedir}/log,%{_rundir}}/%{name}/
#install -Ddm 0755 %{buildroot}%{_sysconfdir}/%{name}/{local,override}.d/

# systemd
install -p -D -m 0644 %{SOURCE1} %{buildroot}%{_sysusersdir}/%{name}.conf
install -p -D -m 0644 %{SOURCE2} %{buildroot}%{_tmpfilesdir}/%{name}.conf

%files
%exclude %{_sysconfdir}/%{name}/*
%exclude %{_mandir}

%{_bindir}/rspam{adm,c,d}{,-%{version}}
%{_bindir}/rspamd_stats
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/effective_tld_names.dat
%dir %{_datadir}/%{name}/{languages,plugins,rules,rules/controller,rules/regexp,lualib}
%{_datadir}/%{name}/languages/*
%{_datadir}/%{name}/plugins/*.lua
%{_datadir}/%{name}/rules/*.lua
%{_datadir}/%{name}/rules/controller/*.lua
%{_datadir}/%{name}/rules/regexp/*.lua
%{_datadir}/%{name}/lualib/*.lua
%dir %{_datadir}/%{name}/lualib/{lua_content,lua_ffi,lua_magic,lua_scanners,lua_selectors,lua_shape,plugins,rspamadm,redis_scripts}
%{_datadir}/%{name}/lualib/{lua_content,lua_ffi,lua_magic,lua_scanners,lua_selectors,lua_shape,plugins,rspamadm,redis_scripts}/*.lua
%{_datadir}/%{name}/lualib/plugins/neural/providers/*.lua
%{_libdir}/%{name}/*
%dir %{_sysconfdir}/%{name}
%{_sysusersdir}/%{name}.conf
%{_tmpfilesdir}/%{name}.conf
