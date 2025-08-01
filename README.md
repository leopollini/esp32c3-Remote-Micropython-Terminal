# Remote Micropython Terminal

This project aims towards the creation of a general purpose remotely controlled micropython executor board, specifically created for an esp32c3 with builtin 0.42inch oled display (from [Aliexpress](https://it.aliexpress.com/item/1005007342383107.html?src=google&pdp_npi=4%40dis!EUR!6.47!4.14!!!!!%40!12000040340730534!ppc!!!&snpsid=1&snps=y&snpsid=1&src=google&albch=shopping&acnt=742-864-1166&isdl=y&slnk=&plac=&mtctp=&albbt=Google_7_shopping&aff_platform=google&aff_short_key=_oDeeeiG&gclsrc=aw.ds&&albagn=888888&&ds_e_adid=&ds_e_matchtype=&ds_e_device=c&ds_e_network=x&ds_e_product_group_id=&ds_e_product_id=it1005007342383107&ds_e_product_merchant_id=5551326180&ds_e_product_country=IT&ds_e_product_language=it&ds_e_product_channel=online&ds_e_product_store_id=&ds_url_v=2&albcp=22441091640&albag=&isSmbAutoCall=false&needSmbHouyi=false&gad_source=1&gad_campaignid=22450993135&gclid=CjwKCAjwv5zEBhBwEiwAOg2YKDLxnmY581rvDMNVz_C3dFVNBQv1Nhfd7prghdYw7ixD5LKuqIX_YRoCqQ4QAvD_BwE))

## Features
- utils.py: contains some utility functions and common variables. Is used by other scripts
- connect.py: importing this file connects to the specified wifi network using the esp32
- sh1106_oled.py: importing this file initialized the oled display (modified [this](https://github.com/robert-hh/SH1106/blob/master/sh1106.py) code for the 0.42 inch display)
- Timeout.py: reimplements asyncio's timeout() macro, since it is missing in micropython's asyncio
- boot.py: if present does nothing, but ensures that no other boot.py is executed
- main.py: runs connect and starts server
- WIFI_CODES.json: contains ssid and password of the wifi network.

##### Sample WIFI_CODES.json
```json
{
	"your_wifi1": ["passcode"],
	"two_wifis_with_same_ssid": ["password_for_1st_wifi", "password_for_2nd_wifi"]
}
```
Each time the esp tries to connect it has a 15s timeout before trying the next password or the next connection.

## Useful infos
My board implements [this](https://micropython.org/download/ESP32_GENERIC_C3/) version of Micropython.

The connection port for the remote (unsecure) shell is 22. NetCat is fine for connecting and interacting with the terminal, althou you cannot use arrows/signals (a nice client terminal will be implementent to automatically connect to the esp).

The ip address of the esp32 is printed both on the serial terminal and on the mini oled display.

Inside utils.py::vars you can set some useful variables, such as AUTOSTART_SERVER or AUTORESTART_SERVER
