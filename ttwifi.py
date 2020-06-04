import network, time

def init_wifi(apname, password, timeout=3000):
  """Connect to wifi. A timeout (milliseconds) will cause the function to block
  until the timeout has expired or a successful connection is made."""
  wifi = network.WLAN(network.STA_IF)
  wifi.active(True)
  wifi.connect(apname, password)

  if timeout > 0:
    time.sleep_ms(1000)

    now = time.ticks_ms()
    while True:
      if wifi.ifconfig()[0] != '0.0.0.0':
        break
      if time.ticks_ms() - now > timeout:
        break

  return wifi
