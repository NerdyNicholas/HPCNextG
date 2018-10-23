Name:          ntp-server
Version:       4.2.8
Release:       1mamba
Summary:       Synchronizes system time using the Network Time Protocol (NTP)
Group:         System/Configuration
Vendor:        openmamba
Distribution:  openmamba
Packager:      Silvan Calarco <silvan.calarco@mambasoft.it>
URL:           http://www.ntp.org
Source0:       http://www.eecis.udel.edu/~ntp/ntp_spool/ntp4/ntp-%{version}.tar.gz
Source1:       ntp.conf
Source2:       ntp.keys
Source3:       ntpd.rc
Source5:       ntpservers
Patch0:        ntp-4.2.6-nano.patch
License:       BSD
## AUTOBUILDREQ-BEGIN
BuildRequires: glibc-devel
BuildRequires: libbeecrypt-devel
BuildRequires: libbzip2-devel
BuildRequires: libcap-devel
BuildRequires: libe2fs-devel
BuildRequires: libelf-devel
BuildRequires: libexpat-devel
BuildRequires: libkrb5-devel
%if "%{stage1}" != "1"
BuildRequires: libnetsnmp-devel
BuildRequires: libnl-devel
BuildRequires: rpm
BuildRequires: libpopt-devel
BuildRequires: libproxy-devel
BuildRequires: libneon-devel
%endif
BuildRequires: libopenssl-devel
BuildRequires: libselinux-devel
BuildRequires: libstdc++6-devel
BuildRequires: libz-devel
BuildRequires: perl-devel
## AUTOBUILDREQ-END
BuildRoot:     %{_tmppath}/%{name}-%{version}-root

%description
The Network Time Protocol (NTP) is used to synchronize a computer's time with another reference time source.
The ntp package contains utilities and daemons which will synchronize your computer's time to Coordinated Universal Time (UTC) via the NTP protocol and NTP servers.
Ntp includes ntpdate (a program for retrieving the date and time from remote machines via a network) and ntpd (a daemon which continuously adjusts system time).

Install the ntp package if you need tools for keeping your system's time synchronized via the NTP protocol.

%prep
%setup -q -n ntp-%{version}
%patch0 -p0

%build
%configure \
   --bindir=%{_sbindir} \
   --with-binsubdir=sbin \
   --with-openssl-libdir=%{_libdir} \
   --enable-all-clocks \
   --enable-parse-clocks \
   --enable-linuxcaps \
   --enable-ipv6

%make \
%if "%{_host}" != "%{_build}"
   LDFLAGS="-lcap -lcrypt -lattr"
%endif

%install
[ "%{buildroot}" != / ] && rm -rf "%{buildroot}"
%makeinstall

install -D -m644 %{S:1} %{buildroot}%{_sysconfdir}/ntp.conf
install -D -m600 %{S:2} %{buildroot}%{_sysconfdir}/ntp/keys
install -D -m755 %{S:3} %{buildroot}%{_initrddir}/ntpd
install -D -m644 %{S:5} %{buildroot}%{_sysconfdir}/ntp/ntpservers

%clean
[ "%{buildroot}" != / ] && rm -rf "%{buildroot}"

%post
if [ $1 -eq 1 ]; then
   /sbin/chkconfig --add ntpd
fi
exit 0

%preun
if [ $1 -eq 0 ]; then
# uninstall
   service ntpd stop
   /sbin/chkconfig --del ntpd
fi
exit 0

%postun
if [ $1 -eq 1 ]; then
#update
   service ntpd condrestart
fi
exit 0

