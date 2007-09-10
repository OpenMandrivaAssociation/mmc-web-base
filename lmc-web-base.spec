%define _requires_exceptions pear(graph\\|pear(includes\\|pear(modules
%define _enable_debug_packages %{nil}
%define debug_package          %{nil}

Summary:	LMC web interface to interact with a LMC agent
Name:		lmc-web-base
Version:	2.0.0
Release:	%mkrel 3
License:	GPL
Group:		System/Servers
URL:		http://lds.linbox.org/
Source0:	%{name}-%{version}.tar.gz
Patch0:		lmc-web-base-Makefile_fix.diff
Requires:	apache-mod_php
Requires:	php-xmlrpc
Requires:	php-iconv
Requires(post): rpm-helper
Requires(postun): rpm-helper
BuildArch:      noarch
BuildRequires:  apache-base >= 2.0.54
Buildroot:	%{_tmppath}/%{name}-buildroot

%description
Linbox Management Console web interface designed by Linbox

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

install -d %{buildroot}%{_sysconfdir}/httpd/conf/webapps.d

cat > %{buildroot}%{_sysconfdir}/httpd/conf/webapps.d/%{name}.conf << EOF

Alias /lmc %{_datadir}/lmc

<Directory "%{_datadir}/lmc">
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
%attr(0640,root,apache) %config(noreplace) %{_sysconfdir}/lmc/lmc.ini
%{_datadir}/lmc
