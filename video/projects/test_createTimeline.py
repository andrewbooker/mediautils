

class Timeline():
    def __init__(self, srcs, edits = {}):
        self.srcs = srcs
    
    def create(self):
        t = []
        for s in self.srcs:
            src = self.srcs[s]
            t.append([src["name"], [0, src["length"]]])
        return t
        
def test_returns_nothing_given_no_data():
    t = Timeline({})
    assert t.create() == []

def test_lists_single_available_source():
    t = Timeline({
        "thing.mp4": {
            "name": "closeUp",
            "length": 211.98
        }
    })
    assert t.create() == [["closeUp", [0, 211.98]]]
