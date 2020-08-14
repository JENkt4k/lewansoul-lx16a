import usb.core
import usb.util
import sys

# commands
CMD_SERVO_MOVE = 3
CMD_ACTION_GROUP_RUN = 6
CMD_ACTION_STOP = 7
CMD_ACTION_SPEED = 11
CMD_GET_BATTERY_VOLTAGE = 15
CMD_MULT_SERVO_UNLOAD = 20
CMD_MULT_SERVO_POS_READ = 21
#

def query(command, endpoint):
  endpoint.write(bytes(command))
  r=dev.read(endpoint.bEndpointAddress, 1024, 1000)
  print(len(r))
  print(r)

# find our device
dev = usb.core.find(idVendor=0x0483, idProduct=0x5750)

# was it found?
if dev is None:
    raise ValueError('Device not found')

for cfg in dev:
    sys.stdout.write(str(cfg.bConfigurationValue) + '\n')
    for intf in cfg:
        sys.stdout.write('\t interface number,setting ' + \
                         str(intf.bInterfaceNumber) + \
                         ',' + \
                         str(intf.bAlternateSetting) + \
                         '\n')
        for ep in intf:
            sys.stdout.write('\t\t address ' + \
                             str(ep.bEndpointAddress) + \
                             '\n' + \
                               '\t\t direction ' + \
                                 str(usb.util.endpoint_direction(ep.bEndpointAddress) == usb.util.ENDPOINT_OUT) +'\n'
                                 '\t\t direction ' + \
                                 str(usb.util.endpoint_direction(ep.bEndpointAddress) == usb.util.ENDPOINT_IN) +'\n'
                                 )



# set the active configuration. With no arguments, the first
# configuration will be the active one
# dev.set_configuration()

# # get an endpoint instance
# cfg = dev.get_active_configuration()
# intf = cfg[(0,0)]


# ep = usb.util.find_descriptor(
#     intf,
#     # match the first OUT endpoint
#     custom_match = \
#     lambda e: \
#         usb.util.endpoint_direction(e.bEndpointAddress) == \
#         usb.util.ENDPOINT_OUT)

# assert ep is not None

# # write the data
# ep.write(bytes(CMD_GET_BATTERY_VOLTAGE))
# print(ep.bEndpointAddress)
# r=dev.read(ep.bEndpointAddress, 1024, 100)
# print(len(r))
# print(r)

# query(CMD_MULT_SERVO_POS_READ, ep)



