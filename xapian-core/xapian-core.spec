%global debug_package %{nil}
%define _build_id_links none

%if 0%{?rhel} && 0%{?rhel} < 10
%global gcc_toolset_enable source /opt/rh/gcc-toolset-15/enable
%else
%global gcc_toolset_enable source /usr/lib/gcc-toolset/15-env.source
%endif

Name:     xapian-core
Version:  1.4.30
Release:  1%{?dist}
Summary:  The Xapian Probabilistic Information Retrieval Library
License:  GPL-2.0-or-later
URL:      https://www.xapian.org/
Source0:  https://www.oligarchy.co.uk/xapian/%{version}/%{name}-%{version}.tar.xz

BuildRequires:  gcc-toolset-15-gcc
BuildRequires:  gcc-toolset-15-gcc-c++
BuildRequires:  gcc-toolset-15-gcc-plugin-annobin
BuildRequires:  libuuid-devel
BuildRequires:  make
BuildRequires:  zlib-devel

%description
Xapian is an Open Source Probabilistic Information Retrieval Library. It
offers a highly adaptable toolkit that allows developers to easily add advanced
indexing and search facilities to applications

%package  libs
Summary:  Xapian search engine libraries
 
%description libs
Xapian is an Open Source Probabilistic Information Retrieval framework. It
offers a highly adaptable toolkit that allows developers to easily add advanced
indexing and search facilities to applications. This package provides the
libraries for applications using Xapian functionality

%package devel
Summary:   Files needed for building packages which use Xapian
Requires:  %{name} = %{version}-%{release}
Requires:  %{name}-libs = %{version}-%{release}
Requires:  libuuid-devel

%description devel
Xapian is an Open Source Probabilistic Information Retrieval framework. It
offers a highly adaptable toolkit that allows developers to easily add advanced
indexing and search facilities to applications. This package provides the
files needed for building packages which use Xapian

%prep
%autosetup -p1

%build
%{gcc_toolset_enable}

%configure

%{make_build}

%install
%{make_install}

# Remove libtool archives
find $RPM_BUILD_ROOT -name '*.la' -delete

# Remove the dev docs, we pick them up below
rm -rf %{buildroot}%{_datadir}/doc/%{name}

%if 0%{?with_tests}
%check
make check %{?_smp_mflags}
%endif

%ldconfig_scriptlets libs

%files
%{_libdir}/libxapian.so.*

%files
%{_bindir}/xapian*
%{_bindir}/quest
%{_bindir}/copydatabase
%{_bindir}/simpleindex
%{_bindir}/simplesearch
%{_bindir}/simpleexpand
%{_datadir}/xapian-core/
%{_mandir}/man1/xapian*
%{_mandir}/man1/quest.1*
%{_mandir}/man1/copydatabase.1*

%files libs
%{_libdir}/libxapian.so.*

%files devel
%doc HACKING PLATFORMS docs/*html docs/apidoc
%{_bindir}/xapian-config
%{_includedir}/xapian
%{_includedir}/xapian.h
%{_libdir}/libxapian.so
%{_libdir}/cmake/xapian
%{_libdir}/pkgconfig/xapian-core.pc
%{_datadir}/aclocal/xapian.m4
%{_mandir}/man1/xapian-config.1*

%changelog
%autochangelog
