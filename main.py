import network, ttwifi, machine, time

wifi = ttwifi.init_wifi('57A-0-Room6-10', 'dc3AunVHLx')
print(wifi.ifconfig())

mqtt = network.mqtt('aaron-mpy1', 'mqtt://broker.hivemq.com', clientid='aaron_sender')
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
