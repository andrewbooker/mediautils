

class MidiFileWriter:
    def __init__(self, fqfn):
        self.tempo = 0
        self.fqfn = fqfn
        self.notes = {"top": [], "bass": []}
        
    def setTempo(self, t):
        self.tempo = t

    def addNote(self, part, note, velocity, duration):
        self.notes[part].append((note, velocity, duration))

    def _endTrack(self, track):
        data = [] + track
        data.append(0)
        data.extend([0xff, 0x2f, 0x00]) # end of track
        self.outFile.write(str.encode("MTrk"))
        dataLength = len(data)
        self.outFile.write(bytes([(dataLength >> 24) % 256, (dataLength >> 16) % 256, (dataLength >> 8) % 256, dataLength % 256])) # as 32-bit number
        self.outFile.write(bytes(data))

    def _tempoTrack(self, tempo):
        if tempo == 0:
            return;
        data = []
        microsPerBeat = int(60000000 / tempo);
        data.append(0) # time since previous event (nothing)
        data.extend([0xff, 0x51, 0x03]) # set tempo (using 3 bytes, ie 24-bit number)
        data.extend([(microsPerBeat >> 16) % 256, (microsPerBeat >> 8) % 256, microsPerBeat % 256]) # tempo as 24-bit number of microseconds per quarter note
        data.append(0)  # time since previous event (nothing)
        data.extend([0xff, 0x58, 0x04]) # set time signature (using 4 bytes)
        data.extend([4, 2])  # music in 4/4 = nn/2^dd = 4/2^2
        data.extend([24, 8]) # these may not be important, about MIDI clock (not necessary here): 24 = MIDI Clocks per metronome tick, 8 = Number of 1/32 notes per 24 MIDI clocks (8 is standard)
        self._endTrack(data)

    def _noteLength(self, dur):
        ret = [((dur % 256) & 0x7f)]
        if (dur < 128):
            return ret
        return [((dur % 256) >> 7) + (0x80 | (dur >> 8) << 1)] + ret

    def __del__(self):
        trackCount = 3 if self.tempo > 0 else 2
        self.outFile = open(self.fqfn, "wb")
        self.outFile.write(str.encode("MThd"))
        self.outFile.write(bytes([0, 0, 0, 6])) #header length = 6
        self.outFile.write(bytes([0, 1])) #file type = 2
        self.outFile.write(bytes([0, trackCount]))
        self.outFile.write(bytes([0, 32])) # 32 ticks per quarter note
        
        self._tempoTrack(self.tempo)
        for part, notes in self.notes.items():
            data = []
            data.append(0) # time since previous event (nothing)
            data.extend([0xff, 0x03]) # set track name
            data.append(len(part))
            data.extend(str.encode(part))
            for note in notes:
                data.append(0)
                data.extend([0x90, note[0], note[1]])
                data.extend(self._noteLength(8 * note[2])) # 8= ticks per 16th
                data.extend([0x80, note[0], 0x00])
            self._endTrack(data)
        self.outFile.close()
