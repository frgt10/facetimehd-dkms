%global commit      805d8654f068c7c4078c550f1d8d9c629d63f157
%global commitdate  20260417
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global srcname     facetimehd

Name:           %{srcname}
Version:        0.7.0.1
Release:        %{commitdate}git%{shortcommit}%{?dist}
Summary:        DKMS package for Broadcom 1570 PCIe FaceTime HD webcam
License:        GPLv2
URL:            https://github.com/patjak/facetimehd/
Source0:        %{URL}/archive/%{commit}.tar.gz

BuildArch:      noarch
BuildRequires:  systemd-rpm-macros
Requires:       dkms >= 1.00
Requires:       bash
Requires:       systemd

%description
This package contains the source code for the facetimehd kernel module
wrapped for the DKMS (Dynamic Kernel Module Support) framework.
Note: This driver requires firmware to be installed separately.

%prep
%autosetup -n %{srcname}-%{commit}

%install
# Install source code to /usr/src/facetimehd-0.7.0.1
mkdir -p %{buildroot}%{_usrsrc}/%{name}-%{version}
cp -r . %{buildroot}%{_usrsrc}/%{name}-%{version}

# Create configuration for automatic module loading at boot
mkdir -p %{buildroot}%{_modulesloaddir}
echo "facetimehd" > %{buildroot}%{_modulesloaddir}/%{name}.conf

%files
%license LICENSE
%doc README.md
%{_usrsrc}/%{name}-%{version}
%config(noreplace) %{_modulesloaddir}/%{name}.conf

%post
# Register and build the module via DKMS
dkms add -m %{name} -v %{version} --rpm_safe_upgrade || :
dkms build -m %{name} -v %{version} || :
dkms install -m %{name} -v %{version} || :

%preun
# Remove all versions of the module during uninstallation
dkms remove -m %{name} -v %{version} --all --rpm_safe_upgrade || :

%changelog
* Sun Apr 19 2026 Stanislav Ashirov <stas.ashirov@gmail.com> - 0.7.0.1-20260417git805d865%{?dist}
- Optimized SPEC for COPR: added %%{?dist} and path macros
- Added support for external patches via %%autosetup
- Set BuildArch to noarch for universal deployment

* Wed May 13 2020 Stanislav Ashirov <stas.ashirov@gmail.com> - 0.1
- Initial RPM release
