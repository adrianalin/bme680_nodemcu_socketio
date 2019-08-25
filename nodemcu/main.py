import usocketio.client as client
import bme680
from machine import Pin
from i2c import I2CAdapter
import gc

# construct an I2C bus
i2c_dev = I2CAdapter(scl=Pin(5), sda=Pin(4), freq=100000)
sensor = bme680.BME680(bme680.I2C_ADDR_SECONDARY, i2c_device=i2c_dev)

# These oversampling settings can be tweaked to
# change the balance between accuracy and noise in
# the data.
sensor.set_humidity_oversample(bme680.OS_2X)
sensor.set_pressure_oversample(bme680.OS_4X)
sensor.set_temperature_oversample(bme680.OS_8X)
sensor.set_filter(bme680.FILTER_SIZE_3)


def get_sensor_data():
    output = ""
    if sensor.get_sensor_data():
        output = "{}, {}, {}, {}".format(
            sensor.data.temperature,
            sensor.data.pressure,
            sensor.data.humidity,
            sensor.data.gas_resistance)
    return output


with client.connect('http://192.168.0.123:5000/') as socketio:

    @socketio.at_interval(1)
    def send_measurement():
        gc.collect()
        data = get_sensor_data()
        print("send measurement ", data)
        socketio.emit("bme680_data", data)

    socketio.run_forever()
