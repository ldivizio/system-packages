%global debug_package %{nil}
%define _build_id_links none

%if 0%{?rhel} && 0%{?rhel} < 10
%global gcc_toolset_enable source /opt/rh/gcc-toolset-15/enable
%else
%global gcc_toolset_enable source /usr/lib/gcc-toolset/15-env.source
%endif

Name:     libtlsrpt
Version:  0.5.0
Release:  1%{?dist}
Summary:  Interface library to implement TLSRPT reporting into an MTA and to generate and submit TLSRPT reports.

License:  LGPLv3+
URL:      https://github.com/sys4/libtlsrpt
Source0:  %{url}/releases/download/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  gcc-toolset-15-gcc
BuildRequires:  gcc-toolset-15-gcc-plugin-annobin
BuildRequires:  gcc-toolset-15-gcc-c++

%description
Interface library to implement TLSRPT reporting into an MTA and to generate and submit TLSRPT reports.
The libtlsrpt library sends the data to the TLSRPT-collectd daemon which collects and pre-aggregates the report data.

%package  devel
Summary:  Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%autosetup

%build
%{gcc_toolset_enable}

%configure --disable-static
%make_build

%install
rm -rf $RPM_BUILD_ROOT
%make_install
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%exclude %{_mandir}
%{_libdir}/*.so.*

%files devel
%{_includedir}/*
%{_libdir}/*.so


%changelog
%autochangelog
