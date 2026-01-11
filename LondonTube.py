from gpiozero import LED, LEDBarGraph, Button, OutputDevice, Button
from RPLCD.i2c import CharLCD
from time import sleep
import requests

URL = "https://api.tfl.gov.uk/line/mode/tube/status" # API endpoint for people in space
POLL_SECONDS = 5

r = requests.get(URL, timeout = 10) # Fetch the data from the API
r.raise_for_status()
data = r.json() # Parse the JSON data

ledGreen = LED(16)  # Example LED on GPIO pin 16
ledYellow = LED(20)  # Example LED on GPIO pin 20
ledRed = LED(21)  # Example LED on GPIO pin 21
btn_a = Button(5)  # Example button on GPIO pin 12
btn_b = Button(13)  # Example button on GPIO pin 16


lcd = CharLCD(
    i2c_expander='PCF8574',
    address=0x27,   # change to 0x3F if that’s what i2cdetect shows
    port=1,
    cols=16,
    rows=2,
    charmap='A00',
)

class TubeLine: # Define TubeLine class
    def __init__(self, name, status, severity): # Initialize TubeLine object
        self.name = name # Set name attribute
        self.status = status # Set status attribute
        self.severity = severity # Set severity attribute
    def __str__(self): # String representation of TubeLine object
        return f"{self.name}: {self.status} [{self.severity}]" # Return formatted string

def lcdservice_disruptions():
    print("Monitoring Service Disruptions...")
    print("---------------------------------")
    rounds = 0 
    while rounds < 1:
        for line in data:
            name = line["name"]
            status = line["lineStatuses"][0]["statusSeverityDescription"]
            severity = line["lineStatuses"][0]["statusSeverity"]
            tube_line = TubeLine(name, status, severity)
            lcd.clear()
            lcd.write_string(f"{tube_line.name}")
            lcd.cursor_pos = (1, 0)
            lcd.write_string(f"{tube_line.status}")
            print(tube_line)
            if severity >= 10:
                ledRed.off()
                ledYellow.off()
                ledGreen.on()
            elif severity >= 9:
                ledGreen.off()
                ledRed.off()
                ledYellow.on()
            elif severity <= 8:
                ledGreen.off()
                ledYellow.off()
                ledRed.on()
            sleep(5)  # Keep the LEDs on for 5 seconds
        sleep(POLL_SECONDS)
        rounds += 1
        print("Do you want to check again? (Y/N)")
        text = input().strip().upper()
        if text == 'Y':
            lcd.clear()
        elif text == 'N':
            lcd.clear()
            ledRed.off()
            ledYellow.off()
            ledGreen.off()
            print("Exiting Service Disruption Monitor.")
            main()

def monitor_tube_delays():
    print("Monitoring Tube Delays...")
    print("---------------------------------")
    print("Which Line would you like to check the status of?")
    print("Available Lines:")
    print("1: Victoria")
    print("2: Central")
    print("3: Northern")
    print("4: Jubilee")
    print("5: Piccadilly")
    print("6: Bakerloo")
    print("7: Circle")
    print("8: District")
    print("9: Hammersmith-City")
    print("10: Metropolitan")
    print("11: Waterloo-City")
    line_to_monitor = input("Enter Tube line: ").strip().lower()
    if line_to_monitor == "1":
        line_to_monitor = "victoria"
    elif line_to_monitor == "2":
        line_to_monitor = "central"
    elif line_to_monitor == "3":
        line_to_monitor = "northern"
    elif line_to_monitor == "4":
        line_to_monitor = "jubilee"
    elif line_to_monitor == "5":
        line_to_monitor = "piccadilly"
    elif line_to_monitor == "6":
        line_to_monitor = "bakerloo"
    elif line_to_monitor == "7":
        line_to_monitor = "circle"
    elif line_to_monitor == "8":
        line_to_monitor = "district"
    elif line_to_monitor == "9":
        line_to_monitor = "hammersmith-city"
    elif line_to_monitor == "10":
        line_to_monitor = "metropolitan"
    elif line_to_monitor == "11":
        line_to_monitor = "waterloo-city"
    rounds = 0 
    while rounds < 1:
        for line in data:
            name = line["name"]
            if name.lower() == line_to_monitor:
                status = line["lineStatuses"][0]["statusSeverityDescription"]
                severity = line["lineStatuses"][0]["statusSeverity"]
                tube_line = TubeLine(name, status, severity)
                lcd.clear()
                lcd.write_string(f"{tube_line.name}")
                lcd.cursor_pos = (1, 0)
                lcd.write_string(f"{tube_line.status}")
                print(tube_line)
                if severity == 10:
                    ledRed.off()
                    ledYellow.off()
                    ledGreen.on()
                elif severity <= 9:
                    ledRed.off()
                    ledYellow.on()
                    ledGreen.off()
                elif severity <= 4:
                    ledRed.on()
                    ledYellow.off()
                    ledGreen.off()
                break
                
        else:
            print(f"Line '{line_to_monitor}' not found. Please check the name and try again.")
            monitor_tube_delays()

        sleep(POLL_SECONDS)
        rounds += 1
        print("Do you want to check another line? (Y/N)")
        text = input().strip().upper()
        if text == 'Y':
            lcd.clear()
            monitor_tube_delays()
        elif text == 'N':
            lcd.clear()
            ledRed.off()
            ledYellow.off()
            ledGreen.off()
            print("Exiting Tube Delay Monitor.")
            main()
            


                
def main():
    print("London Tube Line Status Monitor")
    print("---------------------------------")
    print("What Tube status would you like to monitor?")
    print("1: Press Red button for Tube Delays")
    print("2: Press Blue button for Service Disruptions")
    while True:
        if btn_a.is_pressed:
            btn_a.wait_for_release()
            monitor_tube_delays()
            break
        elif btn_b.is_pressed:
            btn_b.wait_for_release()
            lcdservice_disruptions()
            break
        sleep(0.1)
    
main()