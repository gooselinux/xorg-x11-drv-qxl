%define tarball xf86-video-qxl
%define moduledir %(pkg-config xorg-server --variable=moduledir )
%define driverdir	%{moduledir}/drivers

%define cvsdate xxxxxxx

Summary:   Xorg X11 qxl video driver
Name:      xorg-x11-drv-qxl
Version:   0.0.12
Release:   2.1%{?dist}.1
URL:       http://www.x.org
Source0:   http://xorg.freedesktop.org/releases/individual/driver/%{tarball}-%{version}.tar.bz2
Source1:   qxl.xinf
License: MIT
Group:     User Interface/X Hardware Support
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Patch0:    remove-asserts.patch
Patch1:    0001-Make-non-default-qxl-modes-available.patch
Patch2:    0002-Fix-allocating-a-too-large-fb.patch
Patch3:    0003-Fix-restoration-of-text-mode-font-when-leaving-the-v.patch
Patch4:    0004-Change-default-virtual-size-to-match-the-highest-ava.patch
Patch5:    0005-limit-calculated-virtual-size-to-fit-within-the-fram.patch
Patch6:    0006-Don-t-try-to-switch-back-from-vga-mode-when-our-vt-i.patch

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
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1

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
* Tue Nov  2 2010 Hans de Goede <hdegoede@redhat.com> 0.0.12-2.1.el6_0.1
- Fix crash and vga font corruption when switching vc
  Resolves: rhbz#648935
- Add support for many more resolutions and enable resolutions > 1024x768
  without requiring an xorg.conf
  Resolves: rhbz#648933

* Tue Feb 9 2010 Soren Sandmann <ssp@redhat.com> 0.0.12-2.1.el6
- Remove a couple of obsolete asserts(). 

* Tue Feb 9 2010 Soren Sandmann <ssp@redhat.com> 0.0.12-1.1.el6
- Version 0.0.12

* Fri Jan 22 2010 Soren Sandmann <ssp@redhat.com> 0.0.8-1.1.el6
- Version 0.0.8

* Tue Feb 24 2009 Soren Sandmann <ssp@redhat.com> 0.0.1-1.1
- Initial package
