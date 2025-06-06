# Wi-Fi and BT/BLE connectivity Setup over SPI

| Supported Targets | ESP32 | ESP32-S2 | ESP32-S3 | ESP32-C2 | ESP32-C3 | ESP32-C5 | ESP32-C6 |
| ----------------- | ----- | -------- | -------- | -------- | -------- | -------- | -------- |

## 1. Setup
### 1.1 Hardware Setup
In this setup, ESP board acts as a SPI peripheral and provides Wi-Fi capabilities to host. Please connect ESP board to Raspberry-Pi with jumper cables as mentioned below.
It may be good to use small length cables to ensure signal integrity.
Raspberry Pi should be powered with correct incoming power rating.
ESP can be powered through PC using micro-USB/USB-C cable.

Raspberry-Pi pinout can be found [here!](https://pinout.xyz/pinout/spi)

#### 1.1.1 Pin connections
| Raspberry-Pi Pin | ESP32 | ESP32-S2/S3 | ESP32-C2/C3/C5/C6 | Function |
|:-------:|:---------:|:--------:|:--------:|:--------:|
| 24 | IO15 | IO10 | IO10 | CS0 |
| 23 | IO14 | IO12 | IO6 | SCLK |
| 21 | IO12 | IO13 | IO2 | MISO |
| 19 | IO13 | IO11 | IO7 | MOSI |
| 25 | GND | GND | GND | Ground |
| 15 | IO2 | IO2 | IO3 | Handshake |
| 13 | IO4 | IO4 | IO4 | Data Ready |
| 31 | EN  | RST | RST | ESP32 Reset |

Sample SPI setup with ESP32-C6 as slave and RaspberryPi as Host looks like:

![alt text](rpi_esp32_c6_setup.jpg "setup of Raspberry-Pi as host and ESP32-C6 as ESP peripheral")

- Use good quality extremely small (smaller than 10cm) jumper wires, all equal length
- Optionally, Add external pull-up of min 10k Ohm on CS line just to prevent bus floating
- In case of ESP32-S3, For avoidance of doubt, You can power using [UART port](https://docs.espressif.com/projects/esp-idf/en/latest/esp32s3/hw-reference/esp32s3/user-guide-devkitc-1.html#description-of-components)

### 1.2 Raspberry-Pi Software Setup
The SPI master driver is disabled by default on Raspberry-Pi OS. To enable it add following commands in the _/boot/firmware/config.txt_ file (prior to _Bookworm_, the file is at _/boot/config.txt_):
```
dtparam=spi=on
dtoverlay=disable-bt
```

#### 1.2.1 Setting the correct SPI Clock on Raspberry-Pi
By default, the Raspberry Pi sets the CPU scaling governor to `ondemand` (`cat /sys/devices/system/cpu/cpufreq/policy0/scaling_governor` to see the scaling governor currently in use). This causes the SPI clock frequency used to be lower than the requested one.

Setting the scaling governor to `performance` ensure the SPI clock frequency used is close to the requested one.

To change this, edit `/etc/default/cpu_governor` and add this line:
```
CPU_DEFAULT_GOVERNOR="performance"
```
Please reboot Raspberry-Pi after changing this file.

#### 1.2.2. Disable default Wi-Fi interface
Disable the default Wi-Fi network interface (e.g `wlan0`) using networking configuration on your Linux host so that we will be sure that Wi-Fi is only provided with ESP-Hosted.

Every packet would be passed through the ESP-Hosted Wi-Fi interface and not the native onboard Wi-Fi.

## 2. Load ESP-Hosted Solution
### 2.1 Host Software
* Execute following commands in root directory of cloned ESP-Hosted repository on Raspberry-Pi.

```sh
$ cd esp_hosted_fg/host/linux/host_control/
$ ./rpi_init.sh wifi=spi bt=spi spi_mode=3
```

* This script compiles and loads host driver on Raspberry-Pi. It also creates virtual serial interface `/dev/esps0` which is used as a control interface for Wi-Fi on ESP peripheral

Execute `./rpi_init.sh --help` to see the list of options.

> [!NOTE]
> For SPI+UART, use `bt=uart_2pins` or `bt=uart_4pins` for 2/4 pin UART. For wifi only support, exclude the `bt` parameter.

> [!NOTE]
> For ESP32 peripheral, use `spi_mode=2`. For other ESP SOCs, use `spi_mode=3`.

#### 2.1.1 Manually loading and unloading the Kernel Module

Once built, the kernel module `esp32_spi.ko` can be found in `esp_hosted_fg/host/linux/host_driver/esp32`. You can manualy load/unload the module as needed.

To add the module:

`$ sudo insmod esp_hosted_fg/host/linux/host_driver/esp32/esp32_spi.ko resetpin=518 clockspeed=10 spi_bus=0 spi_cs=0 spi_mode=3 spi_handshake=517 spi_dataready=524`

##### Module Parameters

| Parameter | Meaning |
| --- | --- |
| `resetpin` | GPIO to reset the ESP peripheral |
| `clockspeed` | SPI CLK frequency (in MHz) |
| `spi_bus` | SPI bus to use |
| `spi_cs` | SPI CS/CEx to use |
| `spi_mode` | SPI mode to use (2 for ESP32, 3 for all other SOCS) |
| `spi_handshake` | GPIO for Handshake signal |
| `spi_dataready` | GPIO of Data Ready signal |

To remove the module:

`$ sudo rmmod esp32_spi`

### 2.2 ESP Peripheral Firmware
One can load pre-built release binaries on ESP peripheral or compile those from source. Below subsection explains both these methods.

#### 2.2.1 Load Pre-built Release Binaries
* Download pre-built firmware binaries from [releases](https://github.com/espressif/esp-hosted/releases)
* Follow `readme.txt` from release tarball to flash the ESP binary
* :warning: Make sure that you use `Source code (zip)` in `Assets` fold with associated release for host building.
* Windows user can use ESP Flash Programming Tool to flash the pre-built binary.
* Collect firmware log
    * Use minicom or any similar terminal emulator with baud rate 115200 to fetch esp side logs on UART
```sh
$ minicom -D <serial_port>
```
serial_port is device where ESP chipset is detected. For example, /dev/ttyUSB0

#### 2.2.2 Source Compilation

Make sure that same code base (same git commit) is checked-out/copied at both, ESP and Host

##### Set-up ESP-IDF
- **Note on Windows 11**: follow [these instructions](/esp_hosted_fg/esp/esp_driver/setup_windows11.md) to setup ESP-IDF and build the esp firmware.
- You can install the ESP-IDF using the `setup-idf.sh` script (run `./setup-idf.sh -h` for supported options):
```sh
$ cd esp_hosted_fg/esp/esp_driver
$ ./setup-idf.sh
```
- Once ESP-IDF has been installed, set-up the build environment using
```sh
$ . ./esp-idf/export.sh
```

To remove the ESP-IDF installed by `setup-idf.sh`, you can run the `./remove-idf.sh` script.

##### Configure, Build & Flash SPI ESP firmware
* Set slave chipset environment
```
$ cd network_adapter
$ rm -rf sdkconfig build
$ idf.py set-target <esp_chipset>
```

For SPI, <esp_chipset> could be one of `esp32`, `esp32s2`, `esp32s3`, `esp32c2`, `esp32c3`, `esp32c6`, `esp32c5`
* Execute following command to configure the project
```
$ idf.py menuconfig
```
* This will open project configuration window. To select SPI transport interface, navigate to `Example Configuration ->  Transport layer -> SPI interface -> select` and exit from menuconfig.

* For ESP32-C3, select chip revision in addition. Navigate to `Component config → ESP32C3-Specific → Minimum Supported ESP32-C3 Revision` and select chip version of ESP32-C3.

* Use below command to compile and flash the project. Replace <serial_port> with ESP peripheral's serial port.
```
$ idf.py -p <serial_port> build flash
```
* Collect the firmware log using
```
$ idf.py -p <serial_port> monitor
```

> [!NOTE}
> For `esp32c2`, the standard configuration (which runs Wi-Fi and Bluetooth) disables the [Network Split Feature](Network_Split.md) due to lack of memory. There is a customized configuration for `esp32c2`, for wifi-only operation with Network Split enabled. This configuration disables Bluetooth to save memory.
>
> To use this configuration, execute
>
> ```sh
> rm sdkconfig
> idf.py -D SDKCONFIG_DEFAULTS="sdkconfig.defaults;sdkconfig.defaults.esp32c2.wifionly" menuconfig
> ```
>
> Save the configuration. You can now run `idf.py` with the `build`, `flash` and `monitor` options as per normal.

## 3. Checking the Setup

- Firmware log
On successful flashing, you should see following entry in ESP log:

```
[   77.877892] Features supported are:
[   77.877901]   * WLAN
[   77.877906]   * BT/BLE
[   77.877911]     - HCI over SPI
[   77.877916]     - BLE
```

- Host log
    If the transport is setup correctly, you should receive INIT event similar to above from ESP to host in `dmesg` log

**If intended transport is SPI+UART, please continue ahead with UART setup**
