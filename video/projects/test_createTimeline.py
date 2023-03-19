

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



def test_returns_nothing_given_no_data():
    t = Timeline({})
    assert t.create() == []

def test_lists_single_available_source_with_no_edits():
    t = Timeline({
        "thing.mp4": {
            "name": "closeUp",
            "length": 211.98
        }
    })
    assert t.create() == [["closeUp", [0, 211.98]]]

def test_breaks_up_single_source_given_single_edit_specifying_start():
    srcs = {
        "thing.mp4": {
            "name": "closeUp",
            "length": 211.98
        }
    }
    edits = {
        "thing.mp4": {
            "edits": [{ "start": 5 }]
        }
    }
    t = Timeline(srcs, edits)
    assert t.create() == [["closeUp", [5, 206.98]]]

def test_breaks_up_single_source_given_single_edit_specifying_end():
    srcs = {
        "thing.mp4": {
            "name": "closeUp",
            "length": 211.98
        }
    }
    edits = {
        "thing.mp4": {
            "edits": [{ "end": 11 }]
        }
    }
    t = Timeline(srcs, edits)
    assert t.create() == [["closeUp", [0, 11]]]

def test_breaks_up_single_source_given_single_edit_specifying_start_and_end():
    srcs = {
        "thing.mp4": {
            "name": "closeUp",
            "length": 211.98
        }
    }
    edits = {
        "thing.mp4": {
            "edits": [{ "start": 5, "end": 11 }]
        }
    }
    t = Timeline(srcs, edits)
    assert t.create() == [["closeUp", [5, 6]]]

def test_breaks_up_single_source_given_two_edits():
    srcs = {
        "thing.mp4": {
            "name": "closeUp",
            "length": 211.98
        }
    }
    edits = {
        "thing.mp4": {
            "edits": [
                { "start": 5, "end": 11 },
                { "start": 17 }
            ]
        }
    }
    t = Timeline(srcs, edits)
    assert t.create() == [
        ["closeUp", [5, 6]],
        ["closeUp", [17, 194.98]]
    ]

def test_interleaves_multiple_sources_with_no_overlaps():
    srcs = {
        "thing1.mp4": {
            "name": "closeUp",
            "length": 99
        },
        "thing2.mp4": {
            "name": "wide",
            "length": 99
        }
    }
    edits = {
        "thing1.mp4": {
            "edits": [
                { "start": 5, "end": 11 },
                { "start": 18, "end": 21 }
            ]
        },
        "thing2.mp4": {
            "edits": [
                { "start": 11, "end": 18 },
                { "start": 21, "end": 30 }
            ]
        }
    }
    t = Timeline(srcs, edits)
    assert t.create() == [
        ["closeUp", [5, 6]],
        ["wide", [11, 7]],
        ["closeUp", [18, 3]],
        ["wide", [21, 9]]
    ]

def test_runs_one_source_edit_to_completion_before_interleaving_to_the_next():
    srcs = {
        "thing1.mp4": {
            "name": "closeUp",
            "length": 99
        },
        "thing2.mp4": {
            "name": "wide",
            "length": 99
        }
    }
    edits = {
        "thing1.mp4": {
            "edits": [
                { "start": 5, "end": 11 },
                { "start": 18, "end": 21 }
            ]
        },
        "thing2.mp4": {
            "edits": [
                { "start": 10, "end": 18 },
                { "start": 19, "end": 30 }
            ]
        }
    }
    t = Timeline(srcs, edits)
    assert t.create() == [
        ["closeUp", [5, 6]],
        ["wide", [11, 7]],
        ["closeUp", [18, 3]],
        ["wide", [21, 9]]
    ]

def test_adjusts_timings_with_no_overlap_given_sync_points():
    srcs = {
        "thing1.mp4": {
            "name": "closeUp",
            "length": 99
        },
        "thing2.mp4": {
            "name": "wide",
            "length": 99
        }
    }
    edits = {
        "thing1.mp4": {
            "sync": 10,
            "edits": [
                { "start": 15, "end": 21 },
                { "start": 28, "end": 31 }
            ]
        },
        "thing2.mp4": {
            "sync": 100,
            "edits": [
                { "start": 111, "end": 118 },
                { "start": 121, "end": 130 }
            ]
        }
    }
    t = Timeline(srcs, edits)
    assert t.create() == [
        ["closeUp", [15, 6]],
        ["wide", [111, 7]],
        ["closeUp", [28, 3]],
        ["wide", [121, 9]]
    ]

