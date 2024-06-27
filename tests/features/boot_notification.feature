Feature: Test OCPP Communication

  #@skip
  Scenario Outline: Successful OCPP BootNotification
    Given I have a charging station with unique_id "<unique_id>" and subprotocol "<subprotocol>" connected to the server
    When I send a BootNotification message with vendor "<vendor>" and model "<model>"
    Then I should receive "<response>" as response
    And close the connection

  Examples:
    | unique_id | subprotocol | vendor  | model   | response |
    | CP_1      | ocpp2.0.1   | VendorX | ModelY  | Accepted |
    | CP_2      | ocpp1.6     | VendorX | ModelY  | Accepted |
    | PP_2      | ocpp1.6     | VendorX | ModelY  | Rejected |


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

