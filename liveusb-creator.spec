%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name:           liveusb-creator
Version:        3.11.8
Release:        2
Summary:        Tool to create bootable USB sticks from Live CDs

Group:          System/Configuration/Other
License:        GPLv2
URL:            https://fedorahosted.org/liveusb-creator
Source0:        https://fedorahosted.org/releases/l/i/liveusb-creator/%{name}-%{version}.tar.bz2

BuildArch:      noarch
ExcludeArch:    ppc
ExcludeArch:    ppc64

BuildRequires:  python-devel, python-setuptools, python-qt4-devel, desktop-file-utils gettext
Requires:       syslinux, python-qt4, usermode, isomd5sum
Requires:       python-urlgrabber python-dbus
Requires:       python-parted >= 2.0

%description
Tool to create bootable USB sticks from Live CDs

%prep
%setup -q

%build
%{__python} setup.py build
%make mo

%install
rm -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}
%{__rm} -r liveusb/urlgrabber

# Adjust for console-helper magic
mkdir -p %{buildroot}%{_sbindir}
mv %{buildroot}%{_bindir}/%{name} %{buildroot}%{_sbindir}/%{name}
ln -s ../bin/consolehelper %{buildroot}%{_bindir}/%{name}
mkdir -p %{buildroot}%{_sysconfdir}/pam.d
cp %{name}.pam %{buildroot}%{_sysconfdir}/pam.d/%{name}
mkdir -p %{buildroot}%{_sysconfdir}/security/console.apps
cp %{name}.console %{buildroot}%{_sysconfdir}/security/console.apps/%{name}

desktop-file-install --vendor="OpenMandriva" \
	--dir=%{buildroot}%{_datadir}/applications \
	%{buildroot}/%{_datadir}/applications/liveusb-creator.desktop
rm -rf %{buildroot}/%{_datadir}/applications/liveusb-creator.desktop

%find_lang %{name}

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc README.txt LICENSE.txt
%{python_sitelib}/*
%{_bindir}/%{name}
%{_sbindir}/%{name}
%{_datadir}/applications/OpenMandriva-liveusb-creator.desktop
%{_datadir}/pixmaps/fedorausb.png
#%{_datadir}/locale/*/LC_MESSAGES/liveusb-creator.mo
%config(noreplace) %{_sysconfdir}/pam.d/%{name}
%config(noreplace) %{_sysconfdir}/security/console.apps/%{name}
