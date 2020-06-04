import machine, time, ttwifi, network

servo = machine.PWM(machine.Pin(15), freq=50)
servo2 = machine.PWM(machine.Pin(33), freq=50)

light = machine.ADC(39)
light.atten(light.ATTN_11DB)

led = machine.Pin(27, machine.Pin.OUT)

wifi = ttwifi.init_wifi('57A-0-Room6-10', 'dc3AunVHLx')
wifi.ifconfig()

hit_obstacle = False

white_val = 0
black_val = 0

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

def b1_press(pin):
    print('calibrating black')
    global black_val
    black_val = light.read()

def b0_press(pin):
    print('calibrating white')
    global white_val
    white_val = light.read()

b0 = machine.Pin(0, handler=b0_press, trigger=machine.Pin.IRQ_ANYEDGE, debounce=50000, pull=machine.Pin.PULL_UP)
b1 = machine.Pin(35, handler=b1_press, trigger=machine.Pin.IRQ_ANYEDGE, debounce=50000)

mqtt2 = network.mqtt('aaron1', 'mqtt://broker.hivemq.com', clientid='robot09410948123', data_cb=on_data)
mqtt2.start()
time.sleep(2)
mqtt2.subscribe('pico/moveleft')
mqtt2.subscribe('pico/moveright')

while True:
    threshold = (black_val + white_val) / 2
    if light.read() < threshold and hit_obstacle:
        mqtt2.publish('pico/hit', '0')
        hit_obstacle = False
        print('white')
        led.value(0)
    elif light.read() > threshold and not hit_obstacle:
        mqtt2.publish('pico/hit', '1')
        hit_obstacle = True
        led.value(1)
        print('black')
    time.sleep(0.1)
