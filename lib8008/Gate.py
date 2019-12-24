class Gate(object):
    def __init__(self, l=2, verbose=False):
        self.verbose = verbose
        self.leng = l

        self.active = True
        self.status = False
        self.sustain = False

        self.port = None

        self.msg = None

    #return the trigger event
    def trig(self, clock, beat):
        if self.active:
            if clock is 0:
                self.status = "H"
            elif (clock is self.leng) and (clock is not 0) and (self.status is not "L"):
                self.status = "L"
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

        self.event = 0x00

        super().__init__()

    def message(self):
        MSB = '1001' if self.status else '1000'
        LSB = format(self.ch, '04b')

        self.event = 0x90 if self.status is "H" else 0x80 if self.status is "L" else self.status
        #self.event = self.ffi.cast("uintptr_t", int(MSB + LSB, 2))

        self.msg = (self.event,
                    self.nn,
                    self.v)

        return self.msg