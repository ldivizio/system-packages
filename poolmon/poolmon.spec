%define _etcunitdir     /etc/systemd/system
%define _etctmpfilesdir /etc/tmpfiles.d

Name:      poolmon
Version:   0.6
Release:   1%{?dist}
Summary:   Poolmon is a director mailserver pool monitoring script for Dovecot

License:   GPLv2+        
URL:       https://github.com/HeinleinSupport/poolmon
Source0:   %{name}
Source1:   %{name}.service
#Source2:   %{name}.tmpfilesd
Source4:   %{name}.sysconfig

BuildArch: noarch
Requires:  dovecot
Requires:  perl(IO::Socket::SSL)
Requires:  perl(Net::DNS)

%description
Poolmon is a director mailserver pool monitoring script for Dovecot, meant to
roughly duplicate the functionality of node health monitors on dedicated load-
balancers like Linux LVS or F5 BigIP hardware.

%prep

%build

%install
install -p -D -m 0755 %{S:0} %{buildroot}%{_bindir}/%{name}
install -p -D -m 0644 %{S:1} %{buildroot}%{_etcunitdir}/%{name}.service
install -p -D -m 0644 %{S:4} %{buildroot}%{_sysconfdir}/sysconfig/%{name}

%pre

%preun
%systemd_preun %{name}.service

%post -e
%systemd_post %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_bindir}/%{name}
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%{_etcunitdir}/%{name}.service

%changelog
%autochangelog
