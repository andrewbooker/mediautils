
from timeline import Timeline

fourSrcs = {
    "thing1.mp4": {
        "name": "closeUp",
        "length": 99
    },
    "thing2.mp4": {
        "name": "wide",
        "length": 99
    },
    "thing3.mp4": {
        "name": "left",
        "length": 99
    },
    "thing4.mp4": {
        "name": "right",
        "length": 99
    }
}


def test_returns_nothing_given_no_data():
    t = Timeline({})
    assert t.create() == []

def test_ignores_single_available_source_with_no_edits():
    t = Timeline({
        "thing.mp4": {
            "name": "closeUp",
            "length": 211.98
        }
    })
    assert t.create() == []

def test_lists_single_available_source_with_empty_edits():
    t = Timeline({
        "thing.mp4": {
            "name": "closeUp",
            "length": 211
        }
    }, {
        "thing.mp4": {}
    })
    assert t.create() == [["closeUp", [0, 211]]]
    assert t.create(100) == [["closeUp", [100, 111]]]

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

def test_handles_starting_midway_through_a_single_edit_specifying_start_and_end():
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
    assert t.create(7) == [["closeUp", [7, 4]]]

def test_handles_starting_midway_through_a_single_edit_with_a_sync_value():
    srcs = {
        "thing.mp4": {
            "name": "closeUp",
            "length": 211.98
        }
    }
    edits = {
        "thing.mp4": {
            "sync": 150,
            "edits": [{ "start": 5, "end": 11 }]
        }
    }
    t = Timeline(srcs, edits)
    assert t.create(7) == [["closeUp", [157, 4]]]

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

def test_produces_split_screen_if_4_items_overlap():
    edits = {
        "thing1.mp4": {
            "edits": [
                { "start": 15, "end": 41 }
            ]
        },
        "thing2.mp4": {
            "edits": [
                { "start": 19, "end": 53 }
            ]
        },
        "thing3.mp4": {
            "edits": [
                { "start": 18, "end": 41 }
            ]
        },
        "thing4.mp4": {
            "edits": [
                { "start": 20, "end": 41 }
            ]
        }
    }
    t = Timeline(fourSrcs, edits)
    assert t.create() == [
        ["closeUp", [15, 5]],
        ["closeUp", [20, 21], { "splitScreenWith": ["left", "wide", "right"]}],
        ["wide", [41, 12]]
    ]

def test_produces_split_screen_with_sync_values_if_overlap_longer_than_10s():
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
                { "start": 29, "end": 63 }
            ]
        },
        "thing3.mp4": {
            "sync": 1,
            "edits": [
                { "start": 19, "end": 42 }
            ]
        },
        "thing4.mp4": {
            "sync": 0,
            "edits": [
                { "start": 20, "end": 41 }
            ]
        }
    }
    t = Timeline(fourSrcs, edits)
    assert t.create() == [
        ["closeUp", [115, 5]],
        ["closeUp", [120, 21], { "splitScreenWith": ["left", "wide", "right"]}],
        ["wide", [51, 12]]
    ]

def test_fills_in_a_gap_between_aligned_edits():
    edits = {
        "thing1.mp4": {
            "edits": [
                { "start": 1, "end": 12 }, { "start": 43, "end": 88 }
            ]
        },
        "thing2.mp4": {
            "edits": [
                { "start": 2, "end": 14 }, { "start": 42, "end": 62 }
            ]
        },
        "thing3.mp4": {
            "edits": [
                { "start": 3, "end": 19 }, { "start": 22, "end": 49 }
            ]
        },
        "thing4.mp4": {
            "edits": [
                { "start": 4, "end": 36 }, { "start": 39, "end": 88 }
            ]
        }
    }
    t = Timeline(fourSrcs, edits)
    assert t.create() == [
        ["closeUp", [1, 3]],
        ["closeUp", [4, 8], { "splitScreenWith": ["wide", "left", "right"]}],
        ["wide", [12, 2]],
        ["left", [14, 5]],
        ["right", [19, 17]],
        ["left", [36, 7]],
        ["left", [43, 6], { "splitScreenWith": ["right", "wide", "closeUp"]}],
        ["right", [49, 39]]
    ]

def test_uses_length_to_interpret_edit_without_end():
    srcs = {
        "thing.mp4": {
            "name": "closeUp",
            "length": 20
        }
    }
    edits = {
        "thing.mp4": {
            "edits": [{ "start": 5, "end": 10 }, { "start": 15 }]
        }
    }
    t = Timeline(srcs, edits)
    assert t.create() == [
        ["closeUp", [5, 5]],
        ["closeUp", [15, 5]]
    ]

def test_can_create_from_a_given_point():
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
                { "start": 20, "end": 30 }, { "start": 35, "end": 50 }
            ]
        },
        "thing2.mp4": {
            "sync": 20,
            "edits": [
                { "start": 22, "end": 34 }, { "start": 59, "end": 69 }
            ]
        }
    }
    t = Timeline(srcs, edits)
    assert t.create(21) == [
        ["closeUp", [35, 15]],
        ["wide", [60, 9]]
    ]

def test_considers_a_file_to_begin_at_the_start_point_if_it_begins_before():
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
                { "start": 20, "end": 30 }, { "start": 35, "end": 70 }
            ]
        },
        "thing2.mp4": {
            "sync": 20,
            "edits": [
                { "start": 22, "end": 34 }, { "start": 39, "end": 69 }
            ]
        }
    }
    t = Timeline(srcs, edits)
    assert t.create(21) == [
        ["wide", [41, 28]],
        ["closeUp", [59, 11]]
    ]

def test_can_produce_a_split_screen_from_the_beginning():
    edits = {
        "thing1.mp4": {
            "edits": [
                { "start": 0, "end": 88 }
            ]
        },
        "thing2.mp4": {
            "edits": [
                { "start": 0, "end": 88 }
            ]
        },
        "thing3.mp4": {
            "edits": [
                { "start": 0, "end": 88 }
            ]
        },
        "thing4.mp4": {
            "edits": [
                { "start": 0, "end": 88 }
            ]
        }
    }
    t = Timeline(fourSrcs, edits)
    assert t.create() == [
        ["closeUp", [0, 88], { "splitScreenWith": ["wide", "left", "right"]}]
    ]

