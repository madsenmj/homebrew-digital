# Ben Eater's 8-bit Computer from ICs

A re-creation following [Ben Eater's tutorial](https://www.youtube.com/playlist?list=PLowKtXNTBypGqImE405J2565dvjafglHU) creating the full 8-bit computer using built-in tools in Digital. 

In this version, both the EEPROM and the RAM are programmed with an inital state using the python file `eater_8bit_digital.py`. In this case, programming the RAM loads the memory when the simulation is starting, saving having to reprogram memory every time the simulation runs. The final progam (counting up to 256 and down again), which demonstrates the full Turing complete processor, is the current default program.
