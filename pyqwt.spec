%{expand: %%define pyver %(python -c 'import sys; print sys.version[:3]')}
%{expand: %%define sipver %(rpm -q sip --qf "%{VERSION}")}
%{expand: %%define qtver %(rpm -q libqt3 --qf "%{VERSION}")}

%define name	PyQwt
%define version	4.0
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
BuildRequires:  libqt3-devel = %{qtver}
Requires:	python >= %{pyver}
Requires:       sip = %{sipver}
Requires:       libqt3 = %{qtver}

%description
PyQwt is a set of Python bindings for the Qwt C++ class library which extends
the Qt framework with widgets for scientific and engineering applications.  It
provides a widget to plot 2-dimensional data and various widgets to display
and control bounded or unbounded floating point values.

%prep
%setup -n %{name}-%{version}

%build
cd configure
python configure.py -c -j $(getconf _NPROCESSORS_ONLN)
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


%changelog
* Sun Jun 27 2004 Gerard Vermeulen <gerard.vermeulen@grenoble.cnrs.fr> 4.0-1
- 4.0

# EOF
