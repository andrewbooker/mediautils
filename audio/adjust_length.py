#!/usr/bin/env python3

import sys
import soundfile as sf
import math

def str_to_secs(s):
    if ":" not in s:
        return float(s)
    spl = [s for s in reversed(s.split(":"))]
    total = 0.0
    for i in range(len(spl)):
        total += pow(60, i) * float(spl[i])
    return total


fn = sys.argv[1]
file_start = str_to_secs(sys.argv[2])          # eg "4:39.655"
mix_start = str_to_secs(sys.argv[3])           # eg "1:50.000"
actual_end_in_mix = str_to_secs(sys.argv[4])   # eg "48:07.163"
required_end_in_mix = str_to_secs(sys.argv[5]) # eg "48:05.846"

print("file start", file_start)
print("mix start", mix_start)
print("current mix end", actual_end_in_mix)
print("should end", required_end_in_mix)


data, sample_rate = sf.read(fn)
print(len(data), "samples at", sample_rate)
data_from_start = data[int(file_start * sample_rate):]

diff = required_end_in_mix - actual_end_in_mix
stretch = (required_end_in_mix - mix_start) / (actual_end_in_mix - mix_start)
print("diff", diff)
print("stretch", stretch)
required_length = len(data_from_start) * stretch
print("required length", required_length)
print("iterating over output samples")

array_length = math.ceil(required_length)
fn_spl = fn.split(".")
out_fn = f"{fn_spl[0]}_out.{fn_spl[1]}"
print("writing", out_fn)

with sf.SoundFile(out_fn, "wb", sample_rate, 1) as out_file:
    block = [0.0] * 1024
    for i in range(array_length):
        p = i / stretch
        p0 = math.floor(p)
        p1 = math.ceil(p)
        e = p - p0
        overrun = p1 >= array_length

        if (i % 1024 == 0 and i != 0) or overrun:
            out_file.write(block)
            block = [0.0] * 1024
        if overrun:
            break

        block[i % 1024] = ((1.0 - e) * data_from_start[p0]) + (e * data_from_start[p1])

print("done")

