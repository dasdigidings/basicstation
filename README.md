﻿### Be aware this documentation is work in progress and may have errors in it or is missing steps - June 2021

# LoRa Basics™ Station using balena.io with sx1301 and sx1302 LoRa concentrators and by using docker-compose allow to run more container parallel

This project deploys a LoRaWAN gateway with Basics Station Packet Forward protocol with balena. It runs on a Raspberry Pi (3/4) or balenaFin with a RAK2245, RAK2287 and IMST iC880a LoRa concentrators (sx1301 and sx1302). It provides a second container containing a collectd client as well to transmit metadata from the gateway to a collectd server.


## Introduction

Deploy a The Things Network (TTN), The Things Industries (TTI) or The Things Stack (TTS) LoRaWAN gateway running the Basics Station Semtech Packet Forward protocol. We are using balena.io and RAK or IMST to reduce fricition for the LoRa gateway fleet owners.

The Basics Station protocol enables the LoRa gateways with a reliable and secure communication between the gateways and the cloud and it is becoming the standard Packet Forward protocol used by most of the LoRaWAN operators.

By using a docler-compose build we are able to run other container aswell, in this instance a collectd client to transmit metadata from the gateway to a collectd server. Feel free to change the YAML for docker-compose to add more container or change the container.


## Getting started

### Hardware

