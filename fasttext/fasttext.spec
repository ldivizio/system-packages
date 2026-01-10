%global debug_package   %{nil}
%define _build_id_links none

Name:           fasttext
Version:        0.9.2
Release:        1%{?dist}
Summary:        Library for fast text representation and classification.
License:        MIT
URL:            https://github.com/rspamd/fasttext
Source0:        %{name}-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  pkgconfig

%description
Library for fast text representation and classification.

%package        libs
Summary:        Shared libraries for %{name}

%description    libs
Shared libraries for %{name}

%package        static
Summary:        Static libraries for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    static
Static libraries for %{name}

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The package contains libraries and header files for
developing applications that use %{name}.

%prep
%autosetup

%build
%cmake .
%cmake_build

%install
%cmake_install

%files
%{_bindir}/fasttext

%files libs
%{_libdir}/libfasttext.so*

%files static
%{_libdir}/libfasttext.a
%{_libdir}/libfasttext_pic.a

%files devel
%{_includedir}/fasttext/*
%{_libdir}/pkgconfig/*.pc


%changelog
