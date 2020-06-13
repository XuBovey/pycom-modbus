import machine
import time
from uModBus.serial import Serial
from uModBus.common import Request
import uModBus.const as Const

######################## DS18B20  #############################
from machine import Pin
from ds18x20 import DS18X20

ds=DS18X20(Pin('Y10'))
print(ds.read_temp())


######################## WORK AS SLAVE  #############################
slave_addr_list = [0x0A,0x0B]

register_value = [100,200,300,400] ## 100对应register_addr=0
coil_value = [0,1,0,0, 1,0,1,0]

def modbusHandle(request):
    print("function_code: {:x}".format(request.function))
    print("register_addr: {:x}".format(request.register_addr))
    value_list = []

    if request.function in [Const.READ_COILS, Const.READ_DISCRETE_INPUTS]:
        if len(register_value) < (request.register_addr+request.quantity):
            request.send_exception(Const.ILLEGAL_DATA_ADDRESS)
            return
        print("quantity: {:d}".format(request.quantity))
        
        for index in range (request.register_addr, request.register_addr + request.quantity):
            value_list.append(coil_value[index])
        request.send_response(value_list)

    elif request.function in [Const.READ_HOLDING_REGISTERS, Const.READ_INPUT_REGISTER]:
        if len(register_value) < (request.register_addr+request.quantity):
            request.send_exception(Const.ILLEGAL_DATA_ADDRESS)
            return
        print("quantity: {:d}".format(request.quantity))
        for index in range (request.register_addr, request.register_addr + request.quantity):
            value_list.append(register_value[index])
        request.send_response(value_list)

    elif request.function == Const.WRITE_SINGLE_COIL:
        if coil_value.len() < request.register_addr:
            request.send_exception(Const.ILLEGAL_DATA_ADDRESS)
            return
        
        coil_value[request.register_addr] = request.data
        request.send_response()


    elif request.function == Const.WRITE_SINGLE_REGISTER:
        if len(register_value) < request.register_addr:
            request.send_exception(Const.ILLEGAL_DATA_ADDRESS)

        register_value[request.register_addr] = request.data
        request.send_response()
            

    # elif request.function == Const.WRITE_MULTIPLE_COILS:
    #     request.quantity = struct.unpack_from('>H', data, 4)[0]
    # elif request.function == Const.WRITE_MULTIPLE_REGISTERS:
    #     request.quantity = struct.unpack_from('>H', data, 4)[0]
    else:
        print("not support yet, but come soon~~")

######################### RTU SERIAL MODBUS #########################
if __name__ == '__main__':
    print("start modbus")
    modbus_obj = Serial(4)
    timeout_ms = 10
    while 1:
        time.sleep(0.05)
        try:
            request = modbus_obj.get_request(slave_addr_list, timeout_ms)
            if request is not None:
                modbusHandle(request)
        finally:
            pass

