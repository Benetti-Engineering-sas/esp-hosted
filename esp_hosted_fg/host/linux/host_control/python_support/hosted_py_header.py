# SPDX-License-Identifier: Apache-2.0
# Copyright 2015-2022 Espressif Systems (Shanghai) PTE LTD
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from ctypes import *
from enum import Enum
import sys

SUCCESS = 0
FAILURE = -1

SUCCESS_STR = "success"
FAILURE_STR = "failure"
STA_INTERFACE = 'ethsta0'
AP_INTERFACE = 'ethap0'

# Do not change these values, these need to be exactly similar to with
# 1. protobuf structs (esp_hosted_config.proto) and
# 2 .structures in ctrl_api.h
SSID_LENGTH = 33
PASSWORD_LENGTH = 65
BSSID_LENGTH = 18
STATUS_LENGTH = 14
MAX_MAC_STR_LEN = 17
VENDOR_OUI_BUF = 3

YES = 1
NO = 0

CTRL_RESP_TIMEOUT_SEC = 5
MIN_TIMESTAMP_STR_SIZE = 30

HEARTBEAT_DURATION_SEC = 20

CALLBACK_SET_SUCCESS = 0
CALLBACK_AVAILABLE = 0
CALLBACK_NOT_REGISTERED = -1
MSG_ID_OUT_OF_ORDER = -2

WIFI_BAND_MODE_2G_ONLY = 1
WIFI_BAND_MODE_5G_ONLY = 2
WIFI_BAND_MODE_AUTO = 3

# Custom RPC request IDs
class CUSTOM_RPC_REQ_ID(Enum):
	ONLY_ACK = 1
	ECHO_BACK_RESPONSE = 2
	ECHO_BACK_AS_EVENT = 3

# Custom RPC event IDs
class CUSTOM_RPC_EVENT_ID(Enum):
	DEMO_ECHO_BACK_REQUEST = 100
	DEMO_SIMPLE_EVENT = 101

class WIFI_MODE_E(Enum):
	WIFI_MODE_NONE = 0
	WIFI_MODE_STA = 1
	WIFI_MODE_AP = 2
	WIFI_MODE_APSTA = 3
	WIFI_MODE_MAX = 4


class WIFI_AUTH_MODE(Enum):
	WIFI_AUTH_OPEN = 0
	WIFI_AUTH_WEP = 1
	WIFI_AUTH_WPA_PSK = 2
	WIFI_AUTH_WPA2_PSK = 3
	WIFI_AUTH_WPA_WPA2_PSK = 4
	WIFI_AUTH_WPA2_ENTERPRISE = 5
	WIFI_AUTH_WPA3_PSK = 6
	WIFI_AUTH_WPA2_WPA3_PSK = 7
	WIFI_AUTH_MAX = 8


class WIFI_BW(Enum):
	WIFI_BW_HT20 = 1
	WIFI_BW_HT40 = 2


class WIFI_PS_MODE(Enum):
	WIFI_PS_NONE = 0
	WIFI_PS_MIN_MODEM = 1
	WIFI_PS_MAX_MODEM = 2
	WIFI_PS_INVALID = 3


class WIFI_VND_IE_TYPE(Enum):
	WIFI_VND_IE_TYPE_BEACON = 0
	WIFI_VND_IE_TYPE_PROBE_REQ = 1
	WIFI_VND_IE_TYPE_PROBE_RESP = 2
	WIFI_VND_IE_TYPE_ASSOC_REQ = 3
	WIFI_VND_IE_TYPE_ASSOC_RESP = 4


class WIFI_VND_IE_ID(Enum):
	WIFI_VND_IE_ID_0 = 0
	WIFI_VND_IE_ID_1 = 1

class HOSTED_FEATURE(Enum):
	HOSTED_FEATURE_INVALID = 0
	HOSTED_FEATURE_WIFI = 1
	HOSTED_FEATURE_BLUETOOTH = 2
	HOSTED_FEATURE_NETWORK_SPLIT = 3

class CTRL_ERR(Enum):
	CTRL_ERR_NOT_CONNECTED = 1
	CTRL_ERR_NO_AP_FOUND = 2
	CTRL_ERR_INVALID_PASSWORD = 3
	CTRL_ERR_INVALID_ARGUMENT = 4
	CTRL_ERR_OUT_OF_RANGE = 5
	CTRL_ERR_MEMORY_FAILURE = 6
	CTRL_ERR_UNSUPPORTED_MSG = 7
	CTRL_ERR_INCORRECT_ARG = 8
	CTRL_ERR_PROTOBUF_ENCODE = 9
	CTRL_ERR_PROTOBUF_DECODE = 10
	CTRL_ERR_SET_ASYNC_CB = 11
	CTRL_ERR_TRANSPORT_SEND = 12
	CTRL_ERR_REQUEST_TIMEOUT = 13
	CTRL_ERR_REQ_IN_PROG = 14
	OUT_OF_RANGE = 15


