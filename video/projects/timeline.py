
from enum import Enum

class SplitMode(Enum):
    NotSplit = 0
    ShouldStart = 1
    Started = 2
    Stopped = 3

class Timeline():
    @staticmethod
    def project(events, syncs):
        events.sort(key=lambda e: e["ts"])
        playable = []
        playing = {}
        tl = []
        splitMode = SplitMode.NotSplit

        for i in range(len(events)):
            e = events[i]
            src = e["src"]
            if "start" in e["action"]:
                playable.append(src)
                if len(playable) == 4:
                    splitMode = SplitMode.ShouldStart
            if "stop" in e["action"]:
                playable.remove(src)
                if splitMode == SplitMode.Started and len(playable) < 4:
                    splitMode = SplitMode.Stopped

            if len(events) > (i + 1) and events[i + 1]["ts"] != e["ts"] and len(playable) > 0 and len(playing.items()) == 0:
                if len(playable) == 4:
                    splitMode = SplitMode.Started
                playing[playable[0]] = e["ts"]

            if len(playing.items()) > 0:
                toRemove = []
                toAdd = []
                for (k, v) in playing.items():
                    sync = syncs[k] if k in syncs else 0
                    if k not in playable or splitMode == SplitMode.ShouldStart:
                        d = e["ts"] - v
                        if d > 0 and splitMode != SplitMode.Stopped:
                            tl.append([k, [v + sync, d]])
                            if splitMode == SplitMode.ShouldStart:
                                splitMode = SplitMode.Started
                        toRemove.append(k)
                        if len(playable) > 0:
                            toAdd.append(playable[0])
                    if splitMode == SplitMode.ShouldStart:
                        splitMode = SplitMode.Started
                    if splitMode == SplitMode.Stopped:
                        otherPlayable = filter(lambda p: k not in p, playable)
                        tl.append([k, [v + sync, e["ts"] - v], { "splitScreenWith": [p for p in otherPlayable] }])
                        splitMode = SplitMode.NotSplit
                for k in toRemove:
                    del playing[k]
                if len(toAdd) > 0:
                    playing[toAdd[0]] = e["ts"] #subject to weighting

        return tl

    @staticmethod
    def addTo(events, start, dur, name, startAt):
        if startAt >= (start + dur):
            return
        tss = max(start, startAt)
        tse = tss + dur - max(startAt - start, 0)

        events.append({ "ts": tss, "src": name, "action": "start" })
        events.append({ "ts": tse, "src": name, "action": "stop" })

    def __init__(self, srcs, edits = {}):
        self.srcs = srcs
        self.edits = edits

    def create(self, startAt=0):
        events = []
        syncs = {}

        for s in self.srcs:
            src = self.srcs[s]
            start = 0
            dur = src["length"]

            if s in self.edits:
                sync = self.edits[s]["sync"] if "sync" in self.edits[s] else 0
                syncs[src["name"]] = sync
                if "edits" in self.edits[s]: 
                    for edit in self.edits[s]["edits"]:
                        if "start" in edit:
                            start = edit["start"]
                            dur = src["length"] - start
                        if "end" in edit:
                            dur = edit["end"] - start

                        Timeline.addTo(events, start - sync, dur, src["name"], startAt)

                if len(events) == 0:
                    Timeline.addTo(events, start, dur, src["name"], startAt)

        return Timeline.project(events, syncs)
