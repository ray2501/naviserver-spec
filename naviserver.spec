%{!?directory:%define directory /usr}

%define buildroot %{_tmppath}/%{name}

Name:          naviserver
Summary:       NaviServer
Version:       5.0.3
Release:       1
License:       MPLv2.0
Group:         Productivity/Networking/Web/Servers
Source:        %{name}-%{version}.tar.gz
Source1:       nsd.service
Patch0:        nsd-config.tcl.patch
URL:           https://sourceforge.net/projects/naviserver/
BuildRequires: systemd-rpm-macros
BuildRequires: pkgconfig(systemd)
BuildRequires: autoconf
BuildRequires: gcc
BuildRequires: make
BuildRequires: tcl-devel >= 8.6
BuildRequires: pkgconfig(openssl)
BuildRequires: pkgconfig(zlib)
Requires:      tcl >= 8.6
Requires(pre): shadow
BuildRoot:     %{buildroot}
Provides:       group(nsadmin)
Provides:       user(nsadmin)

%description
NaviServer is an extensible web server suited to create scalable websites and services.

%package devel
Summary:        Development package for NaviServer
Group:          Productivity/Networking/Web/Servers

%description devel
This package contains development files for NaviServer.

%prep
%setup -q -n %{name}-%{version}
%patch 0

%build
./configure \
        --prefix=/var/lib/naviserver \
        --with-tcl=/usr/%{_lib} \
        --with-zlib=/usr/%{_lib} \
        --with-openssl=/usr/%{_lib}
make 

%install
make DESTDIR=%{buildroot} install
mkdir -p %{buildroot}%{_unitdir}
install -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/nsd.service

%clean
rm -rf %buildroot

%pre
if getent passwd nsadmin >/dev/null; then
    echo "User nsadmin already created!"
else
    useradd -r -c 'NaviServer' -d/var/lib/naviserver -U -M -s/bin/bash nsadmin
fi


%post
%systemd_post nsd.service

%files
%doc license.terms README.md NEWS
%dir %attr(-,nsadmin,nsadmin) /var/lib/naviserver
%defattr(-,nsadmin,nsadmin)
/var/lib/naviserver/bin 
/var/lib/naviserver/certificates
/var/lib/naviserver/cgi-bin
/var/lib/naviserver/conf 
/var/lib/naviserver/invalid-certificates
/var/lib/naviserver/lib
/var/lib/naviserver/logs
/var/lib/naviserver/modules
/var/lib/naviserver/pages
/var/lib/naviserver/tcl
/var/lib/naviserver/ca-bundle.crt 
%defattr(-,root,root)
%{_unitdir}/nsd.service

%files devel
%defattr(-,nsadmin,nsadmin)
%dir /var/lib/naviserver
/var/lib/naviserver/include
