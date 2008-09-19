%define _requires_exceptions pear(graph\\|pear(includes\\|pear(modules\\|pear(license.php)
%define _enable_debug_packages %{nil}
%define debug_package          %{nil}

Summary:	MMC web interface to interact with a MMC agent
Name:		mmc-web-base
Version:	2.3.1
Release:	%mkrel 5
License:	GPL
Group:		System/Servers
URL:		http://mds.mandriva.org/
Source0:	%{name}-%{version}.tar.gz
Patch0:		mmc-web-base-Makefile_fix.diff
Patch1:		mmc-web-base-pulse2-1.1.0_fixes.diff
Requires:	apache-mod_php
Requires:	php-xmlrpc
Requires:	php-iconv
Requires:	php-gd
Requires(post): rpm-helper
Requires(postun): rpm-helper
BuildArch:      noarch
BuildRequires:  apache-base >= 2.0.54
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Mandriva Management Console web interface designed by Linbox

%prep

%setup -q -n %{name}-%{version}
for i in `find . -type d -name .svn`; do
    if [ -e "$i" ]; then rm -rf $i; fi >&/dev/null
done

%patch0 -p0
%patch1 -p1

%build

%install
rm -rf %{buildroot}

%makeinstall_std

install -m0644 license.php %{buildroot}%{_datadir}/mmc/

install -d %{buildroot}%{_sysconfdir}/httpd/conf/webapps.d

cat > %{buildroot}%{_sysconfdir}/httpd/conf/webapps.d/%{name}.conf << EOF

Alias /mmc %{_datadir}/mmc

<Directory "%{_datadir}/mmc">
    AllowOverride None
    Order allow,deny
    allow from all
    php_flag short_open_tag on
</Directory>

EOF

%post
%_post_webapp

%postun
%_postun_webapp

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,0755)
%doc COPYING Changelog
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/conf/webapps.d/%{name}.conf
%attr(0640,root,apache) %config(noreplace) %{_sysconfdir}/mmc/mmc.ini
%{_datadir}/mmc
