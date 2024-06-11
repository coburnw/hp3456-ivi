import sys
import time

#
# hit your instrument directly, bypassing IVI and the IVI driver
#
# import vxi11
# instr = vxi11.Instrument("192.168.2.9", "gpib0,22")
# instr.term_char = '\n'
# instr.write("F4W10STI")
# print instr.read()
# print instr.read()
# quit()

import ivi
from hp3456_ivi import agilent3456A

def dump():
    print( 'getting ' + instr.measurement_function)
    print( ' autorange = ' + str(instr.auto_range))
    print( ' man_range = ' + str(instr.range))
    print( ' resolution = ' + str(instr.resolution))
    val = instr.measurement.read(5)
    print( ' overrange = ' + str(instr.measurement.is_over_range(val)))
    print( ' underrange = ' + str(instr.measurement.is_under_range(val)))
    if instr.measurement.is_out_of_range(val):
        print( ' reading = ' + str(val) + ' (out of range)')
    else:
        print( ' reading = ' + str(val))
    print
    

if __name__ == '__main__':
    
    #
    # use IVI and the HP3456A driver to interact with a vxi-11 connected instrument.
    #
    instr = agilent3456A("TCPIP0::192.168.2.9::gpib0,22::INSTR")
    
    #instr.help()

    print( instr.identity.instrument_manufacturer),
    print( instr.identity.instrument_model)
    print()

    instr.measurement_function = 'dc_volts'
    instr.range = 10
    instr.resolution = 0.001
    dump()

    instr.measurement_function = 'ac_volts'
    instr.range = 10
    instr.resolution = 0.001
    dump()

    instr.measurement_function = 'ac_plus_dc_volts'
    instr.range = 10
    instr.resolution = 0.001
    dump()

    instr.measurement_function = 'two_wire_resistance'
    instr.range = 10e3
    instr.resolution = 0.00010
    dump()

    instr.measurement_function = 'two_wire_resistance'
    instr.auto_range = 'on'
    dump()

    instr.measurement_function = 'four_wire_resistance'
    instr.auto_range = 'on'
    dump()

    instr.measurement_function = 'dc_volts'
    instr.range = 10
    instr.resolution = 0.001
    dump()

