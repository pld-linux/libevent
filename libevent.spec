# TODO
# - %attr(755,root,root) %{_bindir}/event_rpcgen.py
#
# Conditional build:
%bcond_without	static_libs	# don't build static library
#
Summary:	libevent - an event notification library
Summary(pl.UTF-8):	libevent - biblioteka powiadamiająca o zdarzeniach
Name:		libevent
Version:	2.0.10
Release:	2
License:	BSD
Group:		Libraries
Source0:	http://www.monkey.org/~provos/%{name}-%{version}-stable.tar.gz
# Source0-md5:	a37401d26cbbf28185211d582741a3d4
Patch0:		%{name}-fpm.patch
Patch1:		%{name}-link.patch
URL:		http://www.monkey.org/~provos/libevent/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	pkgconfig
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

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__automake}
%configure \
	%{!?with_static_libs:--disable-static}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libevent-2.0.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libevent-2.0.so.5
%attr(755,root,root) %{_libdir}/libevent_core-2.0.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libevent_core-2.0.so.5
%attr(755,root,root) %{_libdir}/libevent_extra-2.0.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libevent_extra-2.0.so.5
%attr(755,root,root) %{_libdir}/libevent_openssl-2.0.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libevent_openssl-2.0.so.5
%attr(755,root,root) %{_libdir}/libevent_pthreads-2.0.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libevent_pthreads-2.0.so.5

%files devel
%defattr(644,root,root,755)
# R: python
%attr(755,root,root) %{_bindir}/event_rpcgen.py
%attr(755,root,root) %{_libdir}/libevent.so
%attr(755,root,root) %{_libdir}/libevent_core.so
%attr(755,root,root) %{_libdir}/libevent_extra.so
%attr(755,root,root) %{_libdir}/libevent_openssl.so
%attr(755,root,root) %{_libdir}/libevent_pthreads.so
%{_libdir}/libevent.la
%{_libdir}/libevent_core.la
%{_libdir}/libevent_extra.la
%{_libdir}/libevent_openssl.la
%{_libdir}/libevent_pthreads.la
%dir %{_includedir}/event2
%{_includedir}/event2/*.h
%{_includedir}/evdns.h
%{_includedir}/event*.h
%{_includedir}/evhttp.h
%{_includedir}/evrpc.h
%{_includedir}/evutil.h
#%%{_mandir}/man3/evdns.3*
#%%{_mandir}/man3/event.3*
%{_pkgconfigdir}/libevent.pc
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
