import usb.core
import sys
import os
import logging

dev = usb.core.find(idVendor=0x0483, idProduct=0x5750)
if dev is None:
  raise ValueError('Our device is not connected')
else: 
  print("found it")
  for cfg in dev:
    sys.stdout.write(str(cfg.bConfigurationValue) + '\n')
    for intf in cfg:
        sys.stdout.write('\t (intf.bInterfaceNumber , intf.bAlternateSetting) = ' + \
                         str(intf.bInterfaceNumber) + \
                         ',' + \
                         str(intf.bAlternateSetting) + \
                         '\n')
        for ep in intf:
            sys.stdout.write('\t\t ep.bEndpointAddress = ' + \
                             str(ep.bEndpointAddress) + \
                             '\n')
  ep = dev[0].interfaces()[0].endpoints()[0]
  i = dev[0].interfaces()[0].bInterfaceNumber
  dev.reset()

  if dev.is_kernel_driver_active(i):
    dev.detach_kernel_driver(i)
  
  # dev.set_configuration()
  # eaddr=ep.bEndpointAddress
  # r=dev.read(eaddr, 1024)
  # print(len(r))
  # print(r)