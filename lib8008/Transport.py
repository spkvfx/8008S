class Transport:
    def __init__(self, tempo=120, client=None, division=16):
        self.client = client
        self.tempo = tempo
        self.division = division
        self.clock = -1

    def tick(self, control, frames):
        standard = int(((self.client.samplerate / frames) / self.tempo * 60) / self.division)
        if control % standard is 0:
            self.clock += 1
            return True
        else:
            return False