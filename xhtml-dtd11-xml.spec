# TODO:
#  - xhtml11.dtd requires http://www.w3.org/TR/xhtml-modularization/
#    to work, should those modules be included here or as separate spec ?
%define		major	1
%define		minor	1
%define		micro	%{nil}
%define		type	REC
%define		year	2001
%define		month	05
%define		day	31

%define		mver	%{major}%{minor}
%define		ver	%{major}%{minor}%{micro}
%define		v_er	%{major}.%{minor}%{micro}
%define		v__er	%{major}\.%{minor}%{micro}
Summary:	XHTML %{v_er}
Summary(pl.UTF-8):	XHTML %{v_er}
Name:		xhtml-dtd%{ver}-xml
Version:	%{year}%{month}%{day}
Release:	0.1
Group:		Applications/Publishing/SGML
License:	W3C
Vendor:		W3C
Source0:	http://www.w3.org/TR/%{year}/%{type}-xhtml%{mver}-%{version}/xhtml%{mver}.tgz
# Source0-md5:	00c3fe896f3d29419dbda4186aa98fe1
URL:		http://www.w3.org/TR/xhtml11/
BuildRequires:	libxml2-progs
Requires:	sgml-common >= 0.6.3-5
Requires:	sgmlparser
Requires(post):	/usr/bin/xmlcatalog
Requires(post):	sgml-common >= 0.5
Requires(preun):	/usr/bin/xmlcatalog
Requires(preun):	sgml-common >= 0.5
AutoReqProv:	no
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		catalog		%{_datadir}/sgml/html/xml-dtd-%{v_er}/xmlcatalog-%{v_er}-%{version}-%{release}

%description
XHTML 1.1 specification (with DTD, needed to parse XHTML 1.1 code).

%description -l pl.UTF-8
Specyfikacja XHTML 1.1 (wraz z DTD, potrzebnym do sprawdzania
poprawności kodu XHTML 1.1).

%prep
%setup -q -n xhtml%{mver}-%{version}
rm DTD/VERSION

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_datadir}/sgml/html/xml-dtd-%{v_er}

xmlcatalog --noout --create $RPM_BUILD_ROOT%{catalog}
xmlcatalog --noout --add rewriteSystem \
	'http://www.w3.org/TR/xhtml11/DTD/' \
	'/usr/share/sgml/html/xml-dtd-%{v_er}/' \
	$RPM_BUILD_ROOT%{catalog}
xmlcatalog --noout -add public \
	"-//W3C//DTD XHTML 1.1//EN" \
	xhtml11.dtd \
	$RPM_BUILD_ROOT%{catalog}
xmlcatalog --noout -add public \
	"-//W3C//DTD XHTML 1.1//EN" \
	xhtml11-flat.dtd \
	$RPM_BUILD_ROOT%{catalog}

install DTD/* $RPM_BUILD_ROOT%{_datadir}/sgml/html/xml-dtd-%{v_er}

%post
/usr/bin/install-catalog --add /etc/sgml/xhtml-%{v_er}-%{version}-%{release}.cat /usr/share/sgml/html/xml-dtd-%{v_er}/xhtml11.cat > /dev/null
/usr/bin/xmlcatalog --noout --add nextCatalog xhtml %{catalog} /etc/xml/catalog

%preun
/usr/bin/install-catalog --remove /etc/sgml/xhtml-%{v_er}-%{version}-%{release}.cat /usr/share/sgml/html/xml-dtd-%{v_er}/xhtml11.cat > /dev/null
/usr/bin/xmlcatalog --noout --del %{catalog} /etc/xml/catalog

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc xhtml11.pdf
%{_datadir}/sgml/html/*
