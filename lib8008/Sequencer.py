from .Gate import Gate


class Sequencer:
    def __init__(self, l=16, verbose=False):
        self.length = l + 1

        self.sequence = []
        for gate in range(l):
            self.sequence.append([Gate()])

        self.position = 0

        self.current_gate_list = []

        self.verbose = verbose

        self.seq = self.sequence

    def step(self, beat):
        clock = beat % self.length

        if self.verbose:
            print(self)
            print("beat:")
            print(beat)
            print("clock:")
            print(clock)
            print("******")

        #self.position = clock%self.length - 1

        if clock is 0:
            self.position += 1
        elif self.position is self.length - 1:
            self.position = 0

        self.current_gate_list = self.sequence[self.position - 1]

        for x in self.current_gate_list:
            x.trig(clock, beat)
