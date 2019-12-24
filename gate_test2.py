from lib8008 import *

mySequencer = Sequencer(16)
mySequencer.assign(MidiGate())

def go() :
    my8008 = Jack8008()
    my8008.connect()
    my8008.outport.clear_buffer()

    samplerate = my8008.client.samplerate
    myTransport = Transport(samplerate, 120, 16)

    my8008.play([mySequencer], myTransport)
    myTransport.play([mySequencer], my8008)


go()

