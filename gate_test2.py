from lib8008 import *


#my8008 = Jack8008()
#my8008.connect()
#samplerate = my8008.client.samplerate
#my8008.outport.clear_buffer()

mySequencer = Sequencer(16)

for gates in mySequencer.sequence:
    for gate in gates:
        gate = MidiGate()
        gate.nn = 0x12
        gate.ch = 12
        print(gate.message())

#myTransport = Transport(samplerate, 120, 16)

#my8008.play([mySequencer],myTransport)
#myTransport.play([mySequencer], my8008)

