#!/usr/bin/env python3

import csv
from panda import Panda

OTHER_GMLAN_BUS = 1


def can_logger():
  p = Panda()
  p.set_gmlan(True)
  p.set_safety_mode(Panda.SAFETY_SILENT)

  try:
    outputfile = open('output.csv', 'w')
    csvwriter = csv.writer(outputfile)
    # Write Header
    csvwriter.writerow(['Bus', 'MessageID', 'Message', 'MessageLength'])
    print("Writing csv file output.csv. Press Ctrl-C to exit...\n")

    bus0_msg_cnt = 0
    bus1_msg_cnt = 0
    bus2_msg_cnt = 0
    bus3_msg_cnt = 0

    while True:
      can_recv = p.can_recv()

      for address, _, dat, src in can_recv:
        csvwriter.writerow([str(src), str(hex(address)), f"0x{dat.hex()}", len(dat)])

        if src == 0:
          bus0_msg_cnt += 1
        elif src == 1:
          bus1_msg_cnt += 1
        elif src == 2:
          bus2_msg_cnt += 1
        elif src == 3:
          bus3_msg_cnt += 1
        else:
          print(src)

        print(f"Message Counts... Bus 0: {bus0_msg_cnt} Bus 1: {bus1_msg_cnt} Bus 2: {bus2_msg_cnt} Bus 3: {bus3_msg_cnt}", end='\r')

  except KeyboardInterrupt:
    print(f"\nNow exiting. Final message Counts... Bus 0: {bus0_msg_cnt} Bus 1: {bus1_msg_cnt} Bus 2: {bus2_msg_cnt} Bus 3: {bus3_msg_cnt}")
    outputfile.close()


if __name__ == "__main__":
  can_logger()
