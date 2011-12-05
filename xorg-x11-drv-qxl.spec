%define tarball xf86-video-qxl
%define moduledir %(pkg-config xorg-server --variable=moduledir )
%define driverdir	%{moduledir}/drivers

%define cvsdate xxxxxxx

Summary:   Xorg X11 qxl video driver
Name:      xorg-x11-drv-qxl
Version:   0.0.12
Release:   2.1%{?dist}
URL:       http://www.x.org
Source0:   http://xorg.freedesktop.org/releases/individual/driver/%{tarball}-%{version}.tar.bz2
Source1:   qxl.xinf
License: MIT
Group:     User Interface/X Hardware Support
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Patch0:    remove-asserts.patch

ExclusiveArch: %{ix86} x86_64

BuildRequires: pkgconfig
BuildRequires: xorg-x11-server-sdk >= 1.1.0-1
BuildRequires: glib2-devel

Requires:  xorg-x11-server-Xorg >= 1.1.0-1

%description 
X.Org X11 qxl video driver.

%prep
%setup -q -n %{tarball}-%{version}
%patch0 -p1 -b .remove-asserts

%build
%configure --disable-static
make

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_datadir}/hwdata/videoaliases
install -m 0644 %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/hwdata/videoaliases

# FIXME: Remove all libtool archives (*.la) from modules directory.  This
# should be fixed in upstream Makefile.am or whatever.
find $RPM_BUILD_ROOT -regex ".*\.la$" | xargs rm -f --

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{driverdir}/qxl_drv.so
%{_datadir}/hwdata/videoaliases/qxl.xinf

%changelog
* Tue Feb 9 2010 Soren Sandmann <ssp@redhat.com> 0.0.12-2.1.el6
- Remove a couple of obsolete asserts(). 

* Tue Feb 9 2010 Soren Sandmann <ssp@redhat.com> 0.0.12-1.1.el6
- Version 0.0.12

* Fri Jan 22 2010 Soren Sandmann <ssp@redhat.com> 0.0.8-1.1.el6
- Version 0.0.8

* Tue Feb 24 2009 Soren Sandmann <ssp@redhat.com> 0.0.1-1.1
- Initial package
