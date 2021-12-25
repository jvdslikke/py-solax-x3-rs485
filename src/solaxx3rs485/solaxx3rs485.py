from pymodbus.client.sync import ModbusSerialClient
from pymodbus.exceptions import ModbusException

def unsigned16(result, addr):
    return result.getRegister(addr)

def join_msb_lsb(msb, lsb):
    return (msb << 16) | lsb 
    
class SolaxX3RS485Exception(Exception):
    pass

class SolaxX3RS485Data:
    def __init__(self, modbusresult):
        self.pv1_input_voltage = unsigned16(modbusresult, 0) / 10
        self.pv2_input_voltage = unsigned16(modbusresult, 1) / 10
        self.pv1_input_current = unsigned16(modbusresult, 2) / 10
        self.pv2_input_current = unsigned16(modbusresult, 3) / 10
        self.grid_voltage_phase_1 = unsigned16(modbusresult, 4) / 10
        self.grid_voltage_phase_2 = unsigned16(modbusresult, 5) / 10
        self.grid_voltage_phase_3 = unsigned16(modbusresult, 6) / 10
        self.grid_frequency_phase_1 = unsigned16(modbusresult, 7) / 100
        self.grid_frequency_phase_2 = unsigned16(modbusresult, 8) / 100
        self.grid_frequency_phase_3 = unsigned16(modbusresult, 9) / 100
        self.output_current_phase_1 = unsigned16(modbusresult, 10) / 10
        self.output_current_phase_2 = unsigned16(modbusresult, 11) / 10
        self.output_current_phase_3 = unsigned16(modbusresult, 12) / 10
        self.temperature = unsigned16(modbusresult, 13)
        self.inverter_power = unsigned16(modbusresult, 14)
        self.run_mode = unsigned16(modbusresult, 15)
        self.output_power_phase_1 = unsigned16(modbusresult, 16)
        self.output_power_phase_2 = unsigned16(modbusresult, 17)
        self.output_power_phase_3 = unsigned16(modbusresult, 18)
        self.total_dc_power = unsigned16(modbusresult, 19)
        self.pv1_dc_power = unsigned16(modbusresult, 20)
        self.pv2_dc_power = unsigned16(modbusresult, 21)
        self.fault_value_of_phase_1_voltage = unsigned16(modbusresult, 22) / 10
        self.fault_value_of_phase_2_voltage = unsigned16(modbusresult, 23) / 10
        self.fault_value_of_phase_3_voltage = unsigned16(modbusresult, 24) / 10
        self.fault_value_of_phase_1_frequency = unsigned16(modbusresult, 25) / 100
        self.fault_value_of_phase_2_frequency = unsigned16(modbusresult, 26) / 100
        self.fault_value_of_phase_3_frequency = unsigned16(modbusresult, 27) / 100
        self.fault_value_of_phase_1_dci = unsigned16(modbusresult, 28) / 1000
        self.fault_value_of_phase_2_dci = unsigned16(modbusresult, 29) / 1000
        self.fault_value_of_phase_3_dci = unsigned16(modbusresult, 30) / 1000
        self.fault_value_of_pv1_voltage = unsigned16(modbusresult, 31) / 10
        self.fault_value_of_pv2_voltage = unsigned16(modbusresult, 32) / 10
        self.fault_value_of_temperature = unsigned16(modbusresult, 33)
        self.fault_value_of_gfci = unsigned16(modbusresult, 34) / 1000
        self.total_yield = join_msb_lsb(unsigned16(modbusresult, 36), unsigned16(modbusresult, 35)) / 1000
        self.yield_today = join_msb_lsb(unsigned16(modbusresult, 38), unsigned16(modbusresult, 37)) / 1000
        


class SolaxX3RS485Client:
    def __init__(self, port, unit=1):
        self.unit = unit
        self.client = ModbusSerialClient(method="rtu", port=port, baudrate=9600, parity='N', 
                                            stopbits=1, timeout=1)
        
    def get_data(self) -> SolaxX3RS485Data:
        modbusresult = self.client.read_input_registers(0X400, 53, unit=self.unit)
        if isinstance(modbusresult, ModbusException):
            raise SolaxX3RS485Exception("Error reading data from Solax device") from modbusresult
            
        result =  SolaxX3RS485Data(modbusresult)
        return result
        