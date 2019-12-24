NOTEON = 0x90
NOTEOFF = 0x80

class Gate(object):
    def __init__(self, l=4, verbose=False):
        self.verbose = verbose
        self.leng = l

        self.active = True
        self.status = False
        self.sustain = False

        self.port = None

        self.msg = None

    #return the trigger event
    def trig(self, beat, clock):
        if self.active:
            if beat is 0:
                self.status = True
            elif beat is self.leng and clock is not 0 and not self.sustain and self.status is not NOTEOFF:
                self.status = False
            else:
                self.status = False
        else:
            self.status = False
        return self.status

    #return the gate's message
    #override this method to provide customized gate events
    def message(self):
        #returns garbage by default
        return (self.__dict__)

#midi message method override
class MidiGate(Gate):
    def __init__(self,  nn=0x40, v=0x40, ch=0x00):
        self.nn = nn
        self.v = v
        self.ch = ch
        self.event = 0b00000000

        super().__init__()

    def message(self):
        MSB = '1001' if self.status else '1000'
        LSB = format(self.ch, '04b')

        self.event = int(MSB + LSB, 2)

        self.msg = (self.event,
                    self.nn,
                    self.v)

        return self.msg