* Raspberry Pi 4 or [balenaFin](https://www.balena.io/fin/)
* SD card in case of the RPi 4

#### LoRa Concentrators

* SX1301 
 * [IMST iC880a](https://shop.imst.de/wireless-modules/lora-products/8/ic880a-spi-lorawan-concentrator-868-mhz)
 * [RAK 2245 pi hat](https://store.rakwireless.com/products/rak2245-pi-hat)

* SX1302
 * [RAK 2287 Concentrator](https://store.rakwireless.com/products/rak2287-lpwan-gateway-concentrator-module) with [RAK 2287 Pi Hat](https://store.rakwireless.com/products/rak2287-pi-hat)


### Software

* A TTN  or The Things Stack V3 account ([sign up here](https://console.thethingsnetwork.org)) or [here](https://ttc.eu1.cloud.thethings.industries/console/)
* A balenaCloud account ([sign up here](https://dashboard.balena-cloud.com/))
* [balenaEtcher](https://balena.io/etcher)
* A collectd server to send the metadata to (IP address, name and password)

Once all of this is ready, you are able to deploy this repository following instructions below.

## Deploy the code

### Via [Balena-Cli](https://www.balena.io/docs/reference/balena-cli/)

If you are a balena CLI expert, feel free to use balena CLI.

- Sign up on [balena.io](https://dashboard.balena.io/signup)
- Create a new application on balenaCloud.
- Clone this repository to your local workspace with `git clone https://github.com/dasdigidings/basicstation.git`
- Edit the code (collectd/collectd.conf.d/network.conf - IP/URL + username + password from your collectd server)
- Using [Balena CLI](https://www.balena.io/docs/reference/cli/), push the code with `balena push <application-name>`
- See the magic happening, your device is getting updated 🌟Over-The-Air🌟!

### Via Git

If you are a Git expert, feel free to use Git.

- Sign up on [balena.io](https://dashboard.balena.io/signup)
- Create a new application on balenaCloud.
- Clone this repository to your local workspace with `git clone https://github.com/dasdigidings/basicstation.git`
- `cd basicstation` and connect the new git to your balena application with `git remote add balena youraccount@git.balena-cloud.com:youraccount/yourapplication.git` (adjust youraccount and yourapplication)
- Edit the code (collectd/collectd.conf.d/network.conf - IP/URL + username + password from your collectd server)
- Add the edited files with `git add .`
- Commit the edited files with `git commit -m "[FIX] edited the collectd server address"`
- Push the files to your application on balena.io with `git push -f balena master`
- See the magic happening, your device is getting updated 🌟Over-The-Air🌟!


## Configure the Gateway

### Define your MODEL

The model is defined depending on the version of the concentrator: ```SX1301``` or ```SX1302```. In case that your LoRa concentrator is a ```RAK2287``` it is using ```SX1302```. If the concentrator is the ```RAK2245``` or ```iC880a``` it uses the ```SX1301```. It's important to change the balenaCloud Device Variable with the correct ```MODEL```. The default ```MODEL``` on the balena Application is the ```SX1301```.

1. Go to balenaCloud dashboard and get into your LoRa gateway device site.
2. Click "Device Variables" button on the left menu and change the ```MODEL``` variable to ```SX1302``` if needed.

That enables a fleet of LoRa gateways with both (e.g.) ```RAK2245``` and ```RAK2287``` together under the same app.

### Define your REGION and TTN STACK VERSION

From now it's important to facilitate the ```TTN_STACK_VERSION``` that you are going to use ```2``` (TTN v2) or ```3``` (The Things Stack or TTN V3). The default variable is defined (now finally) into ```3```(V3).
Before starting, also check the ```TTN_REGION```. It needs to be changed if your region is not Europe. In case you use version 3, the European version is ```eu1```. Check [here](https://www.thethingsnetwork.org/docs/lorawan/frequencies-by-country.html) the LoRa frequencies by country.

With these variables ```TTN_REGION``` and ```TTN_STACK_VERSION``` the ```TC_URI``` will be generated automatically. In case that you want to point to another specific TC_URI, feel free to change this Device Variable on the balenaCloud.

### Get the EUI of the LoRa Gateway

The LoRa gateways are manufactured with a unique 64 bits (8 bytes) identifier, called EUI, which can be used to register the gateway on The Things Network. To get the EUI from your board it’s important to know the Ethernet MAC address of it. The TTN EUI will be the Ethernet mac address (6 bytes), which is unique, expanded with 2 more bytes (FFFE). This is a standard way to increment the MAC address from 6 to 8 bytes.

To get the EUI, copy the TAG of the device which will be generated automatically when the device gets provisioned on balenaCloud.

If that does not work, go to the terminal box and click "Select a target", then “HostOS”. Once you are inside the shell, type:

```cat /sys/class/net/eth0/address | sed -r 's/[:]+//g' | sed -e 's#\(.\{6\}\)\(.*\)#\1fffe\2#g' ```

Copy the result and you are ready to register your gateway with this EUI.


### Configure your The Things Stack gateway (V3)

1. Sign up at [The Things Stack console](https://ttc.eu1.cloud.thethings.industries/console/).
2. Click "Go to Gateways" icon.
3. Click the "Add gateway" button.
4. Introduce the data for the gateway.
5. Paste the EUI from the balenaCloud tags.
6. Complete the form and click Register gateway.
7. Once the gateway is created, click "API keys" link.
8. Click "Add API key" button.
9. Select "Grant individual rights" and then "Link as Gateway to a Gateway Server for traffic exchange ..." and then click "Create API key".
10. Copy the API key generated. and bring it to balenaCloud as ```TC_KEY```.

### Configure your The Things Network gateway (V2)

1. Sign up at [The Things Network console](https://console.thethingsnetwork.org/).
2. Click Gateways button.
3. Click the "Register gateway" link.
4. Check “I’m using the legacy packet forwarder” checkbox.
5. Paste the EUI from the balenaCloud tag or the Ethernet mac address of the board (calculated above)
6. Complete the form and click Register gateway.
7. Copy the Key generated on the gateway page.


### Balena LoRa Basics Station Service Variables

Once successfully registered:

1. Go to balenaCloud dashboard and get into your LoRa gateway device site.
2. Click "Device Variables" button on the left menu and add these variables.

Alternativelly, you can also set any of them at application level if you want it to apply to all devices in you application.


#### Common Variables

Variable Name | Value | Description | Default
------------ | ------------- | ------------- | -------------
**`GW_GPS`** | `STRING` | Enables GPS | true or false
**`GW_RESET_PIN`** | `INT` | Pin number that resets (Raspberry Pi header number) | 11
**`GW_RESET_GPIO`** | `INT` | GPIO number that resets (Broadcom pin number, if not defined, it's calculated based on the GW_RESET_PIN) | 17
**`TTN_STACK_VERSION`** | `INT` | If using TTN, version of the stack. It can be either 2 (TTNv2) or 3 (TTS) | 3
**`TTN_REGION`** | `STRING` | Region of the TTN server to use | ```eu1``` (when using TTN v2 use ```eu```)
**`TC_URI`** | `STRING` | basics station TC URI to get connected.  | 
**`TC_TRUST`** | `STRING` | Certificate for the server | Automatically retrieved from LetsEncryt based on the `TTN_STACK_VERSION` value
**`MODEL`** | `STRING` | ```SX1301``` or ```SX1302``` | ```SX1301```


#### The Things Stack (TTS) Specific Variables (V3)

Remember to generate an API Key and copy it. It will be the ```TC_KEY```.

The `TC_URI` and `TC_TRUST` values are automatically populated to use ```wss://eu1.cloud.thethings.network:8887``` if you set `TTN_STACK_VERSION` to 3.If your region is not EU you can set it using ```TTN_REGION```. At the moment there is only one server avalable is ```eu1```.

Variable Name | Value | Description | Default
------------ | ------------- | ------------- | -------------
**`TC_KEY`** | `STRING` | Unique TTN Gateway Key | (Key pasted from TTN console)


#### The Things Network (TTNv2) Specific Variables (V2)

Remember to copy the The Things Network gateway KEY and ID to configure your board variables on balenaCloud.

The `GW_ID`and `GW_KEY` variables have been generated automatically when the Application has been created with the Deploy with Balena button. Replace the values with the KEY and ID from the TTN console.

The `TC_URI` and `TC_TRUST` values are automatically populated to use ```wss://lns.eu.thethings.network:443``` if you set `TTN_STACK_VERSION` to 2. If your region is not EU you can set it using ```TTN_REGION```, Possible values are ```eu```, ```us```, ```in``` and ```au```.

Variable Name | Value | Description | Default
------------ | ------------- | ------------- | -------------
**`GW_ID`** | `STRING` | TTN Gateway EUI | (EUI)
**`GW_KEY`** | `STRING` | Unique TTN Gateway Key | (Key pasted from TTN console)


#### collectd Specific Variables

Variable Name | Value | Description | Default
------------ | ------------- | ------------- | -------------
**`GW_COLLECTD_SERVER`** | `STRING` | URL or IP of the collectd server | please set
**`GW_COLLECTD_INTERVAL`** | `STRING` | interval to send metadata | 30 seconds
**`GW_BME280`** | `STRING` | BME280 connected or not (true or false) | false
**`GW_BME280_ADDR`** | `STRING` | BME280 address (default 0x76) | please set
**`GW_BME280_SMBUS`** | `STRING` | BME280 SMBus (default 1) | please set


At this moment your LoRaWAN gateway should be up and running. Check on the TTN or TTS console if it shows the connected status.


## Troubleshoothing

It's possible that on the TTN Console the gateway appears as Not connected if it's not receiving any LoRa message. Sometimes the websockets connection among the LoRa Gateway and the server can get broken. However a new LoRa package will re-open the websocket between the Gateway and TTN or TTI. This issue should be solved with the TTN v3.

## TTNv2 to TTS migration

Initial state: one of more devices connected to TTNv2 stack (The Things Network).

Proposed procedure:

1. Create the gateways at TTS using the very same Gateway ID (Gateway EUI)
2. Create a `TC_KEY` variable on each device sith the TTN Gateway Key pasted from the TTI console.
3. Set the `TTN_STACK_VERSION` variable to 3, either at application level or per device

Now you can move them from TTS to TTNv2 back and forth (using the `TTN_STACK_VERSION` variable) as you wish as long as the gateways are defined on both platforms and the `TC_KEY` and `GW_KEY` do not change.

## Attribution

- This is an adaptation of the [Semtech Basics Station repository](https://github.com/lorabasics/basicstation). Documentation [here](https://doc.sm.tc/station).
- This is in part working thanks of the work of Jose Marcelino from RAK Wireless, Xose Pérez from Allwize and Marc Pous from balena.io.
- This is in part based on excellent work done by Rahul Thakoor from the Balena.io Hardware Hackers team.
