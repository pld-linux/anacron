Summary:	A cron-like program that can run jobs lost during downtime
Summary(pl):	Wersja crona z mo¿liwo¶ci± uruchamiania zapomnianych procesów
Name:		anacron
Version:	2.3
Release:	10
License:	GPL
Group:		Daemons
Group(de):	Server
Group(pl):	Serwery
Source0:	%{name}-%{version}.tar.gz
Source1:	%{name}tab
Source2:	%{name}.init
Requires:	/bin/sh
Prereq:		/sbin/chkconfig
Provides:	crondaemon
Provides:	crontabs
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Obsoletes:	vixie-cron
Obsoletes:	hc-cron

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
uruchamianie procesów które normalnie by siê nie wykona³y na przyk³ad
z powodu wy³±czenia maszyny. Jest to doskona³e rozwi±zanie dla
komputerów domowych które nie s± w³±czone 24h na dobê. Uwaga - anacron
nie zastêpuje crona a jedynie go wspomaga! Nie ma na przyk³ad
mo¿liwo¶ci uruchamiania procesów np co godzinê.

%prep
%setup -q

%build
%{__make} CFLAGS="%{!?debug:$RPM_OPT_FLAGS}%{?debug:-O -g}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_sbindir},%{_mandir}/man{5,8}} \
	$RPM_BUILD_ROOT/{var/spool/anacron,etc/rc.d/init.d}

install anacron $RPM_BUILD_ROOT%{_sbindir}
install anacron.8 $RPM_BUILD_ROOT%{_mandir}/man8/
install anacrontab.5 $RPM_BUILD_ROOT%{_mandir}/man5/
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}

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

gzip -9nf ChangeLog COPYING README TODO

%post
/sbin/chkconfig --add cron

if [ -f /var/lock/subsys/crond ]; then
	/etc/rc.d/init.d/crond restart >&2
else
	echo "Run \"/etc/rc.d/init.d/crond start\" to start Anacron daemon."
fi

%preun
/sbin/chkconfig --del cron
if [ "$1" = "0" ];then
	if [ -f /var/lock/subsys/crond ]; then
		/etc/rc.d/init.d/crond stop >&2
	fi
	/sbin/chkconfig --del cron
fi

%clean 
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc ChangeLog* COPYING* README* TODO*
%attr(755,root,root) %{_sbindir}/anacron
%attr(754,root,root) /etc/rc.d/init.d/*
%config %{_sysconfdir}/anacrontab
%dir /var/spool/anacron/
%config %{_sysconfdir}/cron.daily/0anacron
%config %{_sysconfdir}/cron.monthly/0anacron
%config %{_sysconfdir}/cron.weekly/0anacron
%{_mandir}/man[58]/*
