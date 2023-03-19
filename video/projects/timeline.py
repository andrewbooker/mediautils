
class Timeline():
    @staticmethod
    def add(src, sync, start, dur, to):
        to.append({ "seqStart": start - sync, "seqEnd": start + dur - sync, "entry": [src["name"], [start, dur]] })

    @staticmethod
    def collate(tl):
        r = []
        lastEnd = 0
        tl.sort(key=lambda t: t["seqStart"])
        for t in tl:
            if lastEnd > t["seqStart"]:
                dur = t["seqEnd"] - lastEnd
                r.append({ "seqStart": lastEnd, "seqEnd": lastEnd + dur, "entry": [t["entry"][0], [lastEnd, dur]]})
            else:
                r.append(t)
            lastEnd = t["seqEnd"]
        return r

    def __init__(self, srcs, edits = {}):
        self.srcs = srcs
        self.edits = edits

    def create(self):
        t = []
        for s in self.srcs:
            src = self.srcs[s]
            start = 0
            dur = src["length"]

            if s in self.edits:
                sync = self.edits[s]["sync"] if "sync" in self.edits[s] else 0
                if "edits" in self.edits[s]: 
                    for edit in self.edits[s]["edits"]:
                        if "start" in edit:
                            start = edit["start"]
                            dur = src["length"] - start
                        if "end" in edit:
                            dur = edit["end"] - start

                        Timeline.add(src, sync, start, dur, t)
            if len(t) == 0:
                Timeline.add(src, 0, start, dur, t)

        return [e["entry"] for e in Timeline.collate(t)]