class CTRL_MSGTYPE(Enum):
	CTRL_MSGTYPE_INVALID = 0
	CTRL_REQ = 1
	CTRL_RESP = 2
	CTRL_EVENT = 3
	CTRL_MSGTYPE_MAX = 4


class CTRL_MSGID(Enum):
	CTRL_MSGID_INVALID = 0
	CTRL_REQ_BASE = 100
	CTRL_REQ_GET_MAC_ADDR = 101
	CTRL_REQ_SET_MAC_ADDR = 102
	CTRL_REQ_GET_WIFI_MODE = 103
	CTRL_REQ_SET_WIFI_MODE = 104
	CTRL_REQ_GET_AP_SCAN_LIST = 105
	CTRL_REQ_GET_AP_CONFIG = 106
	CTRL_REQ_CONNECT_AP = 107
	CTRL_REQ_DISCONNECT_AP = 108
	CTRL_REQ_GET_SOFTAP_CONFIG = 109
	CTRL_REQ_SET_SOFTAP_VND_IE = 110
	CTRL_REQ_START_SOFTAP = 111
	CTRL_REQ_GET_SOFTAP_CONN_STA_LIST = 112
	CTRL_REQ_STOP_SOFTAP = 113
	CTRL_REQ_SET_PS_MODE = 114
	CTRL_REQ_GET_PS_MODE = 115
	CTRL_REQ_OTA_BEGIN = 116
	CTRL_REQ_OTA_WRITE = 117
	CTRL_REQ_OTA_END = 118
	CTRL_REQ_SET_WIFI_MAX_TX_POWER = 119
	CTRL_REQ_GET_WIFI_CURR_TX_POWER = 120
	CTRL_REQ_CONFIG_HEARTBEAT = 121
	CTRL_REQ_ENABLE_DISABLE = 122
	CTRL_REQ_GET_FW_VERSION = 123
	CTRL_REQ_SET_COUNTRY_CODE = 124
	CTRL_REQ_GET_COUNTRY_CODE = 125
	CTRL_REQ_SET_DhcpDnsStatus = 126
	CTRL_REQ_GET_DhcpDnsStatus = 127
	CTRL_REQ_CUSTOM_RPC_UNSERIALISED = 128
	CTRL_REQ_MAX = 129
	CTRL_RESP_BASE = 200
	CTRL_RESP_GET_MAC_ADDR = 201
	CTRL_RESP_SET_MAC_ADDRESS = 202
	CTRL_RESP_GET_WIFI_MODE = 203
	CTRL_RESP_SET_WIFI_MODE = 204
	CTRL_RESP_GET_AP_SCAN_LIST = 205
	CTRL_RESP_GET_AP_CONFIG = 206
	CTRL_RESP_CONNECT_AP = 207
	CTRL_RESP_DISCONNECT_AP = 208
	CTRL_RESP_GET_SOFTAP_CONFIG = 209
	CTRL_RESP_SET_SOFTAP_VND_IE = 210
	CTRL_RESP_START_SOFTAP = 211
	CTRL_RESP_GET_SOFTAP_CONN_STA_LIST = 212
	CTRL_RESP_STOP_SOFTAP = 213
	CTRL_RESP_SET_PS_MODE = 214
	CTRL_RESP_GET_PS_MODE = 215
	CTRL_RESP_OTA_BEGIN = 216
	CTRL_RESP_OTA_WRITE = 217
	CTRL_RESP_OTA_END = 218
	CTRL_RESP_SET_WIFI_MAX_TX_POWER = 219
	CTRL_RESP_GET_WIFI_CURR_TX_POWER = 220
	CTRL_RESP_CONFIG_HEARTBEAT = 221
	CTRL_RESP_ENABLE_DISABLE = 222
	CTRL_RESP_GET_FW_VERSION = 223
	CTRL_RESP_SET_COUNTRY_CODE = 224
	CTRL_RESP_GET_COUNTRY_CODE = 225
	CTRL_RESP_SET_DHCP_DNS_STATUS = 226
	CTRL_RESP_GET_DHCP_DNS_STATUS = 227
	CTRL_RESP_CUSTOM_RPC_UNSERIALISED = 228
	CTRL_RESP_MAX = 229
	CTRL_EVENT_BASE = 300
	CTRL_EVENT_ESP_INIT = 301
	CTRL_EVENT_HEARTBEAT = 302
	CTRL_EVENT_STATION_DISCONNECT_FROM_AP = 303
	CTRL_EVENT_STATION_DISCONNECT_FROM_ESP_SOFTAP = 304
	CTRL_EVENT_STATION_CONNECTED_TO_AP = 305
	CTRL_EVENT_STATION_CONNECTED_TO_ESP_SOFTAP = 306
	CTRL_EVENT_DHCP_DNS_STATUS = 307
	CTRL_EVENT_CUSTOM_RPC_UNSERIALISED_MSG = 308
	CTRL_EVENT_MAX = 309


