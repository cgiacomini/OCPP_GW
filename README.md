

# OCPP Gateway 
The OCPP Gateway application is a WebSocket server that listens for incoming
OCPP messages from the Charge Points and forwards them to a Kafka topic. 
The OCPP Gateway application also listens for messages from the Kafka topic
and forwards them to the Charge Points

1. [Kafka Setup](#kafka-setup)
  1. [Clone Repository](#clone-repositoty)
  2. [configuration](#configuration)
  3. [Startup](#startup)
2. [Run OCPP Gateway](#run-OCPP-gateway)
  1. [Python Virtual Environment Setup](#python-virtual-environment-setup)
  2. [Configuration file](#configuration0-file)
  3. [OCPP Charging Station Management System (CSMS)](#ocpp-charging-Station-Management-system)
  4. [OCPP Gateway](#ocpp-gateway)
  5. [Charging Station](#charging-station)
3. [Testing](#testing)

# Kafka Setup
## Clone Repository
```
$ git clone https://github.com/minhhungit/kafka-kraft-cluster-docker-compose.git
$ cd kafka-kraft-cluster-docker-compose/
```
## Configuration
If needed we can customize the kafka nodes take a look at the following files:

```
  ├── docker-compose.yaml
  └── config
        ├── kafka01
        │   └── server.properties
        ├── kafka02
        │   └── server.properties
        ├── kafka03
        │   └── server.properties
        └── server.properties.orig
```
## Startup
Follow the **kafka-kraft-cluster-docker-compose/readme.md** in the cloned repository, here are the basic steps:
Add the node in the **/etc/hosts** file
```
127.0.0.1 kafka01
127.0.0.1 kafka02
127.0.0.1 kafka03
```
start the kafka cluster
```
$ cd kafka-kraft-cluster-docker-compose/
$ docker-compose up -d
```
# Run OCPP Gateway
## Python Virtual Environment Setup
```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export PYTHONPATH=`pwd`
```

## Configuration file
All software in this project uses a configuration file named config.cfg. 
This file is formatted like a typical Windows INI file:

***config.cfg***
```
[kafka]
servers=kafka01:29192,kafka02:29292,kafka03:29392
consumer_timeout_ms=1000
auto_offset_reset=latest
enable_auto_commit=True
in_messages_topic=messages_in
out_messages_topic=messages_out
ocpp_gw_consumer_group=ocpp_gateways
csms_consumer_group=csms_server
num_partitions=8
replica_factor=3

[ocpp_gateway]
subprotocols=ocpp1.6,ocpp2.0.1
use_ssl=False
host=localhost
listening_host=0.0.0.0
listening_port=9000
```

## OCPP Charging Station Management System (CSMS) 
The module that implements the Charge Point Management System (CSMS) server,
listens for messages from the Kafka topic ***in_messages***, process them and and send the
response back to the Kafka topic ***out_messages***.
We need to start the CSMS first since is in charge to create kafka topics unless the topics are already present or created manually.
```
$ source .venv/bin/activate
$ cd cms_server
$ python csms_server.py --config ../config.cfg
{"timestamp": "2024-06-13T14:57:02.879302", "level": "INFO", "message": "Subscriber: for messages_in topic"}
{"timestamp": "2024-06-13T14:57:02.879422", "level": "INFO", "message": "Producer:   for messages_out topic"}
{"timestamp": "2024-06-13T14:57:02.879460", "level": "INFO", "message": "CSMS Started ..."}
```

## OCPP Gateway
The OCPP Gateway application is a WebSocket server that listens for incoming
OCPP messages from the Charge Points and forwards them to a Kafka topic. The
application also listens for messages from the Kafka topic and forwards them
to the Charge Points.
The OCPP Gateway assume the existences of the kafka topics used for messages 
exchange with the CSMS. 
```
$ source .venv/bin/activate
$ cd ocpp_gw
$ python ocpp_gw.py --config ../config.cfg
{"timestamp": "2024-06-13T14:57:34.076657", "level": "INFO", "message": "OCPP GW application started..."}
{"timestamp": "2024-06-13T14:57:34.083624", "level": "INFO", "message": "KFH: Kafka consumer and producer initialized. servers: kafka01:29192,kafka02:29292,kafka03:29392"}
{"timestamp": "2024-06-13T14:57:34.083878", "level": "INFO", "message": "WSH: WebSocket server initialized. host: 0.0.0.0 port: 9000"}
```

## Charging Station
This is the charge station script that connects to the OCPP Gateway and sends
boot notifications and heartbeats.
```
$ source .venv/bin/activate
$ python charge_station.py  --config ../config.cfg
{"timestamp": "2024-06-13T15:06:50.054303", "level": "INFO", "message": "CP_1: send [2,\"bddb4be5-592e-449e-a746-069f5b3e9551\",\"BootNotification\",{\"chargingStation\":{\"model\":\"Wallbox 123\",\"vendorName\":\"anewone\"},\"reason\":\"PowerUp\"}]"}
{"timestamp": "2024-06-13T15:06:51.116892", "level": "INFO", "message": "CP_1: receive message [3,\"bddb4be5-592e-449e-a746-069f5b3e9551\",{\"currentTime\":\"2024-06-13T17:06:51.049224\",\"interval\":10,\"status\":\"Accepted\"}]"}
{"timestamp": "2024-06-13T15:06:51.117960", "level": "INFO", "message": "Connected to central system."}
{"timestamp": "2024-06-13T15:06:51.118359", "level": "INFO", "message": "CP_1: send [2,\"1f362c4e-d758-42ef-bafb-8816d07c5c12\",\"Heartbeat\",{}]"}
{"timestamp": "2024-06-13T15:06:53.119465", "level": "INFO", "message": "CP_1: receive message [3,\"1f362c4e-d758-42ef-bafb-8816d07c5c12\",{\"currentTime\":\"2024-06-13T17:06:52.218233\"}]"}
```

# Testing
We use Behave, a behavior-driven development (**BDD**) framework for Python, which allow us to define test scenarios using Gherkin syntax. 
This ensures that the documentation is always up-to-date with the actual implementation. 
With Gherkin syntax test case scenarios are written in a human readable way:
```
  Scenario Outline: Successful BootNotification and Heartbeat
    Given I have a charging station with unique_id "<unique_id>" and subprotocol "<subprotocol>" connected to the server
    When I send a BootNotification message with vendor "<vendor>" and model "<model>"
    Then I should receive "<response>" as response
    Then I start sending heartbeats for "<interval>" seconds
    Then close the connection

  Examples:
    | unique_id | subprotocol | vendor  | model   | response | interval |
    | CP_1      | ocpp2.0.1   | VendorX | ModelY  | Accepted | 30       |
    | CP_2      | ocpp1.6     | VendorX | ModelY  | Accepted | 30       |
```

## Setup
Prerequisites: 
  1. Start CSMS
  2. Start OCPP Gateway

```
$ cd OCPPGW
$ export PYTHONPATH=`pwd`
$ source .venv/bin/activate
$ cd tests
# behave
```

