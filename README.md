# Description

A library to read information from your Solax X3 solar inverter through its RS485 port.

# Cable

Connect pin 4 and 5 to the A and B ports of an USB to RS485 adapter. See page 34 of [the manual](https://www.solaxpower.com/wp-content/uploads/2020/02/X3-PRO-USER-MANUAL.pdf).

# Installation

```
pip install solax-x3-rs485
```

# Example

```
import solaxx3rs485

modbusMeter = solaxx3rs485.SolaxX3RS485Client("/dev/ttyUSB1")
data = modbusMeter.get_data()

print(data.yield_today)
```

# Credits

Based on code by "barche", see: https://github.com/InfernoEmbedded/PowerScraper/pull/16.