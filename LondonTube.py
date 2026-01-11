import requests 
import os # Import the requests library to handle HTTP requests
from gpiozero import LED, LEDBarGraph, Button # Import LEDBarGraph from gpiozero to control a bar graph of LEDs
from time import sleep
import time

URL = "https://api.tfl.gov.uk/line/mode/tube/status" # API endpoint for people in space
POLL_SECONDS = 5

btn_a = Button(18)
btn_b = Button(27)
btn_c = Button(22)
btn_d = Button(4)

r = requests.get(URL, timeout = 10) # Fetch the data from the API
r.raise_for_status()
data = r.json() # Parse the JSON data

LINE_TO_GPIO = {
    "victoria": 23,
    "central": 25,
    "northern": 16,
    "jubilee": 20,
    "piccadilly": 21,
    "bakerloo": 6,
    "circle": 12,
    "district": 5,
    "hammersmith-city": 13,
    "metropolitan": 19,
    "waterloo-city": 26,

}
# leds = LEDBarGraph(26, 19, 13, 6, 5, 12, 16, 20, 21, 25, 23) # Initialize the LED bar graph with GPIO pins
LEDS = {line_id: LED(gpio_pin) for line_id, gpio_pin in LINE_TO_GPIO.items()}


lines = []

    
class TubeLine:
    def __init__(self, name, status, severity):
        self.name = name
        self.status = status
        self.severity = severity
    def __str__(self):
        return f"{self.name}: {self.status} [{self.severity}]"


# def All_ServiceDisruptions():
#     for line in data:
#             name = line["name"]
#             status = line["lineStatuses"][0]["statusSeverityDescription"]
#             severity = line["lineStatuses"][0]["statusSeverity"]
#             tube_line = TubeLine(name, status, severity)
#             lines.append(tube_line)
#             print(tube_line)
#             if severity >= 10:
#                 leds.value = 1.0  # Set the LED bar graph value to maximum for severe disruptions
#                 sleep(5)  # Keep the LEDs on for 5 seconds
#             elif severity >= 9:
#                 leds.value = 0.5  # Set the LED bar graph value to medium for moderate disruptions
#                 sleep(5)  # Keep the LEDs on for 5 seconds
#             elif severity >= 6:
#                 leds.value = 0.3  # Set the LED bar graph value to low-medium for minor disruptions
#                 sleep(5)  # Keep the LEDs on for 5 seconds
#             else:
#                 leds.value = 0.1  # Set the LED bar graph value to low for minor disruptions
#                 sleep(5)  # Keep the LEDs on for 5 seconds
#     leds.off()  # Turn off all LEDs after processing
#     sleep(60)  # Wait for 10 seconds before the next update
# main()




# def Specfic_Line_Status():
#     line_name = input("Enter the Tube line name (e.g., Jubilee, Central): ")
#     for line in data:
#         if line["name"].lower() == line_name.lower():
#             status = line["lineStatuses"][0]["statusSeverityDescription"]
#             severity = line["lineStatuses"][0]["statusSeverity"]
#             tube_line = TubeLine(line_name, status, severity)
#             print(tube_line)
#             if severity >= 10:
#                 leds.value = 1.0  # Set the LED bar graph value to maximum for severe disruptions
#             elif severity >= 9:
#                 leds.value = 0.5  # Set the LED bar graph value to medium for moderate disruptions
#             elif severity >= 6:
#                 leds.value = 0.3  # Set the LED bar graph value to low-medium for minor disruptions
#             else:
#                 eds.value = 0.1  # Set the LED bar graph value to low for minor disruptions
#             sleep(10)  # Keep the LEDs on for 10 seconds
#             leds.off()  # Turn off all LEDs after processing
#             return
#     print(f"No data found for line: {line_name}")
#     return


def is_delayed(line_obj: dict) -> bool:
    """
    Treat anything other than 'Good Service' as delayed.
    """
    statuses = line_obj.get("lineStatuses", [])
    if not statuses:
        return False  # or True if you prefer “unknown = alert”
    text = (statuses[0].get("statusSeverityDescription") or "").strip().lower()
    return text != "good service"

def Disruptions_On_Service():
    rounds = 0
    while rounds < 1:
        # Build a quick lookup by line id
        by_id = {line.get("id"): line for line in data if isinstance(line, dict)}

        for line_id, led in LEDS.items():
            line_obj = by_id.get(line_id)

            if not line_obj:
                # If TfL didn't return that line for some reason, turn off
                led.off()
                continue

            delayed = is_delayed(line_obj)
            if delayed:
                led.on()
            else:
                led.off()

            # Optional debug print
            status_text = line_obj.get("lineStatuses", [{}])[0].get("statusSeverityDescription", "Unknown")
            print(f"{line_id}: {status_text} -> LED {'ON' if delayed else 'OFF'}")
        rounds += 1
    print("Do want to exit?") 
    print("Press the Dark Button to return to main menu.")
    while True:
        if btn_d.is_pressed:
            btn_d.wait_for_release()
            print("Exiting program.")
            for led in LEDS.values():
                led.off()
            main()

def button_p():
    button.wait_for_press()
    print("Button pressed!")
    button.wait_for_release()
    print("Button released!")

def main():
    print("London Tube Line Status Monitor")
    print("---------------------------------")
    print("What Tube status would you like to monitor?")
    print("Blue Button: For Disruptions on any service")
    print("Yellow Button: NA")
    print("Green Button: NA")
    while True:
        if btn_a.is_pressed:
            btn_a.wait_for_release()
            print("You pressed the Blue Button")
            print('\n')
            Disruptions_On_Service()
            # Specfic_Line_Status()
        elif btn_b.is_pressed:
            btn_b.wait_for_release()
            print("You pressed the Yellow Button")
            print('\n')
            main()
            # All_ServiceDisruptions()
        elif btn_c.is_pressed:
            btn_c.wait_for_release()
            print("You pressed the Green Button")
            print('\n')
            main()
            
 


main()