Summary:	libevent - an event notification library
Summary(pl):	libevent - biblioteka powiadamiaj±ca o zdarzeniach
Name:		libevent
Version:	1.0
Release:	1
Epoch:		0
License:	BSD
Group:		Libraries
#Source0Download: http://www.monkey.org/~provos/libevent/
Source0:	http://www.monkey.org/~provos/%{name}-%{version}.tar.gz
# Source0-md5:	312136a01f7a1d7561ed12c702c8a6fb
Patch0:		%{name}-shared.patch
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

%description -l pl
API libevent dostarcza mechanizm do wykonywania funkcji callback,
kiedy nast±pi³o okre¶lone zdarzenie w deskryptorze pliku lub po
okre¶lonym czasie. Ma to na celu zast±pienie asynchronicznych pêtli w
sterowanych zdarzeniami us³ugach sieciowych.

%package devel
Summary:	Header files for libevent library
Summary(pl):	Pliki nag³ówkowe biblioteki libevent
Group:		Development/Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description devel
Header files for libevent library.

%description devel -l pl
Pliki nag³ówkowe biblioteki libevent.

%package static
Summary:	Static libevent library
Summary(pl):	Statyczna biblioteka libevent
Group:		Development/Libraries
Requires:	%{name}-devel = %{epoch}:%{version}-%{release}

%description static
Static libevent library.

%description static -l pl
Statyczna biblioteka libevent.

%prep
%setup -q
%patch -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure
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
%attr(755,root,root) %{_libdir}/lib*.so.*.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_includedir}/*.h
%{_mandir}/man3/*

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
