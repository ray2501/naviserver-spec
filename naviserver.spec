#
# spec file for package naviserver
#

Summary:        NaviServer: HTTP server
Name:           naviserver
Version:        4.99.20
Release:        1
License:        MPL-1.1
Group:          Productivity/Networking/Web/Servers
Url:            http://bitbucket.org/naviserver/
BuildRequires:  systemd-rpm-macros
BuildRequires:  shadow
BuildRequires:  tcl-devel
BuildRequires:  zlib-devel
BuildRequires:  openssl-devel
Source0:        %{name}-%{version}.tar.gz
Source1:        naviserver_lib.conf
Source2:        naviserver.service
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%define pkgprefix /var/lib/%name

%description
NaviServer is a versatile multiprotocol (httpd et al) server written
in C/Tcl.  It can be easily extended in either language to create
interesting web sites and services.

%package devel
Summary:        Header Files for NaviServer
Group:          Productivity/Networking/Web/Servers
Requires:       naviserver
Requires:       tcl-devel
Requires:       zlib-devel
Requires:       openssl-devel

%description devel
This package contains header files and documentation needed for writing
and compiling extensions for NaviServer.

%prep
%setup -q
%configure \
        --prefix=%pkgprefix \
        --disable-rpath \
        --enable-64bit \
        --enable-threads \
        --with-tcl=/usr/lib64 \
        --with-zlib=/usr/lib64 \
        --with-openssl=/usr/lib64

# workaround for build error when using GCC 4.8
sed -i s/stack-protector-strong/stack-protector/g include/Makefile.global
sed -i s/stack-clash-protection/stack-protector/g include/Makefile.global

%build
make %{?_smp_mflags}

%install
make DESTDIR=%buildroot install
install -D -m 644 %{S:1} %{buildroot}/etc/ld.so.conf.d/naviserver_lib.conf
install -D -m 644 %{S:2} %{buildroot}%{_unitdir}/naviserver.service

%clean
rm -rf %buildroot

%pre -n naviserver
if ! id -u nsadmin > /dev/null 2>&1; then
    useradd -d/var/lib/naviserver -U -M -s/bin/bash nsadmin
fi
%service_add_pre naviserver.service

%post -n naviserver
%service_add_post naviserver.service
/sbin/ldconfig

%preun -n naviserver
%service_del_preun naviserver.service

%postun -n naviserver
%service_del_postun naviserver.service
/sbin/ldconfig

%files
%defattr(-,root,root,-)
/etc/ld.so.conf.d/naviserver_lib.conf
%{_unitdir}/naviserver.service
%defattr(-,nsadmin,nsadmin,-)
%docdir %pkgprefix/pages/*
%pkgprefix
%config(noreplace) %pkgprefix/conf/*
%exclude %pkgprefix/include

%files devel
%defattr(-,nsadmin,nsadmin,-)
%pkgprefix/include

%changelog

