%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name:           liveusb-creator
Version:        3.11.6
Release:        %mkrel 4
Summary:        A liveusb creator

Group:          System/Configuration/Other
License:        GPLv2
URL:            https://fedorahosted.org/liveusb-creator
Source0:        https://fedorahosted.org/releases/l/i/liveusb-creator/%{name}-%{version}.tar.bz2
Source1:	releases.py
Source2:	liveusb-header.png
Source3:	mandrivausb.png
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

BuildArch:      noarch
ExcludeArch:    ppc
ExcludeArch:    ppc64

BuildRequires:  python-devel, python-setuptools, python-qt4-devel, desktop-file-utils gettext
Requires:       syslinux, python-qt4, usermode, isomd5sum
Requires:       python-urlgrabber python-dbus
Requires:       python-parted >= 2.0

%description
A liveusb creator from Live Mandriva images

%prep
%setup -q

#replace Fedora for Mandriva
sed -i 's/fedorausb.png/mandrivausb.png/' data/liveusb-creator.desktop

for a in data/*; do
sed -i 's/Fedora/Mandriva/g' $a
done

for a in liveusb/*.py; do
sed -i 's/Fedora/Mandriva/g' $a
done

for a in po/*.po; do
sed -i 's/Fedora/Mandriva/g' $a
done

cp -f %{SOURCE1} liveusb/
cp -f %{SOURCE2} data/
cp -f %{SOURCE3} data/

rm -f liveusb/resources_rc.py

%build
pyrcc4 data/resources.qrc -o liveusb/resources_rc.py
%{__python} setup.py build
make mo
make mo

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

desktop-file-install --vendor="fedora"                    \
--dir=%{buildroot}%{_datadir}/applications           \
%{buildroot}/%{_datadir}/applications/liveusb-creator.desktop
rm -rf %{buildroot}/%{_datadir}/applications/liveusb-creator.desktop

%find_lang %{name}

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc README.txt LICENSE.txt
%{python_sitelib}/*
%{_bindir}/%{name}
%{_sbindir}/%{name}
%{_datadir}/applications/fedora-liveusb-creator.desktop
%{_datadir}/pixmaps/fedorausb.png
#%{_datadir}/locale/*/LC_MESSAGES/liveusb-creator.mo
%config(noreplace) %{_sysconfdir}/pam.d/%{name}
%config(noreplace) %{_sysconfdir}/security/console.apps/%{name}

