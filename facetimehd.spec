%global commitdate 20200430
%global commit e989703071246a9d4e6d75e8de34b746b707ecde
%global shortcommit %(c=%{commit}; echo ${c:0:7})

%global srcname bcwc_pcie

%define module facetimehd
%define version 0.1
%define baseurl https://github.com/patjak/

Summary: %{module} %{version} dkms package
Name: %{module}
Version: %{version}
Release: 2dkms
License: GPLv2
Group: System Environment/Kernel
Requires: dkms >= 1.00
Requires: bash
URL: %{baseurl}%{srcname}

Source0: %{baseurl}%{srcname}/archive/%{commit}/%{srcname}-%{version}-%{shortcommit}.tar.gz
Source1: %{baseurl}facetimehd-firmware/archive/master/facetimehd-firmware-master.tar.gz
Source2: facetimehd-modules-load.conf
Source3: facetimehd-dracut.conf

%description
This package contains %{module} module wrapped for the DKMS framework.

%prep
%setup -q -c -T -a 0
mv %{srcname}-%{commit}/ %{module}-%{version}/
%setup -q -T -D -a 1
mv facetimehd-firmware-master/* %{module}-%{version}/firmware/
rm -rf facetimehd-firmware-master

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

mkdir -p $RPM_BUILD_ROOT/etc/dracut.conf.d/
cp $RPM_SOURCE_DIR/facetimehd-dracut.conf $RPM_BUILD_ROOT/etc/dracut.conf.d/facetimehd.conf

mkdir -p $RPM_BUILD_ROOT/etc/modules-load.d/
cp $RPM_SOURCE_DIR/facetimehd-modules-load.conf $RPM_BUILD_ROOT/etc/modules-load.d/facetimehd.conf

%clean
if [ "$RPM_BUILD_ROOT" != "/" ]; then
	rm -rf $RPM_BUILD_ROOT
fi

%files
%defattr(-,root,root)
%config /etc/dracut.conf.d/facetimehd.conf
%config /etc/modules-load.d/facetimehd.conf
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

%changelog

* Wed May 13 2020 Stanislav Ashirov <stas.ashirov@gmail.com>

- Initial RPM release
