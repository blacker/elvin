#!/usr/bin/env python
# encoding: utf-8
import sys
import os

import echonest.remix.audio as audio

def main(input_filename):
	audio_file = audio.LocalAudioFile(input_filename)
	bars = audio_file.analysis.bars
	histogram = dict()
	seg_start_times = []
	for i, bar in enumerate(bars):
	    segments = bar.segments
	    relative_start_times = [seg.start - bar.start for seg in segments]
	    seg_start_times.extend(relative_start_times)
	    
	for start_time in seg_start_times:
	    rounded_start_time = round(start_time, 2)
	    if rounded_start_time in histogram:
	        histogram[rounded_start_time] += 1
	    else:
	        histogram[rounded_start_time] = 1
	
	# now print that histogram
	for length in sorted(histogram.keys()):
	    line = "%.2f : " % (length)
	    for i in range(histogram[length]):
	        line = line + "x"
	    print line


if __name__ == '__main__':
    filename = sys.argv[1]
    main(filename)

