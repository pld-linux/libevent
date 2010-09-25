# TODO
# - %attr(755,root,root) %{_bindir}/event_rpcgen.py
# - needs -levent: /usr/lib64/libevent_extra-1.4.so.2.1.3
#
# Conditional build:
%bcond_without	static_libs	# don't build static library
%bcond_without	dietlibc	# don't build static dietlibc library
#
Summary:	libevent - an event notification library
Summary(pl.UTF-8):	libevent - biblioteka powiadamiająca o zdarzeniach
Name:		libevent
Version:	1.4.14b
Release:	2
License:	BSD
Group:		Libraries
Source0:	http://www.monkey.org/~provos/%{name}-%{version}-stable.tar.gz
# Source0-md5:	a00e037e4d3f9e4fe9893e8a2d27918c
Patch0:		%{name}-fpm.patch
Patch1:		%{name}.fb-changes.diff
URL:		http://www.monkey.org/~provos/libevent/
%{?with_dietlibc:BuildRequires:	dietlibc-static >= 2:0.31-5}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# to get backslash, we need to escape it from spec parser. therefore "\\|" not "\|" here
%define		dietarch	%(echo %{_target_cpu} | sed -e 's/i.86\\|pentium.\\|athlon/i386/;s/amd64/x86_64/;s/armv.*/arm/')
%define		dietlibdir	%{_prefix}/lib/dietlibc/lib-%{dietarch}

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

%package dietlibc
Summary:	Static dietlibc libevent library
Summary(pl.UTF-8):	Biblioteka statyczna dietlibc libevent
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description dietlibc
Static dietlibc libevent library.

%description dietlibc -l pl.UTF-8
Biblioteka statyczna dietlibc libevent.

%prep
%setup -q -n %{name}-%{version}-stable
%patch0 -p1
%patch1 -p1

%build
%if %{with dietlibc}
%configure \
	CC="diet %{__cc} %{rpmcflags} %{rpmldflags} -Os -D_BSD_SOURCE -D_EVENT_HAVE_FD_MASK" \
	--enable-static \
	--disable-shared

# libtool sucks, build just the libs
%{__make}
mv .libs/libevent.a diet-libevent.a
mv .libs/libevent_core.a diet-libevent_core.a
mv .libs/libevent_extra.a diet-libevent_extra.a
%{__make} clean
%endif

%configure \
	%{!?with_static_libs:--disable-static}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{?with_dietlibc:install -d $RPM_BUILD_ROOT%{dietlibdir}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%if %{with dietlibc}
install diet-libevent.a $RPM_BUILD_ROOT%{dietlibdir}/libevent.a
install diet-libevent_core.a $RPM_BUILD_ROOT%{dietlibdir}/libevent_core.a
install diet-libevent_extra.a $RPM_BUILD_ROOT%{dietlibdir}/libevent_extra.a
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libevent-1.4.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libevent-1.4.so.2
%attr(755,root,root) %{_libdir}/libevent_core-1.4.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libevent_core-1.4.so.2
%attr(755,root,root) %{_libdir}/libevent_extra-1.4.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libevent_extra-1.4.so.2

%files devel
%defattr(644,root,root,755)
# R: python
#%attr(755,root,root) %{_bindir}/event_rpcgen.py
%attr(755,root,root) %{_libdir}/libevent.so
%attr(755,root,root) %{_libdir}/libevent_core.so
%attr(755,root,root) %{_libdir}/libevent_extra.so
%{_libdir}/libevent.la
%{_libdir}/libevent_core.la
%{_libdir}/libevent_extra.la
%{_includedir}/evdns.h
%{_includedir}/event*.h
%{_includedir}/evhttp.h
%{_includedir}/evrpc.h
%{_includedir}/evutil.h
%{_mandir}/man3/evdns.3*
%{_mandir}/man3/event.3*

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libevent.a
%{_libdir}/libevent_core.a
%{_libdir}/libevent_extra.a
%endif

%if %{with dietlibc}
%files dietlibc
%defattr(644,root,root,755)
%{dietlibdir}/libevent.a
%{dietlibdir}/libevent_core.a
%{dietlibdir}/libevent_extra.a
%endif
