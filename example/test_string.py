import usb.core
import usb.util
import sys
import math
import time

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
# looks like 256 bits
# 64 results, 2 results per byte, 32 bytes total, 

# read positions 1 - 6
# length === number of servos + 3 ==> 6 servos + 3 = 0x09 
position=[0x55, 0x55, 0x09, 0x15, 0x06, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06]

# move servo
# header, length === number of servos + 3 ==> 6 servos + 3 = 0x09, command 0x3, ID, time (2b), position (2b) 
move_servos =[0x55, 0x55, 0x0B, 0x03, 0x02, 0xE8, 0x03, 0x01, 0xE8, 0x03, 0x02, 0xE8, 0x03]
move_servos2=[0x55, 0x55, 0x0B, 0x03, 0x02, 0xE8, 0x03, 0x01, 0xF4, 0x01, 0x02, 0xF4, 0x01]
stop=[0x55, 0x55, 0x02, 0x07]

def lower_byte(value):
    return int(value) % 256


def higher_byte(value):
    return int(value / 256) % 256


def word(low, high):
    #print(hex(low) + " " + hex(high))
    return int(low) + int(high)*256

def get_byte_at_32(array, index):
  if index < 0:
    raise Exception('spam', 'eggs')
  elif index == 0:
    return word(array[0],array[1])
  return word(array[2*index],array[2*index+1])

def print_hex(array):
  result = [get_byte_at_32(array,i) for i in range(math.floor(len(array)/2))]
  print(result)
  #print('TODO')

def print_read_servos(array):
  # read header
  # 2 bytes 55 555
  # 1 byte length
  # 1 byte command 
  out = [word(array[0], array[1]),
    word(array[2], 0),
    word(array[3], 0)]
  # first byte is number of servos read
  out.append(word(array[4], 0))
  for i in range(5, len(array[5:]), 3):
    # servo number
    out.append([word(array[i],0),word(array[i+1],array[i+2])])

  print(out)

def print_move_servos(array):
  # read header
  # 2 bytes 55 555
  # 1 byte length
  # 1 byte command 
  out = [word(array[0], array[1]),
    word(array[2], 0),
    word(array[3], 0)]
  # first byte is number of servos read
  out.append(word(array[4], 0))
  numServos = word(array[4], 0)
  # time is 2b
  timeout =  word(array[5], array[6])
  out.append(timeout)
  # get all servo ids positions (2b)
  # for i in range(6, len(array[6:]), 3):
  #   # servo number, position
  #   out.append([word(array[i],0),word(array[i+1],array[i+2])])
  assert(numServos*3+7 < len(array)+1)
  for i in range(numServos):
    index = i*3 + 7
    out.append([word(array[index],0),word(array[index+1],array[index+2])])
  # for i in range(5, len(array[5:]), 5):
  #   # time value(2bytes), servo ID, position(2 bytes) 
  #   out.append([word(array[i],array[i+1]),word(array[i+2],0),word(array[i+3],array[i+4])])

  print(out)

def query(command, writeEp, readEpId):
  writeEp.write(bytes(command))
  r=dev.read(readEpId, 1024,17)
  print(len(r))
  print(r)
  print_hex(r)
  # a= word(r[4], r[5])
  # print(a)

def read(command, writeEp, readEpId):
  writeEp.write(bytes(command))
  r=dev.read(readEpId, 1024,495)
  print(len(r))
  print(r)
  print_read_servos(r)

def move(command, writeEp, readEpId):
  timeout=word(command[5],command[6])
  writeEp.write(bytes(command))
  time.sleep(timeout/1000)
  # writeEp.write(bytes(stop))
  # r=dev.read(readEpId, 1024,495)
  # print(len(r))
  # print(r)
  # print_read_servos(r)

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
# ep.write(bytes(CMD_GET_BATTERY_VOLTAGE))
# ep.write(bytes(battery))
# print(ep.bEndpointAddress)
# r=dev.read(130, 64)
# print(len(r))
# print(r)
# print(r[1])
# print_hex(r)

query(battery, ep, 130)
read(position,ep,130)
query(battery, ep, 130)
print_move_servos(move_servos)
move(move_servos, ep, 130)
print_move_servos(move_servos2)
move(move_servos2, ep, 130)



