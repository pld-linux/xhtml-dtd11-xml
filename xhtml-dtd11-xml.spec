# TODO:
# - maybe separate xhtml-modularization
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

%define		xhtmlver	%{year}%{month}%{day}
%define		modver	20081008
%define		rubyver	20010531

Summary:	XHTML %{v_er}
Summary(pl.UTF-8):	XHTML %{v_er}
Name:		xhtml-dtd%{ver}-xml
Version:	%{xhtmlver}
Release:	1
Group:		Applications/Publishing/SGML
License:	W3C
Vendor:		W3C
Source0:	http://www.w3.org/TR/%{year}/%{type}-xhtml%{mver}-%{xhtmlver}/xhtml%{mver}.tgz
# Source0-md5:	00c3fe896f3d29419dbda4186aa98fe1
Source1:	http://www.w3.org/TR/2008/REC-xhtml-modularization-%{modver}/xhtml-modularization.tgz
# Source1-md5:	404429a5aae9c60382569d4d1b67acc0
Source2:	http://www.w3.org/TR/2001/REC-ruby-%{rubyver}/xhtml-ruby-1.mod
# Source2-md5:	0ea30a78a115139d3dde421227a54b24
URL:		http://www.w3.org/TR/xhtml11/
BuildRequires:	libxml2-progs
Requires(post):	/usr/bin/xmlcatalog
Requires(post):	sgml-common >= 0.5
Requires(preun):	/usr/bin/xmlcatalog
Requires(preun):	sgml-common >= 0.5
Requires:	sgml-common >= 0.6.3-5
Requires:	sgmlparser
AutoReqProv:	no
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		dtddir		%{_datadir}/sgml/html/xml-dtd-%{v_er}
%define		catalog		%{dtddir}/xmlcatalog-%{v_er}-%{version}-%{release}
%define		ccatalog	%{_sysconfdir}/sgml/xhtml-%{v_er}-%{version}-%{release}.cat

%description
XHTML 1.1 specification (with DTD, needed to parse XHTML 1.1 code).

%description -l pl.UTF-8
Specyfikacja XHTML 1.1 (wraz z DTD, potrzebnym do sprawdzania
poprawności kodu XHTML 1.1).

%prep
%setup -q -a1 -n xhtml%{mver}-%{xhtmlver}
rm DTD/VERSION
rm DTD/xml*.dcl
rm xhtml-modularization-%{modver}/DTD/VERSION
rm -r xhtml-modularization-%{modver}/DTD/{examples,templates}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{dtddir},%{_sysconfdir}/sgml}

xmlcatalog --noout --create $RPM_BUILD_ROOT%{catalog}
xmlcatalog --noout --add rewriteSystem \
	'http://www.w3.org/TR/xhtml11/DTD/' \
	'%{dtddir}/' \
	$RPM_BUILD_ROOT%{catalog}
xmlcatalog --noout --add rewriteSystem \
	'http://www.w3.org/TR/xhtml-modularization/DTD/' \
	'%{dtddir}/' \
	$RPM_BUILD_ROOT%{catalog}
xmlcatalog --noout --add rewriteSystem \
	'http://www.w3.org/TR/ruby/' \
	'%{dtddir}/' \
	$RPM_BUILD_ROOT%{catalog}
xmlcatalog --noout -add public \
	'-//W3C//DTD XHTML 1.1//EN' \
	'xhtml11.dtd' \
	$RPM_BUILD_ROOT%{catalog}

install DTD/* xhtml-modularization-%{modver}/DTD/* %{SOURCE2} \
	$RPM_BUILD_ROOT%{dtddir}

touch $RPM_BUILD_ROOT%{ccatalog}

%post
%{_bindir}/install-catalog --add %{ccatalog} %{dtddir}/xhtml11.cat > /dev/null
%{_bindir}/install-catalog --add %{ccatalog} %{dtddir}/xhtml.cat > /dev/null
%{_bindir}/xmlcatalog --noout --add nextCatalog xhtml %{catalog} %{_sysconfdir}/xml/catalog

%preun
%{_bindir}/install-catalog --remove %{ccatalog} %{dtddir}/xhtml11.cat > /dev/null
%{_bindir}/install-catalog --remove %{ccatalog} %{dtddir}/xhtml.cat > /dev/null
%{_bindir}/xmlcatalog --noout --del %{catalog} %{_sysconfdir}/xml/catalog

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc xhtml11.pdf
%ghost %{ccatalog}
%{_datadir}/sgml/html/xml-dtd-%{v_er}
