import jack


class Jack8008:
    def __init__(self,client_name='8008S Midi Gate',outport_name='outport',verbose=False):
        self.client_name = client_name
        self.client = None

        self.outport_name = outport_name
        self.outport = None

        self.control = 0

        self.verbose = verbose

    def connect(self):
        self.client = jack.Client(self.client_name)
        self.outport = self.client.midi_outports.register(self.outport_name)
        # self.inport = client.midi_inports.register('input')

    def send(self, msg,channel=0):
        if self.verbose:
            print(msg)
        self.outport.write_midi_event(channel, msg)

    def play(self, sequencer_list, transport):
        @self.client.set_process_callback
        def process(frames):
            self.outport.clear_buffer()
            x = transport.play(sequencer_list,self.control,frames)
            if x:
                self.send(x.message())

            self.control += 1

        self.control = 0

        with self.client:
            input()


