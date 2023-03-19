
from timeline import Timeline

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

def test_lists_single_available_source_with_empty_edits():
    t = Timeline({
        "thing.mp4": {
            "name": "closeUp",
            "length": 211.98
        }
    }, {
        "thing.mp4": {}
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

def test_ignores_short_edit_entirely_overlapped_by_another():
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
                { "start": 15, "end": 21 }
            ]
        },
        "thing2.mp4": {
            "edits": [
                { "start": 17, "end": 19 }
            ]
        }
    }
    t = Timeline(srcs, edits)
    assert t.create() == [["closeUp", [15, 6]]]

def test_produces_split_screen_if_overlap_longer_than_10s():
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
                { "start": 15, "end": 41 }
            ]
        },
        "thing2.mp4": {
            "edits": [
                { "start": 20, "end": 53 }
            ]
        }
    }
    t = Timeline(srcs, edits)
    assert t.create() == [
        ["closeUp", [15, 5]],
        ["closeUp", [20, 21], { "splitScreenWith": ["wide"]}],
        ["wide", [41, 12]]
    ]

def test_produces_split_screen_with_sync_values_if_overlap_longer_than_10s():
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
            "sync": 100,
            "edits": [
                { "start": 115, "end": 141 }
            ]
        },
        "thing2.mp4": {
            "sync": 10,
            "edits": [
                { "start": 30, "end": 63 }
            ]
        }
    }
    t = Timeline(srcs, edits)
    assert t.create() == [
        ["closeUp", [115, 5]],
        ["closeUp", [120, 21], { "splitScreenWith": ["wide"]}],
        ["wide", [51, 12]]
    ]

