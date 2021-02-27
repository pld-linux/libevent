# TODO: %{_bindir}/event_rpcgen.py - rename to event_rpcgen?
#
# Conditional build:
%bcond_without	static_libs	# don't build static library
#
Summary:	libevent - an event notification library
Summary(pl.UTF-8):	libevent - biblioteka powiadamiająca o zdarzeniach
Name:		libevent
Version:	2.1.12
Release:	1
License:	BSD
Group:		Libraries
#Source0Download: https://github.com/libevent/libevent/releases
Source0:	https://github.com/libevent/libevent/releases/download/release-%{version}-stable/%{name}-%{version}-stable.tar.gz
# Source0-md5:	b5333f021f880fe76490d8a799cd79f4
Patch0:		%{name}-fpm.patch
Patch1:		%{name}-link.patch
URL:		https://libevent.org/
BuildRequires:	autoconf >= 2.67
BuildRequires:	automake >= 1:1.13
BuildRequires:	libtool >= 2:2.4.2
BuildRequires:	openssl-devel
BuildRequires:	pkgconfig
BuildRequires:	sed >= 4.0
BuildRequires:	zlib-devel
Obsoletes:	libevent-dietlibc
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The libevent API provides a mechanism to execute a callback function
when a specific event occurs on a file descriptor or after a timeout
has been reached. It is meant to replace the asynchronous event loop
found in event-driven network servers.

%description -l pl.UTF-8
API libevent dostarcza mechanizm do wykonywania funkcji callback,
kiedy nastąpiło określone zdarzenie w deskryptorze pliku lub po
określonym czasie. Ma to na celu zastąpienie asynchronicznych pętli w
sterowanych zdarzeniami usługach sieciowych.

%package devel
Summary:	Header files for libevent library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libevent
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	openssl-devel

%description devel
Header files for libevent library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libevent.

%package static
Summary:	Static libevent library
Summary(pl.UTF-8):	Statyczna biblioteka libevent
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libevent library.

%description static -l pl.UTF-8
Statyczna biblioteka libevent.

%prep
%setup -q -n %{name}-%{version}-stable
%patch0 -p1
%patch1 -p1

%{__sed} -i -e '1s,/usr/bin/env python$,%{__python3},' \
	event_rpcgen.py \
	test/check-dumpevents.py

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules \
	%{!?with_static_libs:--disable-static}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/%{_lib}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__mv} $RPM_BUILD_ROOT%{_libdir}/libevent-2.1.so.* $RPM_BUILD_ROOT/%{_lib}
ln -sf /%{_lib}/$(basename $RPM_BUILD_ROOT/%{_lib}/libevent-2.1.so.*.*.*) \
	$RPM_BUILD_ROOT%{_libdir}/libevent.so

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libevent*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc ChangeLog* LICENSE
%attr(755,root,root) /%{_lib}/libevent-2.1.so.*.*.*
%attr(755,root,root) %ghost /%{_lib}/libevent-2.1.so.7
%attr(755,root,root) %{_libdir}/libevent_core-2.1.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libevent_core-2.1.so.7
%attr(755,root,root) %{_libdir}/libevent_extra-2.1.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libevent_extra-2.1.so.7
%attr(755,root,root) %{_libdir}/libevent_openssl-2.1.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libevent_openssl-2.1.so.7
%attr(755,root,root) %{_libdir}/libevent_pthreads-2.1.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libevent_pthreads-2.1.so.7

%files devel
%defattr(644,root,root,755)
# R: python3
%attr(755,root,root) %{_bindir}/event_rpcgen.py
%attr(755,root,root) %{_libdir}/libevent.so
%attr(755,root,root) %{_libdir}/libevent_core.so
%attr(755,root,root) %{_libdir}/libevent_extra.so
%attr(755,root,root) %{_libdir}/libevent_openssl.so
%attr(755,root,root) %{_libdir}/libevent_pthreads.so
%{_includedir}/event2
%{_includedir}/evdns.h
%{_includedir}/event.h
%{_includedir}/evhttp.h
%{_includedir}/evrpc.h
%{_includedir}/evutil.h
%{_pkgconfigdir}/libevent.pc
%{_pkgconfigdir}/libevent_core.pc
%{_pkgconfigdir}/libevent_extra.pc
%{_pkgconfigdir}/libevent_openssl.pc
%{_pkgconfigdir}/libevent_pthreads.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libevent.a
%{_libdir}/libevent_core.a
%{_libdir}/libevent_extra.a
%{_libdir}/libevent_openssl.a
%{_libdir}/libevent_pthreads.a
%endif
