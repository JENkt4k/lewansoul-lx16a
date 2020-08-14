import usb.core
import usb.util
import sys


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

# commands
CMD_SERVO_MOVE = 3
CMD_ACTION_GROUP_RUN = 6
CMD_ACTION_STOP = 7
CMD_ACTION_SPEED = 11
CMD_GET_BATTERY_VOLTAGE = 15
CMD_MULT_SERVO_UNLOAD = 20
CMD_MULT_SERVO_POS_READ = 21
#
#Header Length Command Parameter
#0x55 0x55 0x08 0x03 0x01 0xE8 0x03 0x01 0xD0 0x07

#READ 
#0x55 0x55 0x09 0x15 0x06 0x01 0x02 0x03 0x04 0x05 0x06
header = [0x55, 0x55, 0x09, 0x15, 0x06, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06]
battery = [0x55, 0x55, 0x02, 0x0F]
# looks like 512 bytes

def query(command, writeEp, readEpId):
  writeEp.write(bytes(command))
  r=dev.read(readEpId, 1024,17)
  print(len(r))
  print(r)

# find our device
dev = usb.core.find(idVendor=0x0483, idProduct=0x5750)

# was it found?
if dev is None:
    raise ValueError('Device not found')

# for cfg in dev:
#     sys.stdout.write(str(cfg.bConfigurationValue) + '\n')
#     for intf in cfg:
#         sys.stdout.write('\t interface number,setting ' + \
#                          str(intf.bInterfaceNumber) + \
#                          ',' + \
#                          str(intf.bAlternateSetting) + \
#                          '\n')
#         for ep in intf:
#             sys.stdout.write('\t\t address ' + \
#                              str(ep.bEndpointAddress) + \
#                              '\n' + \
#                                '\t\t direction ' + \
#                                  str(usb.util.endpoint_direction(ep.bEndpointAddress) == usb.util.ENDPOINT_OUT) +'\n'
#                                  '\t\t direction ' + \
#                                  str(usb.util.endpoint_direction(ep.bEndpointAddress) == usb.util.ENDPOINT_IN) +'\n'
#                                  )



# set the active configuration. With no arguments, the first
# configuration will be the active one
dev.set_configuration()

# get an endpoint instance
cfg = dev.get_active_configuration()
intf = cfg[(0,0)]


ep = usb.util.find_descriptor(
    intf,
    # match the first OUT endpoint
    custom_match = \
    lambda e: \
        usb.util.endpoint_direction(e.bEndpointAddress) == \
        usb.util.ENDPOINT_OUT)

assert ep is not None

# write the data
#ep.write(bytes(CMD_GET_BATTERY_VOLTAGE))
ep.write(bytes(battery))
print(ep.bEndpointAddress)
r=dev.read(130, 64)
print(len(r))
print(r)

query(battery, ep, 130)
query(battery, ep, 130)