class STA_CONFIG(Structure):
	_fields_ = [("ssid", c_char * SSID_LENGTH),
			("pwd", c_char * PASSWORD_LENGTH),
			("bssid", c_char * BSSID_LENGTH),
			("is_wpa3_supported", c_bool),
			("rssi", c_int),
			("channel", c_uint),
			("encryption_mode", c_uint),
			("listen_interval", c_ushort),
			("status", c_char * STATUS_LENGTH),
			("out_mac", c_char * MAX_MAC_STR_LEN),
			("band_mode", c_int)]


class SOFTAP_CONFIG(Structure):
	_fields_ = [("ssid", c_char * SSID_LENGTH),
			("pwd", c_char * PASSWORD_LENGTH),
			("channel", c_int),
			("encryption_mode", c_int),
			("max_connections", c_int),
			("ssid_hidden", c_bool),
			("bandwidth", c_uint),
			("out_mac", c_char * MAX_MAC_STR_LEN),
			("band_mode", c_int)]


class CONTROL_CONFIG(Union):
	_fields_ = [("station", STA_CONFIG),
				("softap", SOFTAP_CONFIG)]


class WIFI_SCAN_LIST(Structure):
	_fields_ = [("ssid", c_char * SSID_LENGTH),
			("bssid", c_char * BSSID_LENGTH),
			("rssi", c_int),
			("channel", c_int),
			("encryption_mode", c_int)]


class WIFI_AP_SCAN_LIST(Structure):
	_fields_ = [("count", c_int),
			("out_list", POINTER(WIFI_SCAN_LIST))]


class WIFI_STATIONS_LIST(Structure):
	_fields_ = [("bssid", c_char * BSSID_LENGTH),
			("rssi", c_int)]


class WIFI_CONNECTED_STATIONS_LIST(Structure):
	_fields_ = [("count", c_int),
			("out_list", POINTER(WIFI_STATIONS_LIST))]


class WIFI_MAC(Structure):
	_fields_ = [("mode", c_int),
			("mac", c_char * MAX_MAC_STR_LEN)]


class WIFI_MODE(Structure):
	_fields_ = [("mode", c_int)]


class WIFI_POWER_SAVE_MODE(Structure):
	_fields_ = [("ps_mode", c_int)]


class VENDOR_IE_DATA(Structure):
	_fields_ = [("element_id", c_char),
			("length", c_char),
			("vendor_oui", c_char * VENDOR_OUI_BUF),
			("vendor_oui_type", c_char),
			("payload_len", c_ushort),
			("payload", c_wchar_p)]


class WIFI_SOFTAP_VENDOR_IE(Structure):
	_fields_ = [("enable", c_bool),
			("type", c_int),
			("idx", c_int),
			("vnd_ie", VENDOR_IE_DATA)]

class FEATURE_CONFIG(Structure):
	_fields_ = [("feature", c_int), # represents 'enum HostedFeature'
			("enable", c_uint8)]

class FW_VERSION(Structure):
	_fields_ = [("project_name", c_char * 3),
			("major_1", c_uint8),
			("major_2", c_uint8),
			("minor", c_uint8),
			("revision_patch_1", c_uint8),
			("revision_patch_2", c_uint8)]

class COUNTRY_CODE(Structure):
	_fields_ = [("country", c_char * 3),
			("ieee80211d_enabled", c_bool)]

class OTA_WRITE(Structure):
	_fields_ = [("ota_data", c_char_p),
			("ota_data_len", c_uint)]


