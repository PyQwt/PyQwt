# Make sure that you have installed the development packages for PyQt and sip

#define use_system_qwt  0, if you do not want to use the Qwt system library
%define use_system_qwt  1


%{expand:%define buildForMandrake %(if [ -e /etc/mandrake-release ]; then echo 1; else echo 0; fi)}
%{expand:%define buildForSuSE %(if [ -e /etc/SuSE-release ]; then echo 1; else echo 0; fi)}

%{expand: %%define pyver %(python -c 'import sys; print sys.version[:3]')}
%{expand: %%define qtver %(python -c 'import qt; print qt.QT_VERSION_STR')}
%{expand: %%define sipver %(rpm -q sip --qf "%{VERSION}")}

%define name	PyQwt
%define version	4.1
%define release	1
%define qtdir   /usr/lib/qt3

Summary:	Python bindings for Qt.
Name:		%{name}
Version:	%{version}
Release:	%{release}
Copyright:	GPL
Group:		Development/Languages/Python
Source:		%{name}-%{version}.tar.gz
URL:		http://pyqwt.sourceforge.net
BuildRoot:	%{_tmppath}/%{name}-buildroot
BuildRequires:  python >= %{pyver}
BuildRequires:	sip = %{sipver}
Requires:	python >= %{pyver}
Requires:       sip = %{sipver}
%if %buildForMandrake 
BuildRequires:  libqt3-devel = %{qtver}
Requires:       libqt3 = %{qtver}
%endif
%if %buildForSuSE
BuildRequires:  qt3-devel = %{qtver}
Requires:       qt3 = %{qtver}
%endif

%description
PyQwt is a set of Python bindings for the Qwt C++ class library which extends
the Qt framework with widgets for scientific and engineering applications.  It
provides a widget to plot 2-dimensional data and various widgets to display
and control bounded or unbounded floating point values.

%prep
%setup -n %{name}-%{version}

%build
cd configure
%if %use_system_qwt
%if %buildForMandrake
python configure.py -c -j $(getconf _NPROCESSORS_ONLN) \
	-i %qtdir/include/qwt -l %qtdir/lib
%endif
%if %buildForSuSE
python configure.py -c -j $(getconf _NPROCESSORS_ONLN) \
	-i %qtdir/include/qwt -l %{_libdir}
%endif
%else
python configure.py -c -j $(getconf _NPROCESSORS_ONLN)
%endif

make CXX='ccache g++' -j $(getconf _NPROCESSORS_ONLN)

%install
cd configure
make install DESTDIR=%{buildroot}
python \
    %{_libdir}/python%{pyver}/compileall.py \
    -d {_libdir}/python%{pyver}/site-packages/ \
    %{buildroot}/%{_libdir}/python%{pyver}/site-packages/

cd ..
# clean up links for testing
rm examples/{iqt,qwt}
# add Qwt documentation
mkdir -p Doc/html/pyqwt/qwt
cp -p qwt-sources/doc/html/* Doc/html/pyqwt/qwt

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, root, 755)
%doc COPYING COPYING.PyQwt Doc/html examples
%dir %{_datadir}/sip
%{_datadir}/sip/*
%dir %{_libdir}/python%{pyver}/site-packages/iqt/
%dir %{_libdir}/python%{pyver}/site-packages/qwt/
%{_libdir}/python%{pyver}/site-packages/iqt/*
%{_libdir}/python%{pyver}/site-packages/qwt/*

# EOF
