Summary:	A cron-like program that can run jobs lost during downtime
Summary(pl):	Wersja crona z mo¿liwo¶ci± uruchamiania zapomnianych procesów
Name:		anacron
Version:	2.1
Release:	6
License:	GPL
Group:		Daemons
Source0:	%{name}-%{version}.tar.bz2
Source1:	anacrontab
Source2:	anacron.init
Requires:	/bin/sh
Prereq:		/sbin/chkconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Anacron (like `anac(h)ronistic') is a periodic command scheduler. It
executes commands at intervals specified in days. Unlike cron, it does
not assume that the system is running continuously. It can therefore
be used to control the execution of daily, weekly and monthly jobs (or
anything with a period of n days), on systems that don't run 24 hours
a day. When installed and configured properly, Anacron will make sure
that the commands are run at the specified intervals as closely as
machine-uptime permits.

This package is pre-configured to execute the daily jobs of the Red
Hat Linux system. You should install this program if your system isn't
powered on 24 hours a day to make sure the maintenance jobs of other
Red Hat Linux packages are executed each day.

%description -l pl
cron to standardowy unixowy program, okresowo uruchamiaj±cy zadane
przez u¿ytkowników programy. anacron jest wersj± crona umo¿liwiaj±c±
uruchamianie procesów które normalnie by siê nie wykona³y z powodu
wy³±czenia maszyny. Jest to doskona³e rozwi±zanie dla komputerów
domowych które nie s± w³±czone 24h na dobê. Uwaga - anacron nie
zastêpuje crona a jedynie go wspomaga! Nie ma mo¿liwo¶ci uruchamiania
procesów np co godzinê

%prep
%setup -q

%build
%{__make} CFLAGS="$RPM_OPT_FLAGS"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%_{sbindir},%{_mandir}/man{5,8}} \
	$RPM_BUILD_ROOT/{var/spool/anacron,etc/rc.d/init.d}

install -s anacron $RPM_BUILD_ROOT%{_sbindir}
install anacron.8 $RPM_BUILD_ROOT%{_mandir}/man8/
install anacrontab.5 $RPM_BUILD_ROOT%{_mandir}/man5/
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/anacron

for i in cron.daily cron.weekly cron.monthly; do
install  -d $RPM_BUILD_ROOT%{_sysconfdir}/$i/
cat << EOF > $RPM_BUILD_ROOT%{_sysconfdir}/$i/0anacron
#!/bin/sh
#
# anacron's cron script
#
# This script updates anacron time stamps. It is called through run-parts
# either by anacron itself or by cron.
#
# The script is called "0anacron" to assure that it will be executed
# _before_ all other scripts.

anacron -u $i

EOF
done

gzip -9nf $RPM_BUILD_ROOT%{_mandir}/man{5,8}/* \
	NEWS README

%post
/sbin/chkconfig --add anacron

%preun
/sbin/chkconfig --del anacron

%clean 
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc *.gz
%attr(755,root,root) %{_sbindir}/anacron
%attr(754,root,root) /etc/rc.d/init.d/*
%config %{_sysconfdir}/anacrontab
%dir /var/spool/anacron/
%config %{_sysconfdir}/cron.daily/0anacron
%config %{_sysconfdir}/cron.monthly/0anacron
%config %{_sysconfdir}/cron.weekly/0anacron
%{_mandir}/man[58]/*
