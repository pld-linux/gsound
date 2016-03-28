#
# Conditional build:
%bcond_without	static_libs	# static library

Summary:	GSound - library for playing system sounds
Summary(pl.UTF-8):	GSound - biblioteka do odtwarzania dźwięków systemowych
Name:		gsound
Version:	1.0.2
Release:	2
License:	LGPL v2.1+
Group:		Applications/System
Source0:	http://ftp.gnome.org/pub/GNOME/sources/gsound/1.0/%{name}-%{version}.tar.xz
# Source0-md5:	c26fd21c21b9ef6533a202a73fab21db
URL:		https://wiki.gnome.org/Projects/GSound
BuildRequires:	glib2-devel >= 1:2.36.0
BuildRequires:	gobject-introspection-devel >= 1.2.9
BuildRequires:	gtk-doc >= 1.20
BuildRequires:	libcanberra-devel
BuildRequires:	pkgconfig
BuildRequires:	tar >= 1:1.22
BuildRequires:	vala >= 2:0.17.2.12
BuildRequires:	vala-libcanberra
BuildRequires:	xz
Requires:	glib2 >= 1:2.36.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
GSound is a small library for playing system sounds. It's designed to
be used via GObject Introspection, and is a thin wrapper around the
libcanberra C library.

%description -l pl.UTF-8
GSound to mała biblioteka do odtwarzania dźwięków systemowych. Jest
zaprojektowana z myślą o używaniu poprzez GObject Introspection i jest
niewielkim obudowaniem biblioteki C libcanberra.

%package devel
Summary:	Header files for GSound library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki GSound
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel >= 1:2.36.0

%description devel
Header files for GSound library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki GSound.

%package static
Summary:	Static GSound library
Summary(pl.UTF-8):	Statyczna biblioteka GSound
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static GSound library.

%description static -l pl.UTF-8
Statyczna biblioteka GSound.

%package apidocs
Summary:	API documentation for GSound library
Summary(pl.UTF-8):	Dokumentacja API biblioteki GSound
Group:		Documentation

%description apidocs
API documentation for GSound library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki GSound.

%package -n vala-gsound
Summary:	Vala API for GSound library
Summary(pl.UTF-8):	API języka Vala do biblioteki GSound
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Requires:	vala >= 2:0.17.2.12
Requires:	vala-libcanberra
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description -n vala-gsound
Vala API for GSound library.

%description -n vala-gsound -l pl.UTF-8
API języka Vala do biblioteki GSound.

%prep
%setup -q

%build
%configure \
	--disable-silent-rules \
	%{!?with_static_libs:--disable-static} \
	--with-html-dir=%{_gtkdocdir}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libgsound.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{_bindir}/gsound-play
%attr(755,root,root) %{_libdir}/libgsound.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgsound.so.0
%{_libdir}/girepository-1.0/GSound-1.0.typelib

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgsound.so
%{_includedir}/gsound*.h
%{_datadir}/gir-1.0/GSound-1.0.gir
%{_pkgconfigdir}/gsound.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libgsound.a
%endif

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/gsound

%files -n vala-gsound
%defattr(644,root,root,755)
%{_datadir}/vala/vapi/gsound.deps
%{_datadir}/vala/vapi/gsound.vapi
