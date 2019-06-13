from .Gate import Gate


class Sequencer:
    def __init__(self, l):
        self.l = l + 1

        self.seq = []
        for gate in range(l):
            self.seq.append(Gate(0x40,
                                 0x40,
                                 2))

        self.position = 0

        self.current_gate = None

    def step(self, beat):
        clock = beat % self.l

        print("beat:")
        print(beat)
        print("clock:")
        print(clock)
        print("******")

        if clock is 0:
            self.position += 1
        elif self.position is self.l - 1:
            self.position = 0

        self.current_gate = self.seq[self.position - 1]
        # print(self.current_gate)

        self.current_gate.trig(clock, beat)