%files
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/ntp.conf
%config(noreplace) %{_sysconfdir}/ntp/keys
%config %{_sysconfdir}/ntp/ntpservers
%{_initrddir}/ntpd
%{_sbindir}/calc_tickadj
%{_sbindir}/ntp-keygen
%{_sbindir}/ntp-wait
%{_sbindir}/ntpdate
%{_sbindir}/ntpd
%{_sbindir}/ntpdc
%{_sbindir}/ntpq
%if "%{stage1}" != "1"
%{_sbindir}/ntpsnmpd
%endif
%{_sbindir}/ntptime
%{_sbindir}/ntptrace
%{_sbindir}/sntp
%{_sbindir}/tickadj
%dir %{_datadir}/ntp
%dir %{_datadir}/ntp/lib
%dir %{_datadir}/ntp/lib/NTP
%{_datadir}/ntp/lib/NTP/Util.pm
%dir %{_docdir}/ntp4
%{_docdir}/ntp4/*.html
%dir %{_docdir}/ntp4/html
%{_docdir}/ntp4/html/*
%{_docdir}/sntp/sntp.html
%{_mandir}/man1/calc_tickadj.1*
%{_mandir}/man1/ntp-wait.1*
%{_mandir}/man1/ntptrace.1*
%{_mandir}/man5/ntp.conf.5*
%{_mandir}/man5/ntp.keys.5*
%{_mandir}/man1/ntp-keygen.*
%{_mandir}/man1/ntpd.*
%{_mandir}/man1/ntpdc.*
%{_mandir}/man1/ntpsnmpd.*
%{_mandir}/man1/ntpq.*
%{_mandir}/man1/sntp.*
%doc COPYRIGHT
#%doc ChangeLog NEWS *.y2kfixes README* TODO WHERE-TO-START

%changelog
* Thu Jan 29 2015 Automatic Build System <autodist@mambasoft.it> 4.2.8-1mamba
- automatic update by autodist

* Tue May 27 2014 Silvan Calarco <silvan.calarco@mambasoft.it> 4.2.6p5-2mamba
- rebuilt with libnetsnmp 5.7.2

* Thu Jun 14 2012 Automatic Build System <autodist@mambasoft.it> 4.2.6p5-1mamba
- automatic version update by autodist

* Mon Sep 26 2011 Automatic Build System <autodist@mambasoft.it> 4.2.6p4-1mamba
- automatic version update by autodist

* Tue Jan 04 2011 Automatic Build System <autodist@mambasoft.it> 4.2.6p3-1mamba
- automatic update by autodist

* Fri Oct 22 2010 Silvan Calarco <silvan.calarco@mambasoft.it> 4.2.6p2-3mamba
- also source renamed to ntp-server

* Fri Oct 15 2010 Silvan Calarco <silvan.calarco@mambasoft.it> 4.2.6p2-2mamba
- renamed to ntp-server to leave place to chrony on client installations

* Mon Aug 09 2010 Automatic Build System <autodist@mambasoft.it> 4.2.6p2-1mamba
- automatic update by autodist
- initscript: use ntpserver file instead fo step-tickers; start later (99)
- /etc/ntp/ntpserver: updated server list with *.pool.ntp.org and names replaced with IP's
- /etc/ntp/step-tickers: file removed

* Wed Feb 17 2010 Silvan Calarco <silvan.calarco@mambasoft.it> 4.2.6-2mamba
- fixed multicast and authentication configuration keys in ntp.conf to work with recent version

* Sun Jan 10 2010 Silvan Calarco <silvan.calarco@mambasoft.it> 4.2.6-1mamba
- update to 4.2.6
- initscript: stard ntpd with -g option to enable big adjustment on first check

* Fri May 29 2009 Automatic Build System <autodist@mambasoft.it> 4.2.4p7-1mamba
- automatic update by autodist

* Sun Mar 15 2009 Silvan Calarco <silvan.calarco@mambasoft.it> 4.2.4p6-1mamba
- automatic update by autodist

* Wed Dec 10 2008 Silvan Calarco <silvan.calarco@mambasoft.it> 4.2.4p5-1mamba
- update to 4.2.4p5

* Fri Aug 31 2007 Aleph0 <aleph0@openmamba.org> 4.2.4p3-1mamba
- update to 4.2.4p3
- fix action stop in the initscript

* Tue Oct 31 2006 Stefano Cotta Ramusino <stefano.cotta@qilinux.it> 4.2.2p4-1qilnx
- update to version 4.2.2p4 by autospec

* Fri Oct 13 2006 Davide Madrisan <davide.madrisan@qilinux.it> 4.2.2p3-2qilnx
- update to version 4.2.2p3 by autospec
- dropped patch against CAN-2005-2496 (merged upstream)

* Wed Sep 07 2005 Davide Madrisan <davide.madrisan@qilinux.it> 4.2.0a-1qilnx
- update to version 4.2.0a-20050816
- security fix QSA-2005-102 (CAN-2005-2496)

* Tue Feb 08 2005 Silvan Calarco <silvan.calarco@mambasoft.it> 4.2.0-3qilnx
- chkconfig of service on first install

* Tue Nov 30 2004 Silvan Calarco <silvan.calarco@mambasoft.it> 4.2.0-2qilnx
- fixed default configuration of ntp.conf to include /etc/ntp/ntpservers

* Tue Feb 24 2004 Davide Madrisan <davide.madrisan@qilinux.it> 4.2.0-1qilnx
- new version rebuild

* Mon Sep 09 2003 Davide Madrisan <davide.madrisan@qilinux.it> 4.1.1-3qilnx
- fixed the date localization problem in /etc/init.d/ntpd

* Wed Jun 25 2003 Silvan Calarco <silvan.calarco@mambasoft.it> 4.1.1-2qilnx
- changed initscript to support hardware clock synconization

* Wed Jun 25 2003 Silvan Calarco <silvan.calarco@mambasoft.it> 4.1.1-1qilnx
- fixed sysconfdir information

* Fri Apr 18 2003 Mirko Cortillaro <mirko.cortillaro@qinet.it>
- write a spec file for ntp
