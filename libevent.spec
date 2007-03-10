#
# Conditional build:
%bcond_without	static_libs	# don't build static library
#
Summary:	libevent - an event notification library
Summary(pl.UTF-8):	libevent - biblioteka powiadamiająca o zdarzeniach
Name:		libevent
Version:	1.3b
Release:	1
Epoch:		0
License:	BSD
Group:		Libraries
#Source0Download: http://www.monkey.org/~provos/libevent/
Source0:	http://www.monkey.org/~provos/%{name}-%{version}.tar.gz
# Source0-md5:	7fc864faee87dbe1ed5e34ab8787172c
URL:		http://www.monkey.org/~provos/libevent/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
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
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description devel
Header files for libevent library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libevent.

%package static
Summary:	Static libevent library
Summary(pl.UTF-8):	Statyczna biblioteka libevent
Group:		Development/Libraries
Requires:	%{name}-devel = %{epoch}:%{version}-%{release}

%description static
Static libevent library.

%description static -l pl.UTF-8
Statyczna biblioteka libevent.

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
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
%attr(755,root,root) %{_libdir}/libevent-*.so.*.*.*

%files devel
%defattr(644,root,root,755)
# R: python
#%attr(755,root,root) %{_bindir}/event_rpcgen.py
%attr(755,root,root) %{_libdir}/libevent.so
%{_libdir}/libevent.la
%{_includedir}/ev*.h
%{_mandir}/man3/ev*.3*

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libevent.a
%endif
