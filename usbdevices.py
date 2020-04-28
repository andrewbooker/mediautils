
import pygame.midi as midi

class UsbMidiDevices():
    def __init__(self):
        print("listing MIDI devices")
        midi.init()
        self.outputs = []
        self.inputs = []
        count = midi.get_count()
        print("found", count, "devices (including non USB)")
        for d in range(count):
            info = midi.get_device_info(d)
            name = info[1].decode("utf-8")
            
            isOutput = (info[3] == 1)
            isInput = (info[2] == 1)
            if isOutput and "USB" in name: self.outputs.append((d, name))
            if isInput and "USB" in name: self.inputs.append((d, name))
                
        print("inputs:", self.inputs)
        print("outputs:", self.outputs)
        if len(self.inputs) == 0 or len(self.outputs) == 0:
            print("need both input and output USB devices")
            exit()
        
    def forInput(self):
        return self.inputs[0][0] if len(self.inputs) > 0 else None

    def forOutput(self):
        return self.outputs[0][0] if len(self.outputs) > 0 else None

    def __del__(self):
        midi.quit()
        print("exiting MIDI")


class MidiIo():
    def __init__(self, io):
        self.io = io

    def __del__(self):
        self.io.close()
        del self.io

class MidiOut(MidiIo):
    def __init__(self, devs):
        MidiIo.__init__(self, midi.Output(devs.forOutput(), latency = 0))

class MidiIn(MidiIo):
    def __init__(self, devs):
        MidiIo.__init__(self, midi.Input(devs.forInput()))
