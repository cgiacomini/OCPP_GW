Feature: Test OCPP Communication

  Scenario Outline: Successful OCPP BootNotification
    Given a charging station with unique_id <unique_id> and subprotocol <subprotocol> connected to CSMS
    When the Charging Station sends a BootNotification message to the CSMS with vendor "<vendor>" and model "<model>"
    Then the CSMS should respond with a BootNotificationResponse "<response>" as response
    Then the charging station close the connection

  Examples:
    | unique_id | subprotocol | vendor  | model   | response |
    | CP_1      | ocpp2.0.1   | VendorX | ModelY  | Accepted |
    | CP_2      | ocpp1.6     | VendorX | ModelY  | Accepted |
    | PP_2      | ocpp1.6     | VendorX | ModelY  | Rejected |

  Scenario Outline: Successful BootNotification and Heartbeat
    Given a charging station with unique_id <unique_id> and subprotocol <subprotocol> connected to CSMS
    When the Charging Station sends a BootNotification message to the CSMS with vendor "<vendor>" and model "<model>"
    Then the CSMS should respond with a BootNotificationResponse "<response>" as response
    When the Charging Station sends a Heartbeat request to the CSMS each "<interval>" seconds
    Then the CSMS should respond with a HeartbeatResponse with the current time
    Then the charging station close the connection

  Examples:
    | unique_id | subprotocol | vendor  | model   | response | interval |
    | CP_1      | ocpp2.0.1   | VendorX | ModelY  | Accepted | 30       |

