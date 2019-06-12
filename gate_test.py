import jack

NOTEON = 0x90
NOTEOFF = 0x80

division = 16

client = jack.Client('MIDI-Gate')
# inport = client.midi_inports.register('input')
outport = client.midi_outports.register('output')


# Gate(note number, velocity, length in divisions)
class Gate:
    def __init__(self, nn, v, l=4):
        self.nn = int(nn)
        self.v = int(v)
        self.leng = l

        self.status = False
        self.sustain = True

    def trig(self, beat, clock):
        if beat is 0 :
            self.status = NOTEON
            print("NOTEON")
            return True
        elif beat is self.leng and clock is not 0 and not self.sustain and self.status is not NOTEOFF:
            self.status = NOTEOFF
            print("NOTEOFF")
            return True
        else:
            self.status = False
            return False


class Sequencer:
    def __init__(self, l):
        self.l = l + 1

        self.seq = []
        for gate in range(l):
            self.seq.append(Gate(0x40,
                                 0x40,
                                 8))

        self.position = 0

        self.current_gate = None

    def step(self, beat):
        clock = beat % self.l

        print("beat:")
        print(beat)
        print("clock")
        print(clock)
        print("******")

        if clock is 0:
            self.position += 1
        elif self.position is self.l - 1:
            self.position = 0

        self.current_gate = self.seq[self.position - 1]
        # print(self.current_gate)

        self.current_gate.trig(clock, beat)


class Transport:
    def __init__(self, tempo):
        self.tempo = tempo
        self.clock = -1

    def tick(self, control, frames):
        standard = int(((client.samplerate / frames) / self.tempo * 60) / division)
        if control % standard is 0:
            self.clock += 1
            return True
        else:
            return False


mySequencer = Sequencer(16)
myTransport = Transport(120)

print('*********************************')
print(len(mySequencer.seq))


# program
i = 0
for gate in mySequencer.seq:
    gate.nn = gate.nn + i
    if i % 2 == 0:
        gate.nn -= 4
    elif i%3 == 0:
        gate.sustain = False
        gate.leng = 4
    else:
        gate.sustain = True
        gate.leng = 2
    if i%7 == 0:
        gate.nn += 3
        gate.sustain = mySequencer.seq[i-1].sustain
    if mySequencer.seq[i-1].nn is gate.nn:
        gate.nn += 5
    i += 1


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
