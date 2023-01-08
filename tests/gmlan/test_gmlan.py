import time

from panda import Panda


def connect_wo_esp():
  # connect to the panda
  p = Panda()

  # power down the ESP
  p.set_esp_power(False)
  return p


def time_many_sends(p, bus):
  MSG_COUNT = 100

  st = time.time()
  p.can_send_many([(0x1aa, 0, b"\xaa"*8, bus)]*MSG_COUNT)
  r = []

  while len(r) < 200 and (time.time() - st) < 3:
    r.extend(p.can_recv())

  sent_echo = filter(lambda x: x[3] == 0x80 | bus, r)
  loopback_resp = filter(lambda x: x[3] == bus, r)

  assert len(list(sent_echo)) == 100
  assert len(list(loopback_resp)) == 100

  et = (time.time()-st)*1000.0
  comp_kbps = (1+11+1+1+1+4+8*8+15+1+1+1+7)*MSG_COUNT / et

  return comp_kbps


def test_gmlan():
  p = Panda()

  # enable output mode
  p.set_safety_mode(Panda.SAFETY_ALLOUTPUT)

  # enable CAN loopback mode
  p.set_can_loopback(True)

  SPEED_NORMAL = 500
  SPEED_GMLAN = 33.3

  p.set_can_speed_kbps(1, SPEED_NORMAL)
  p.set_can_speed_kbps(2, SPEED_NORMAL)
  p.set_can_speed_kbps(3, SPEED_GMLAN)

  # set gmlan on CAN2
  bus = Panda.GMLAN_CAN3
  p.set_gmlan(bus)
  comp_kbps_gmlan = time_many_sends(p, 3)
  assert 0.8 * SPEED_GMLAN < comp_kbps_gmlan < 1.0 * SPEED_GMLAN

  p.set_gmlan(None)
  comp_kbps_normal = time_many_sends(p, bus)
  assert 0.8 * SPEED_NORMAL < comp_kbps_normal < 1.0 * SPEED_NORMAL

  print("%d: %.2f kbps vs %.2f kbps" % (bus, comp_kbps_gmlan, comp_kbps_normal))


if __name__ == '__main__':
  test_gmlan()
