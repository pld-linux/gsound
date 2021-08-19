#
# Conditional build:
%bcond_without	apidocs		# API documentation
%bcond_without	static_libs	# static library

Summary:	GSound - library for playing system sounds
Summary(pl.UTF-8):	GSound - biblioteka do odtwarzania dźwięków systemowych
Name:		gsound
Version:	1.0.3
Release:	1
License:	LGPL v2.1+
Group:		Applications/System
Source0:	https://download.gnome.org/sources/gsound/1.0/%{name}-%{version}.tar.xz
# Source0-md5:	7338c295034432a6e782fd20b3d04b68
URL:		https://wiki.gnome.org/Projects/GSound
BuildRequires:	glib2-devel >= 1:2.36.0
BuildRequires:	gobject-introspection-devel >= 1.2.9
%{?with_apidocs:BuildRequires:	gtk-doc >= 1.20}
BuildRequires:	libcanberra-devel
BuildRequires:	meson
BuildRequires:	ninja >= 1.5
BuildRequires:	pkgconfig
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.736
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

%package -n vala-gsound
Summary:	Vala API for GSound library
Summary(pl.UTF-8):	API języka Vala do biblioteki GSound
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Requires:	vala >= 2:0.17.2.12
Requires:	vala-libcanberra
BuildArch:	noarch

%description -n vala-gsound
Vala API for GSound library.

%description -n vala-gsound -l pl.UTF-8
API języka Vala do biblioteki GSound.

%package apidocs
Summary:	API documentation for GSound library
Summary(pl.UTF-8):	Dokumentacja API biblioteki GSound
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for GSound library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki GSound.

%prep
%setup -q

%build
%meson build \
	%{!?with_static_libs:--default-library=shared} \
	%{?with_apidocs:-Dgtk_doc=true}

%ninja_build -C build

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_bindir}/gsound-play
%attr(755,root,root) %{_libdir}/libgsound.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgsound.so.0
%{_libdir}/girepository-1.0/GSound-1.0.typelib
%{_mandir}/man1/gsound-play.1*

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

%files -n vala-gsound
%defattr(644,root,root,755)
%{_datadir}/vala/vapi/gsound.deps
%{_datadir}/vala/vapi/gsound.vapi

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/gsound-%{version}
%endif
