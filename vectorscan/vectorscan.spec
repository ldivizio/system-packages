%global __cmake_in_source_build 1
%global debug_package   %{nil}
%define _build_id_links none

Name:    vectorscan
Version: 5.4.12
Release: 1%{?dist}
Summary: High-performance regular expression matching library

# Automatically converted from old format: BSD - review is highly recommended.
License: LicenseRef-Callaway-BSD
URL:     https://www.vectorcamp.gr/project/vectorscan
Source0: https://github.com/VectorCamp/%{name}/archive/refs/tags/vectorscan/%{version}.tar.gz

BuildRequires:  gcc-toolset-15-gcc
BuildRequires:  gcc-toolset-15-gcc-c++
BuildRequires:  gcc-toolset-15-gcc-plugin-annobin
BuildRequires:  boost-devel
BuildRequires:  cmake
BuildRequires:  pcre2-devel
BuildRequires:  python3
BuildRequires:  ragel
BuildRequires:  sqlite-devel >= 3.0
BuildRequires:  libpcap-devel

#package requires SSE support and fails to build on non x86_64 archs
ExclusiveArch: x86_64

%description
Vectorscan is a high-performance multiple regex matching library. It
follows the regular expression syntax of the commonly-used libpcre
library, but is a standalone library with its own C API.

Vectorscan uses hybrid automata techniques to allow simultaneous
matching of large numbers (up to tens of thousands) of regular
expressions and for the matching of regular expressions across streams
of data.

Vectorscan is typically used in a DPI library stack.

%package devel
Summary: Libraries and header files for the vectorscan library
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
Vectorscan is a high-performance multiple regex matching library. It
follows the regular expression syntax of the commonly-used libpcre
library, but is a standalone library with its own C API.

Vectorscan uses hybrid automata techniques to allow simultaneous
matching of large numbers (up to tens of thousands) of regular
expressions and for the matching of regular expressions across streams
of data.

Vectorscan is typically used in a DPI library stack.

This package provides the libraries, include files and other resources
needed for developing Vectorscan applications.

%prep
%setup -n %{name}-%{name}-%{version}

%build
source /opt/rh/gcc-toolset-15/enable

# LTO seems to be losing the target prefix on ifunc targets leading to
# multiply defined symbols.  This seems like a GCC bug
# Disable LTO
%define _lto_cflags %{nil}
%cmake \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_C_FLAGS="-fpic -fPIC" \
  -DCMAKE_CXX_FLAGS="-fPIC -fpic" \
  -DBUILD_SHARED_LIBS:BOOL=ON \
  -DBUILD_STATIC_AND_SHARED:BOOL=OFF \
  -DFAT_RUNTIME=ON \
  -DPCRE_SUPPORT_LIBBZ2=OFF .
%cmake_build

%install
%cmake_install

%files
%exclude %{_defaultdocdir}/%{name}/
%{_libdir}/*.so.*

%files devel
%{_libdir}/*.so
%{_libdir}/pkgconfig/libhs.pc
%{_includedir}/hs/

%changelog
