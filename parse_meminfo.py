#!/usr/bin/python3
#
# ========================================================================================
# 20120222 RAD Hacked mem_usage from pi_health.py to illutrate the building of a dict
#              from a "file".
#
# ========================================================================================
#
import re

# ----------------------------------------------------------------------------------------
#   Get memory usage data.
#
#   Read /proc/meminfo and parse the lines into a dict where the key is the parameter
#   and the value is the size in kB.  We use several lines now, but all are loaded
#   in meminfoarray[]
#
# line---key---------------size-------------
#   0   MemTotal:         949444 kB   <---
#   3   MemAvailable:     791532 kB   <---
#   8   SwapTotal:        102396 kB   <---
#  10   SwapFree:         102396 kB   <---
#
# ----------------------------------------------------------------------------------------
def mem_usage():

	meminfoarray = dict()
	fileHandle = open( "/proc/meminfo","r" )
	line = fileHandle.readlines()
	fileHandle.close()
#DEBUG#	print( "DEBUG: line array --->\n{}".format( line ) )
	for iii in range(0, len(line)):
#DEBUG#		print( "line {} = \"{}\"".format( iii, line[iii].strip() ) )
		# ------------------------------------------------------------------------
		#  NOTE: See https://pythonexamples.org/python-re-split/
		#             Use '+' rather than '*'
		#                        (which inappropriately allows for 0 matches.)
		# ------------------------------------------------------------------------
		tok = re.split("[: \t]+", line[iii])
#DEBUG#		print( "len = {}".format( len(tok) ) )
#DEBUG#		for jjj in range(0, len(tok)):
#DEBUG#			print( "{:5d} \"{}\"".format( jjj, tok[jjj].strip() ) )
		if len(tok) == 3 :
			meminfoarray[ tok[0] ] = tok[1].strip()

	print( meminfoarray )
	exit


# ----------------------------------------------------------------------------------------
# This handles the startup and shutdown of the script.
# ----------------------------------------------------------------------------------------
if __name__ == '__main__':
	mem_usage()

