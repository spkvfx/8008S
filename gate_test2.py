import jack
from lib8008 import *

client = jack.Client('MIDI-Gate')
# inport = client.midi_inports.register('input')
outport = client.midi_outports.register('output')

myTransport = Transport(120,client)
mySequencer = Sequencer(16)

print('*********************************')
print(len(mySequencer.seq))


def write_gate(gate):
    event = (gate.status,
             gate.nn,
             gate.v)

    print(event)

    outport.write_midi_event(0, event)


@client.set_process_callback
def process(frames):
    global control
    outport.clear_buffer()

    if myTransport.tick(control, frames):
        mySequencer.step(myTransport.clock)
        if mySequencer.current_gate.status:
            print(mySequencer.position)
            write_gate(mySequencer.current_gate)

    control += 1


control = 0
with client:
    input()
