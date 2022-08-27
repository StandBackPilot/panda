#!/usr/bin/env python3
from typing import Dict
from panda import Panda
#from panda.tests.gmlan_harness_test import set_speed_kbps

WHITE_GMLAN_BUS = 3
OTHER_GMLAN_BUS = 1

bus = OTHER_GMLAN_BUS

try:
  p = Panda()
except AssertionError:
  print("Unable to find any attached Pandas")
  quit(1)

p.set_safety_mode(Panda.SAFETY_ALLOUTPUT)

if p.is_white() or p.is_grey():
  print("White/grey Panda: using set_gmlan")
  p.set_gmlan(Panda.GMLAN_CAN3) # 2
  bus = WHITE_GMLAN_BUS
else:
  print("Black Panda (or newer): using OBD-II harness")
  p.set_obd(True)
  bus = OTHER_GMLAN_BUS

#set_speed_kbps(p,33.0)


stats: Dict[int, int] = {}
counter: int = 0

def addCount(bus: int, count: int) -> None:
  if bus in stats:
    stats[bus] += count
  else:
    stats[bus] = count


try:
  while 1:
    msgList = p.can_recv()
    if len(msgList) <= 0:
      continue
    for msg in msgList:
      msgBus = int(msg[3])
      addCount(msgBus, 1)
      if (msgBus == bus):
        print(msg)
      if counter % 5000 == 0:
        print("STATS:")
        for bus in sorted(stats):
          print(f"Bus: {bus}, Count: {stats[bus]}")
      counter += 1
except:
  print("")
  print("FINAL STATS:")
  for bus in sorted(stats):
    print(f"Bus: {bus}, Count: {stats[bus]}")