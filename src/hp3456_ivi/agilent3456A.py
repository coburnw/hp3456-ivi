"""

Python Interchangeable Virtual Instrument Library

agilent3456A.py
Copyright (c) 2024 Coburn Wightman

Derived from agilent436A.py
Copyright (c) 2012-2017 Alex Forencich

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

"""

import math

import ivi
from ivi import dmm

Auto = set(['off', 'on'])
MeasurementFunctionMapping = {'dc_volts' : 'F1',
                              'ac_volts' : 'F2',
                              'ac_plus_dc_volts' : 'F3',
                              'two_wire_resistance' : 'F4',
                              'four_wire_resistance' : 'F5'}

# voltage range starts at 100mV
VoltageRangeMapping = {1e-1 : 'R2',
                       1e0 : 'R3',
                       1e1 : 'R4',
                       1e2 : 'R5',
                       1e3 : 'R6'}

# resistance starts at 100ohms
ResistanceRangeMapping = {1e2 : 'R2',
                          1e3 : 'R3',
                          1e4 : 'R4',
                          1e5 : 'R5',
                          1e6 : 'R6',
                          1e7 : 'R7',
                          1e8 : 'R8',
                          1e9 : 'R9'}

class agilent3456A(ivi.Driver, dmm.Base):
    "Agilent HP3456A Digital Voltmeter"

    def __init__(self, *args, **kwargs):
        self.__dict__.setdefault('_instrument_id', '3456A')

        super(agilent3456A, self).__init__(*args, **kwargs)

        self._identity_description = "Agilent HP3456A Digital Voltmeter"
        self._identity_identifier = ""
        self._identity_revision = ""
        self._identity_vendor = ""
        self._identity_instrument_manufacturer = "Agilent Technologies"
        self._identity_instrument_model = ""
        self._identity_instrument_firmware_revision = ""
        self._identity_specification_major_version = 3
        self._identity_specification_minor_version = 0
        self._identity_supported_instrument_models = ['3456A']

    def _initialize(self, resource=None, id_query=False, reset=False, **keywargs):
        "Opens an I/O session to the instrument."

        super(agilent3456A, self)._initialize(resource, id_query, reset, **keywargs)

        # configure interface
        if self._interface is not None:
            self._interface.term_char = '\n'

        # interface clear
        if not self._driver_operation_simulate:
            self._clear()

        # check ID
        if id_query and not self._driver_operation_simulate:
            id = self.identity.instrument_model
            id_check = self._instrument_id
            id_short = id[:len(id_check)]
            if id_short != id_check:
                raise Exception("Instrument ID mismatch, expecting %s, got %s", id_check, id_short)

        # reset
        if reset:
            self.utility_reset()

    def _load_id_string(self):
        if self._driver_operation_simulate:
            self._identity_instrument_manufacturer = "Not available while simulating"
            self._identity_instrument_model = "Not available while simulating"
            self._identity_instrument_firmware_revision = "Not available while simulating"
        else:
            #lst = self._ask("*IDN?").split(",")
            self._identity_instrument_manufacturer = "HP"
            self._identity_instrument_model = "3456A"
            self._identity_instrument_firmware_revision = "Unknown"
            self._set_cache_valid(True, 'identity_instrument_manufacturer')
            self._set_cache_valid(True, 'identity_instrument_model')
            self._set_cache_valid(True, 'identity_instrument_firmware_revision')

    def _get_identity_instrument_manufacturer(self):
        if self._get_cache_valid():
            return self._identity_instrument_manufacturer
        self._load_id_string()
        return self._identity_instrument_manufacturer

    def _get_identity_instrument_model(self):
        if self._get_cache_valid():
            return self._identity_instrument_model
        self._load_id_string()
        return self._identity_instrument_model

    def _get_identity_instrument_firmware_revision(self):
        if self._get_cache_valid():
            return self._identity_instrument_firmware_revision
        self._load_id_string()
        return self._identity_instrument_firmware_revision

    def _utility_disable(self):
        pass

    def _utility_error_query(self):
        error_code = 0
        error_message = "No error"
        #if not self._driver_operation_simulate:
        #    error_code, error_message = self._ask(":system:error?").split(',')
        #    error_code = int(error_code)
        #    error_message = error_message.strip(' "')
        return (error_code, error_message)

    def _utility_lock_object(self):
        pass

    def _utility_reset(self):
        if not self._driver_operation_simulate:
            self._write("H")
            self._clear()
            self.driver_operation.invalidate_all_attributes()

    def _utility_reset_with_defaults(self):
        self._utility_reset()

    def _utility_self_test(self):
        raise ivi.OperationNotSupportedException()

    def _utility_unlock_object(self):
        pass

    # end of base class

    def _get_measurement_function(self):
        return self._measurement_function

    def _set_measurement_function(self, value):
        if value not in MeasurementFunctionMapping:
            raise ivi.ValueNotSupportedException()
        self._measurement_function = value

    def _measurement_abort(self):
        self._clear()

    def _measurement_fetch(self):
        if self._driver_operation_simulate:
            return
        val = self._read()
        f = float(val[0:12])
        return f

    def _measurement_initiate(self):
        if self._driver_operation_simulate:
            return
        cmd = MeasurementFunctionMapping[self._measurement_function]
        if self._auto_range == 'on':
            cmd += 'R1'
        elif 'volts' in self._measurement_function:
            cmd += VoltageRangeMapping[self._range]
        else:
            cmd += ResistanceRangeMapping[self._range]
        self._write(cmd)

    def _measurement_read(self, maximum_time):
        self._measurement_initiate()
        return self._measurement_fetch()

    def _measurement_is_out_of_range(self, value):
        return self._measurement_is_over_range(value) or self._measurement_is_under_range(value)

    # the 3456a returns a positive inf for both positive or negative out of bounds
    def _measurement_is_over_range(self, value):
        if value > +1.999990E15:
            return True
        return False

    # the 3456a returns a negative inf for math error.  What to do?
    def _measurement_is_under_range(self, value):
        if value < -1.999990E15:
            return True
        return False

    def _get_range(self):
        return self._range

    def _set_range(self, value):
        value = float(value)
        value = math.pow(10, math.ceil(math.log10(value)))
        func = self._get_measurement_function()
        if ('volts' in func) and (value in VoltageRangeMapping):
            pass
        elif ('resistance' in func) and (value in ResistanceRangeMapping):
            pass
        else:
            raise ivi.ValueNotSupportedException()
        self._range = value

    def _get_resolution(self):
        return self.range / 1e6

    def _set_resolution(self, value):
        value = float(value)
        self.range = value * 1e6

    ########## (todo) from dmm.py
    
    # def _get_trigger_delay(self):
    #     return self._trigger_delay
    
    # def _set_trigger_delay(self, value):
    #     value = float(value)
    #     self._trigger_delay = value
    
    # def _get_trigger_delay_auto(self):
    #     return self._trigger_delay_auto
    
    # def _set_trigger_delay_auto(self, value):
    #     value = bool(value)
    #     self._trigger_delay_auto = value
    
    # def _get_trigger_source(self):
    #     return self._trigger_source
    
    # def _set_trigger_source(self, value):
    #     value = str(value)
    #     self._trigger_source = value
        
    # def _trigger_configure(self, source, delay):
    #     self._set_trigger_source(source)
    #     if isinstance(delay, bool):
    #         self._set_trigger_auto_delay(delay)
    #     else:
    #         self._set_trigger_delay(delay)
    