class WIFI_TX_POWER(Structure):
	_fields_ = [("power", c_int)]


class EVENT_HEARTBEAT(Structure):
	_fields_ = [("hb_num", c_uint),
			("enable", c_char),
			("duration", c_uint)]


class EVENT_STATION_CONN_TO_AP(Structure):
	_fields_ = [("ssid", c_char * SSID_LENGTH),
			("ssid_len", c_uint),
			("bssid", c_char * BSSID_LENGTH),
			("channel", c_int),
			("authmode", c_int),
			("aid", c_int)]


class EVENT_STATION_DISCONN_FROM_AP(Structure):
	_fields_ = [("ssid", c_char * SSID_LENGTH),
			("ssid_len", c_uint),
			("bssid", c_char * BSSID_LENGTH),
			("reason", c_uint),
			("rssi", c_int)]


class EVENT_STATION_CONN_TO_SOFTAP(Structure):
	_fields_ = [("mac", c_char * MAX_MAC_STR_LEN),
			("aid", c_int),
			("is_mesh_child", c_int)]


class EVENT_STATION_DISCONN_FROM_SOFTAP(Structure):
	_fields_ = [("mac", c_char * MAX_MAC_STR_LEN),
			("aid", c_int),
			("is_mesh_child", c_int),
			("reason", c_uint)]

class EVENT_DHCP_DNS_STATUS(Structure):
	_fields_ = [("iface", c_int),
			("net_link_up", c_int),
			("dhcp_up", c_int),
			("dhcp_ip", c_char * 64),
			("dhcp_nm", c_char * 64),
			("dhcp_gw", c_char * 64),
			("dns_up", c_int),
			("dns_ip", c_char * 64),
			("dns_type", c_int)]

class CUSTOM_RPC_UNSERIALISED_MSG(Structure):
	_fields_ = [("custom_msg_id", c_uint32),
			 ("data_len", c_uint16),
			 ("free_func", c_void_p),
			 ("data", c_void_p)]

class CONTROL_DATA(Union):
	_fields_ = [("resp_event_status", c_int),
			("wifi_mac", WIFI_MAC),
			("wifi_mode", WIFI_MODE),
			("wifi_ap_scan_list", WIFI_AP_SCAN_LIST),
			("wifi_ap_config", STA_CONFIG),
			("wifi_softap_config", SOFTAP_CONFIG),
			("wifi_softap_vendor_ie", WIFI_SOFTAP_VENDOR_IE),
			("wifi_connected_stations_list", WIFI_CONNECTED_STATIONS_LIST),
			("wifi_power_save_mode", WIFI_POWER_SAVE_MODE),
			("ota_write", OTA_WRITE),
			("wifi_tx_power", WIFI_TX_POWER),
			("feature_config", FEATURE_CONFIG),
			("fw_version", FW_VERSION),
			("country_code", COUNTRY_CODE),
			("e_heartbeat", EVENT_HEARTBEAT),
			("e_sta_conn", EVENT_STATION_CONN_TO_AP),
			("e_sta_disconn", EVENT_STATION_DISCONN_FROM_AP),
			("e_softap_sta_conn", EVENT_STATION_CONN_TO_SOFTAP),
			("e_softap_sta_disconn", EVENT_STATION_DISCONN_FROM_SOFTAP),
			("e_dhcp_dns_status", EVENT_DHCP_DNS_STATUS),
			("custom_rpc_unserialised_data", CUSTOM_RPC_UNSERIALISED_MSG)]


class CONTROL_COMMAND(Structure):
	pass


CTRL_CB = CFUNCTYPE(c_int, POINTER(CONTROL_COMMAND))
FREE_BUFFFER_FUNC = CFUNCTYPE(None, c_void_p)


CONTROL_COMMAND._fields_ = [("msg_type", c_char),
			("msg_id", c_ushort),
			("uid", c_int),
			("resp_event_status", c_char),
			("control_data", CONTROL_DATA),
			("ctrl_resp_cb", CTRL_CB),
			("cmd_timeout_sec", c_int),
			("free_buffer_handle", c_void_p),
			("free_buffer_func", FREE_BUFFFER_FUNC)]


class EVENT_CALLBACK_TABLE_T(Structure):
	_fields_ = [("event", c_int),
			("fun", CTRL_CB)]


def get_str(string):
	if sys.version_info >= (3, 0):
		return string.decode()
	else:
		return string


def set_str(string):
	if sys.version_info >= (3, 0):
		return string.encode('utf-8')
	else:
		return string
