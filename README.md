# london-tube-delay-tracker

This project is a real-time London Tube delay tracker built using a Raspberry Pi and Python.
It consumes live service status data from the TfL API and displays it on an LCD screen with LEDs, allowing users to quickly see which Tube lines are running normally, experiencing minor delays, or are fully disrupted.

The goal of the project is to explore hardware–software integration, API consumption, and physical user feedback, while also providing an unusually reliable confirmation of London commuters' expectations.

Features

Version 1 — Acceptance

The first iteration focused on proving the concept:
	•	Python script pulling live Tube status data from the TfL API
	•	Raspberry Pi with a breadboard and single-colour LEDs
	•	Red LEDs illuminated for delayed lines
	•	Minimal output, maximum disappointment

This version answered one key question:
“Are the Tube lines delayed?”
The answer was almost always yes.

⸻

Version 2 — Detail

Version 2 expands the project both technically and emotionally:
	•	RGB LEDs to represent service states:
	•	🟢 Green — Good service
	•	🟡 Yellow — Minor delays
	•	🔴 Red — Severe delays/character building
	•	LCD screen displaying:
	•	Tube line name
	•	Delay type (good service, minor delays, severe delays, etc.)
	•	Improved user interaction and clearer real-time feedback
	•	Same data source, greater specificity, identical outcome

⸻

Future Improvements (V3)

Planned ideas for a potential Version 3 include:
	•	Removal of the green LED to reduce false optimism
	•	Historical delay tracking to prove this isn’t “just a bad day”
	•	Audible alerts for delays (optional, but emotionally risky)
	•	Web dashboard or companion app for remote monitoring
	•	Power-saving mode for when everything is delayed anyway

All improvements are subject to one major external dependency:
London transport infrastructure is behaving differently.
