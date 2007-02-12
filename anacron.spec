# TODO
# - missing /etc/cron.hourly processing!!!!
# - doesn't obsolete other crondaemons like other Provides: crondaemons do.
Summary:	A cron-like program that can run jobs lost during downtime
Summary(pl.UTF-8):   Wersja crona z możliwością uruchamiania zapomnianych procesów
Summary(pt_BR.UTF-8):   Auxiliar do cron para máquinas que não ficam ligadas o tempo todo
Name:		anacron
Version:	2.3
Release:	26
License:	GPL
Group:		Daemons
Source0:	http://dl.sourceforge.net/anacron/%{name}-%{version}.tar.gz
# Source0-md5:	865cc1dfe1ed75c470d3e6de13763f03
Source1:	%{name}tab
Source2:	%{name}.init
Patch0:		%{name}-SIGTERM.patch
Patch1:		%{name}-sendmail.patch
Patch2:		%{name}-content-type.patch
Patch3:		%{name}-mailto.patch
Patch4:		%{name}-noconst.patch
URL:		http://anacron.sourceforge.net/
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(post,preun):	/sbin/chkconfig
Requires:	/usr/lib/sendmail
Requires:	rc-scripts
Provides:	crondaemon
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

This package is pre-configured to execute the daily jobs of the PLD
Linux system. You should install this program if your system isn't
powered on 24 hours a day to make sure the maintenance jobs of other
PLD Linux packages are executed each day.

%description -l pl.UTF-8
Anacron (od ,,anac(h)ronistic'') zajmuje się okresowym wykonywaniem
poleceń. Wykonuje je w odstępach będących wielokrotnością dni. W
przeciwieństwie do crona nie zakłada, że system działa 24 godziny na
dobę. Dzięki temu może być używany do wykonywania codziennych,
cotygodniowych i comiesięcznych (lub innych powtarzających się co ileś
dni) zadań w systemach, które nie są włączone non-stop. Zainstalowany
i poprawnie skonfigurowany Anacron zapewni wykonywanie zleconych zadań
tak blisko wyznaczonych terminów, jak tylko możliwe.

Ten pakiet został wstępnie skonfigurowany do działania w systemie PLD
Linux. Powinieneś zainstalować ten program na systemach, które nie są
włączone non-stop aby zapewnić uruchamianie różnych zadań
utrzymujących system we właściwych odstępach czasu.

%description -l pt_BR.UTF-8
Anacron é uma agenda para marcar a execução de comandos em horários
programados. Ao contrário do cron, o anacron não requer que o sistema
esteja rodando continuamente, podendo ser executado em sistemas que
não estão ligados 24 horas por dia.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build
%{__make} \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags}"

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
install -d $RPM_BUILD_ROOT%{_sysconfdir}/$i/
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

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add anacron
%service anacron restart "Anacron daemon"

%preun
if [ "$1" = "0" ];then
	%service anacron stop
	/sbin/chkconfig --del anacron
fi

%files
%defattr(644,root,root,755)
%doc ChangeLog README TODO
%attr(755,root,root) %{_sbindir}/anacron
%attr(754,root,root) /etc/rc.d/init.d/*
%config %{_sysconfdir}/anacrontab
%dir /var/spool/anacron/
%attr(750,root,root) %dir %{_sysconfdir}/cron.*
%attr(755,root,root) /etc/cron.daily/0anacron
%attr(755,root,root) %{_sysconfdir}/cron.monthly/0anacron
%attr(755,root,root) %{_sysconfdir}/cron.weekly/0anacron
%{_mandir}/man[58]/*
