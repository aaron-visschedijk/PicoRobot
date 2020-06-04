import machine, time, ttwifi, network

servo = machine.PWM(machine.Pin(15), freq=50)
servo2 = machine.PWM(machine.Pin(33), freq=50)

light = machine.ADC(39)
light.atten(light.ATTN_11DB)

led = machine.Pin(27, machine.Pin.OUT)

wifi = ttwifi.init_wifi('57A-0-Room6-10', 'dc3AunVHLx')
wifi.ifconfig()

def on_data(data):
    name, topic, message = data
    value = int(message)
    print("[{}] Data arrived from topic: {}, Message:\n{}\n".format(name, topic, message))
    if topic == 'pico/moveleft':
        if value:
            servo.duty(13.5)
        else:
            servo.duty(0)
    elif topic == 'pico/moveright':
        if value:
            servo2.duty(13.5)
        else:
            servo2.duty(0)

mqtt2 = network.mqtt('aaron1', 'mqtt://broker.hivemq.com', clientid='robot09410948123', data_cb=on_data)
mqtt2.start()
time.sleep(2)
mqtt2.subscribe('pico/moveleft')
mqtt2.subscribe('pico/moveright')
