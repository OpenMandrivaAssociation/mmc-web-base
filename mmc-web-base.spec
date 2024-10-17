%define _requires_exceptions pear(graph\\|pear(includes\\|pear(modules\\|pear(license.php)
%define _enable_debug_packages %{nil}
%define debug_package          %{nil}

Summary:	MMC web interface to interact with a MMC agent
Name:		mmc-web-base
Version:	2.3.2
Release:	%mkrel 3
License:	GPL
Group:		System/Servers
URL:		https://mds.mandriva.org/
Source0:	%{name}-%{version}.tar.gz
Patch0:		mmc-web-base-Makefile_fix.diff
Requires:	apache-mod_php
Requires:	php-xmlrpc
Requires:	php-iconv
Requires:	php-gd
%if %mdkversion < 201010
Requires(post):   rpm-helper
Requires(postun):   rpm-helper
%endif
BuildArch:      noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}

%description
Mandriva Management Console web interface designed by Linbox

%prep

%setup -q -n %{name}-%{version}

for i in `find . -type d -name .svn`; do
    if [ -e "$i" ]; then rm -rf $i; fi >&/dev/null
done

%patch0 -p0

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
%if %mdkversion < 201010
%_post_webapp
%endif

%postun
%if %mdkversion < 201010
%_postun_webapp
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,0755)
%doc COPYING Changelog
%config(noreplace) %{_sysconfdir}/httpd/conf/webapps.d/%{name}.conf
%attr(0640,root,apache) %config(noreplace) %{_sysconfdir}/mmc/mmc.ini
%{_datadir}/mmc
