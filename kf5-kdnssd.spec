#
# Conditional build:
%bcond_with	tests		# build with tests
# TODO:
# - runtime Requires if any
%define		kdeframever	5.115
%define		qtver		5.15.2
%define		kfname		kdnssd

Summary:	Network service discovery using Zeroconf
Name:		kf5-%{kfname}
Version:	5.115.0
Release:	1
License:	GPL v2+/LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/frameworks/%{kdeframever}/%{kfname}-%{version}.tar.xz
# Source0-md5:	2327fbcd8dea339ca3ef24b889a71e63
URL:		http://www.kde.org/
BuildRequires:	Qt5Core-devel >= %{qtver}
BuildRequires:	Qt5DBus-devel >= %{qtver}
BuildRequires:	Qt5Gui-devel >= %{qtver}
BuildRequires:	Qt5Network-devel >= %{qtver}
BuildRequires:	Qt5Test-devel >= %{qtver}
BuildRequires:	Qt5Widgets-devel >= %{qtver}
BuildRequires:	Qt5Xml-devel >= %{qtver}
BuildRequires:	avahi-devel
BuildRequires:	cmake >= 3.16
BuildRequires:	kf5-extra-cmake-modules >= 1.4.0
BuildRequires:	ninja
BuildRequires:	qt5-linguist >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	kf5-dirs
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		qt5dir		%{_libdir}/qt5

%description
KDNSSD is a library for handling the DNS-based Service Discovery
Protocol (DNS-SD), the layer of [Zeroconf](http://www.zeroconf.org)
that allows network services, such as printers, to be discovered
without any user intervention or centralized infrastructure.

%package devel
Summary:	Header files for %{kfname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kfname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for %{kfname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kfname}.

%prep
%setup -q -n %{kfname}-%{version}

%build
%cmake -B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON

%ninja_build -C build

%if %{with tests}
%ninja_build -C build test
%endif


%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%find_lang %{kfname}5_qt --with-qm --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f %{kfname}5_qt.lang
%defattr(644,root,root,755)
%doc README.md
%ghost %{_libdir}/libKF5DNSSD.so.5
%attr(755,root,root) %{_libdir}/libKF5DNSSD.so.*.*

%files devel
%defattr(644,root,root,755)
%{_includedir}/KF5/KDNSSD
%{_libdir}/cmake/KF5DNSSD
%{_libdir}/libKF5DNSSD.so
%{qt5dir}/mkspecs/modules/qt_KDNSSD.pri
