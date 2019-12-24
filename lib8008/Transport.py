#from .Jack8008 import *

class Transport:
    def __init__(self, samplerate=1000, tempo=120, division=16, control=0):

        self.samplerate = samplerate

        self.tempo = tempo
        self.division = division
        self.clock = -1
        self.control = control

        self.sequencer_list = None
        self.transport = None

    def tick(self, control=0, frames=1):
        standard = int(((self.samplerate / frames) / self.tempo * 60) / self.division)
        if control % standard is 0:
            self.clock += 1
            return True
        else:
            return False

    def play(self, sequencer_list, control=0, frames=1):
        if self.tick(control, frames):
            for sequencer in sequencer_list:
                sequencer.step(self.clock)
                for gate in sequencer.current_gate_list:
                    if gate.status:
                        return gate
        return False
