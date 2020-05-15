# facetimehd-dkms

DKMS package for [Facetime HD driver](https://github.com/patjak/bcwc_pcie/).

## Installation

You need to manually download and install [firmware](https://github.com/patjak/bcwc_pcie/wiki/Get-Started#firmware-extraction).

## Known issues

* Fedora 32, error load firmware on boot:
    ```
    ]$ dmesg | grep facetimehd
    [    1.910684] facetimehd 0000:04:00.0: Direct firmware load for facetimehd/firmware.bin failed with error -2
    ```
    Add config for dracut:

    ```
    echo 'install_items+="/usr/lib/firmware/facetimehd/firmware.bin"' >> /etc/dracut.conf.d/facetimehd.conf
    ```
