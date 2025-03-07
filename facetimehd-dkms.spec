%global commitdate 20250304
%global commit 499004489f62a6e5669044001f7ca267d2608b55
%global shortcommit %(c=%{commit}; echo ${c:0:7})

%global srcname facetimehd

%define module facetimehd
%define version 0.6.13

Summary: %{module} %{version} dkms package
Name: %{module}
Version: %{version}
Release: %{commitdate}git%{shortcommit}.2dkms
License: GPLv2
Group: System Environment/Kernel
Requires: dkms >= 1.00
Requires: bash
URL: https://github.com/patjak/facetimehd/

Source0: https://github.com/patjak/facetimehd/archive/%{commit}.tar.gz

%description
This package contains %{module} module wrapped for the DKMS framework.

%global debug_package %{nil}
%prep
%setup -q -c -T -a 0

%install
if [ "$RPM_BUILD_ROOT" != "/" ]; then
	rm -rf $RPM_BUILD_ROOT
fi

mkdir -p $RPM_BUILD_ROOT/usr/src/%{module}-%{version}/
cp -rf %{srcname}-%{commit}/* $RPM_BUILD_ROOT/usr/src/%{module}-%{version}/

mkdir -p $RPM_BUILD_ROOT/usr/share/doc/%{module}/
cp %{srcname}-%{commit}/README.md $RPM_BUILD_ROOT/usr/share/doc/%{module}/

mkdir -p $RPM_BUILD_ROOT/etc/modules-load.d/
echo -e "# Load facetimehd.ko at boot\nfacetimehd" > $RPM_BUILD_ROOT/etc/modules-load.d/facetimehd.conf

%clean
if [ "$RPM_BUILD_ROOT" != "/" ]; then
	rm -rf $RPM_BUILD_ROOT
fi

%files
%defattr(-,root,root)
%config /etc/modules-load.d/facetimehd.conf
/usr/src/%{module}-%{version}/
/usr/share/doc/%{module}/

%pre

%post
dkms add -m %{module} -v %{version} --rpm_safe_upgrade

	if [ `uname -r | grep -c "BOOT"` -eq 0 ] && [ -e /lib/modules/`uname -r`/build/include ]; then
		dkms build -m %{module} -v %{version}
		dkms install -m %{module} -v %{version}
	elif [ `uname -r | grep -c "BOOT"` -gt 0 ]; then
		echo -e ""
		echo -e "Module build for the currently running kernel was skipped since you"
		echo -e "are running a BOOT variant of the kernel."
	else
		echo -e ""
		echo -e "Module build for the currently running kernel was skipped since the"
		echo -e "kernel headers for this kernel do not seem to be installed."
	fi
exit 0

%preun
echo -e
echo -e "Uninstall of %{module} module (version %{version}) beginning:"
dkms remove -m %{module} -v %{version} --all --rpm_safe_upgrade
exit 0

%changelog

* Wed May 13 2020 Stanislav Ashirov <stas.ashirov@gmail.com>

- Initial RPM release
