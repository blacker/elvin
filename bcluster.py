# By Robert M Ochshorn: rmo@mit.edu
import sys
import numpy
from operator import itemgetter
import echonest.remix.audio as audio
import scipy.cluster.vq

def run(filename):
	aa = audio.LocalAudioFile(filename)
	segs = aa.analysis.segments
	clusters = cluster_segs_by_pitch(segs, 8)
	#render_clusters(aa, clusters)

def cluster_segs_by_timbre(segs, n_clusters):
    """segs is a list of Echonest Remix segment objects
    returns a list of seglists [ [s1, s2], [s3], [s4, s5, s6] ]
    """
    # whitened_segs = scipy.cluster.vq.whiten(
    #     numpy.array(
    #         [X.seg.timbre for X in items]))
    # whitened_segs = scipy.cluster.vq.whiten(
    #     numpy.array(
    #         [X.seg.timbre + [X.seg.duration, X.seg.loudness_max] + X.seg.pitches for X in items])) # try everything
    # whitened_segs = numpy.array( # don't whiten
    #     [X.seg.timbre + [X.seg.duration, X.seg.loudness_max] + X.seg.pitches for X in items]) # try everything
    whitened_segs = numpy.array( # don't whiten
        [x.timbre for x in segs])
    code_book = scipy.cluster.vq.kmeans(whitened_segs, n_clusters)
    indices, dists = scipy.cluster.vq.vq(whitened_segs, code_book[0])
    clusters = [ [] for X in range(n_clusters) ]
    for i in range(len(indices)):
        # how well does this fit into the cluster?
        segs[i].dist = int((dists[i]-min(dists)) * 255.0 / (max(dists) - min(dists)))
        clusters[indices[i]].append(segs[i])
    return clusters

def cluster_segs_by_pitch(segs, n_clusters):
	"""
	Group segments into clusters based on pitch vectors.
	segs is a list of Echonest Remix segment objects
	returns a list of seglists [ [s1, s2], [s3], [s4, s5, s6] ]
	"""
	whitened_segs = numpy.array( # don't whiten
		[x.pitches for x in segs])
	code_book = scipy.cluster.vq.kmeans(whitened_segs, n_clusters)
    # print 'CODE BOOK :'
    # print code_book[0]
	indices, dists = scipy.cluster.vq.vq(whitened_segs, code_book[0])
	clusters = [ [] for X in range(n_clusters) ]
	for i in range(len(indices)):
		# how well does this fit into the cluster?
		segs[i].dist = int((dists[i]-min(dists)) * 255.0 / (max(dists) - min(dists)))
		clusters[indices[i]].append(segs[i])
    # print 'CLUSTERS : '
    # print clusters
	return clusters

def cluster_segs_by_pitch_winner(segs, n_clusters):
    """
    Group segments into clusters based on pitch winner.
    These clusters come back already sorted.
    segs is a list of Echonest Remix segment objects
    returns a list of seglists [ [s1, s2], [s3], [s4, s5, s6] ]
    """
    clusters = [[] for x in range(12)]
    for x in segs:
        winner = x.pitches.index(max(x.pitches))
        clusters[winner].append(x)
    for i in range(len(clusters)):
        clusters[i] = sorted(clusters[i], key=lambda x:x.pitches[i], reverse=True)
    if n_clusters < len(clusters):
        clusters = sorted(clusters, key=len, reverse=True)[:n_clusters]
    return clusters

def render_clusters(afile, clusters, filename):
    for i, clust in enumerate(clusters):
        out = audio.getpieces(afile, clust)
        filename = '%s-cluster-%i.wav' % (filename.split('.'), i)
        out.encode(filename)

def sort_clusters(clusters, sort_function, reverse=False):
    for i in range(len(clusters)):
        clusters[i] = sorted(clusters[i], key=sort_function, reverse=reverse)[:127]
    return clusters

def dist(seg):
    return seg.dist

def loudness_max(seg):
    return seg.loudness_max

def duration(seg):
    return seg.duration

if __name__=='__main__':
    filename = sys.argv[1]
    run(filename)

