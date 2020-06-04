import network, ttwifi, machine, time

wifi = ttwifi.init_wifi("signalhuset", "signal+huset2017")
# wifi = ttwifi.init_wifi('57A-0-Room6-10', 'dc3AunVHLx')
print(wifi.ifconfig())
beeper = machine.PWM(machine.Pin(25, machine.Pin.OUT), freq=294, duty=0)

def on_hit(data):
    name, topic, message = data
    value = int(message)
    print("[{}] Data arrived from topic: {}, Message:\n{}\n".format(name, topic, message))
    if value == 1:
        beeper.duty(1)
    else:
        beeper.duty(0)

mqtt = network.mqtt('diana-mpy1', 'mqtt://broker.hivemq.com', clientid='diana-43674632', data_cb=on_hit)
mqtt.start()

def b1_press(pin):
    if pin.value() :
        print(mqtt.publish('pico/moveright', '0'))
    else:
        print(mqtt.publish('pico/moveright', '1'))

def b0_press(pin):
    if pin.value() :
        print(mqtt.publish('pico/moveleft', '0'))
    else:
        print(mqtt.publish('pico/moveleft', '1'))

b0 = machine.Pin(0, handler=b0_press, trigger=machine.Pin.IRQ_ANYEDGE, debounce=50000, pull=machine.Pin.PULL_UP)
b1 = machine.Pin(35, handler=b1_press, trigger=machine.Pin.IRQ_ANYEDGE, debounce=50000)

time.sleep(3)
connected = mqtt.subscribe("pico/hit")
print("MQTT Connected", connected)
