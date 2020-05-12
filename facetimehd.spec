%global commitdate 20200430
%global commit e989703071246a9d4e6d75e8de34b746b707ecde
%global shortcommit %(c=%{commit}; echo ${c:0:7})

%global srcname bcwc_pcie

%define module facetimehd
%define version 0.1
%define url https://github.com/patjak/bcwc_pcie

Summary: %{module} %{version} dkms package
Name: %{module}
Version: %{version}
Release: 2dkms
License: GPLv2
Group: System Environment/Kernel
Requires: dkms >= 1.00
Requires: bash
URL: %{url}

Source0: %{url}/archive/%{commit}/%{srcname}-%{version}-%{shortcommit}.tar.gz
Source1: https://github.com/patjak/facetimehd-firmware/archive/577f143e3be592665988bba7f1eebdabbe2e4177/facetimehd-firmware-577f143.tar.gz

%description
This package contains %{module} module wrapped for the DKMS framework.

%prep
%setup -q -c -T -a 0
mv %{srcname}-%{commit}/ %{module}-%{version}/
%setup -q -T -D -a 1
mv facetimehd-firmware-577f143e3be592665988bba7f1eebdabbe2e4177/* %{module}-%{version}/firmware/
rm -rf facetimehd-firmware-577f143e3be592665988bba7f1eebdabbe2e4177

%install
if [ "$RPM_BUILD_ROOT" != "/" ]; then
	rm -rf $RPM_BUILD_ROOT
fi

pushd %{module}-%{version}/firmware/
make
popd

mkdir -p $RPM_BUILD_ROOT/usr/src/%{module}-%{version}/
cp -rf %{module}-%{version}/* $RPM_BUILD_ROOT/usr/src/%{module}-%{version}/

mkdir -p $RPM_BUILD_ROOT/usr/lib/firmware/%{module}/
cp %{module}-%{version}/firmware/firmware.bin $RPM_BUILD_ROOT/usr/lib/firmware/%{module}/

mkdir -p $RPM_BUILD_ROOT/usr/share/doc/%{module}/
cp %{module}-%{version}/README.md $RPM_BUILD_ROOT/usr/share/doc/%{module}/

%clean
if [ "$RPM_BUILD_ROOT" != "/" ]; then
	rm -rf $RPM_BUILD_ROOT
fi

%files
%defattr(-,root,root)
/usr/src/%{module}-%{version}/
/usr/share/doc/%{module}/
/usr/lib/firmware/%{module}/

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
