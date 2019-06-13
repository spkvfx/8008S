NOTEON = 0x90
NOTEOFF = 0x80

class Gate:
    def __init__(self, nn, v, l=4):

        self.nn = int(nn)
        self.v = int(v)
        self.leng = l

        self.active = True
        self.status = False
        self.sustain = False

    def trig(self, beat, clock):
        global NOTEON
        global NOTEOFF
        if self.active :
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
        else:
            self.status = False
            return False
