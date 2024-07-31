Feature: Test OCPP Communication

#  Scenario Outline: Successful OCPP BootNotification
#  
#    Given a charging station with unique_id <unique_id> and subprotocol <subprotocol> connected to CSMS
#    When the Charging Station sends a BootNotification to the CSMS with ven:q!dor "<vendor>" and model "<model>"
#    Then the CSMS respond with BootNotificationResponse with status "<status>"
#    Then the charging station close the connection
#
#  Examples:
#    | unique_id | subprotocol | vendor  | model   | status   |
#    | CP_1      | ocpp2.0.1   | VendorX | ModelY  | Accepted |
#    | CP_2      | ocpp1.6     | VendorX | ModelY  | Accepted |
#    | PP_2      | ocpp1.6     | VendorX | ModelY  | Rejected |
#
#  Scenario Outline: Successful BootNotification and Heartbeat
#    Given a charging station with unique_id <unique_id> and subprotocol <subprotocol> connected to CSMS
#    When the Charging Station sends a BootNotification to the CSMS with vendor "<vendor>" and model "<model>"
#    Then the CSMS respond with BootNotificationResponse with status "<response>"
#    When the Charging Station sends heartbeat requests to the CSMS for "<interval>" seconds
#    Then the CSMS respond with HeartbeatResponse with the current time
#    Then the charging station close the connection
#
#  Examples:
#    | unique_id | subprotocol | vendor  | model   | response | interval |
#    | CP_1      | ocpp2.0.1   | VendorX | ModelY  | Accepted | 30       |
#
  Scenario Outline: Successful OCPP BootNotification

    Given a charging station with unique_id <unique_id> and subprotocol <subprotocol> connected to CSMS
    When the Charging Station sends a BootNotification to the CSMS with vendor "<vendor>" and model "<model>"
    Then the CSMS respond with BootNotificationResponse with status "<status>"
    Then the charging station close the connection
  Examples:
    | unique_id | subprotocol | vendor  | model   | status   |
    | CP_1      | ocpp2.0.1   | VendorX | ModelY  | Accepted |

#    Given the Charging Station with unique_id <unique_id> has connectors with initial statuses
#    | unique_id | connector_1 | connector_2 |
#    | CP_3      | Unavailable | Unavailable |
#
#   Then the charging station close the connection
