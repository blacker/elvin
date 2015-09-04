#!/usr/bin/env python
# encoding: utf-8
import sys
import os

import echonest.remix.audio as audio

import bcluster

N_CLUSTERS = 8

def main(filename):
    # get the audio analysis
    audio_file = audio.LocalAudioFile(filename)
    # prepare the output file
    basename, extension = os.path.splitext(filename)
    segment_filename = basename + '.segs'
    segment_file = open(segment_filename, 'wb')
	
    canonical_segments = get_canonical_segments(audio_file)
    
    write_segments_to_file(canonical_segments, segment_file)
    
    write_clusters_to_file(canonical_segments, segment_file)
    
    write_tempo_to_file(audio_file, segment_file)
    
    segment_file.close()
    

def get_canonical_segments(audio_file):
    """For each bar, iterate through that bar's segments
    and calculate the relative start times. Make sure we don't
    include the same segment twice."""
    bars = audio_file.analysis.bars
    seen_segments = set()
    canonical_segments = audio.AudioQuantumList()
    for bar in bars:
        for segment in bar.segments:
            abs_context = segment.absolute_context()
            segment_index = abs_context[0]
            if segment_index in seen_segments:
                continue
            relative_start_time = segment.start - bar.start
            # the following condition probably isn't necessary, because
            # the condition above will catch it. but just in case
            if relative_start_time < 0:
                continue
            segment.relative_start_time = relative_start_time
            canonical_segments.append(segment)
            seen_segments.add(segment_index)
    print 'that yielded %i canonical segments' % len(canonical_segments)
    return canonical_segments
            
def write_segments_to_file(segments, segment_file):
    for i, segment in enumerate(segments):
        data = (i, segment.start, segment.duration, segment.relative_start_time)
        row = '%i, %f %f %f;\n' % data
        segment_file.write(row)

def write_clusters_to_file(segments, segment_file):
    # clusters = bcluster.cluster_segs_by_pitch(segments, N_CLUSTERS)
    clusters = bcluster.cluster_segs_by_timbre(segments, N_CLUSTERS)
    clusters = bcluster.sort_clusters(clusters, bcluster.dist, reverse=False)
    for i, clust in enumerate(clusters):
        row = 'cluster%i,' % (i)
        for x in clust:
            row += ' %i' % (segments.index(x))
        row += ';\n'
        segment_file.write(row)

def write_tempo_to_file(audio_file, segment_file):
	tempo = audio_file.analysis.tempo.get('value', 120)
	line = 'tempo, %f;\n' % tempo
	segment_file.write(line)


if __name__ == '__main__':
    fname = sys.argv[1]
    main(fname)