### NodeMCU read measurements from BME680 and send to flask SocketIO using MicroPython

1. BME680 sensor readings using https://github.com/robmarkcole/bme680-mqtt-micropython
2. SocketIO communication with Flask web server using https://github.com/danni/uwebsockets, with small changes
needed for NodeMCU.

Don't forget to set your SSID credentials in boot.py. You also need to use `mpy-cross` in order to compile the `*.py`
files (otherwise you get `MemoryError: memory allocation failed`).
