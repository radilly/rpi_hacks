#!/usr/bin/python
#
#   Use /proc/stat to calculate cpu utilization as a percentage.
#
#   This should work with a very generic Python installation.
#
# ========================================================================================
# 20171215 RAD Could use a class for data hiding.  This incoroporates the initialization
#              into the first call.
#              This version, the first, has a lot of debug junk in it.
#
# ========================================================================================

import re			# For demo
import datetime 		# For demo
from time import sleep		# For demo

interval = 15			# For demo

proc_stat_busy = -1		# Sentinal value
proc_stat_idle = -1
proc_stat_hist = []		# Holds last proc_stat_hist_n samples
proc_stat_hist_n = 10		# Control length of history array to keep

# ----------------------------------------------------------------------------------------
#  Read and parse the first line of "/proc/stat", the cpu line, and calulate the
#  average cpu utilization as a percentage.
#
#  First call is the initialization - usage since boot-up.
#  Subsequent calls find the avergae utilization since the previous call.
#
# ----------------------------------------------------------------------------------------
def proc_stat() :
	global proc_stat_busy
	global proc_stat_idle
	global proc_stat_hist

	# --------------------------------------------------------------------------------
	# Work backwards from the end of the most recent file looking for
	# one of the lines above.
	# --------------------------------------------------------------------------------

	fileHandle = open ( "/proc/stat","r" )
	lineList = fileHandle.readlines()
	fileHandle.close()

	lineList[0] = re.sub('\n', '', lineList[0])        # Remove any newline which might be left

	tok = re.split(' *', lineList[0])

	idle = int(tok[4]) + int(tok[5])
	busy = int(tok[1]) + int(tok[2]) + int(tok[3]) + int(tok[6]) + int(tok[7]) + int(tok[8])

	if proc_stat_busy < 0 :
		print "Since last boot:  {} * 100 / {}".format( busy, idle+busy )
		print "{:6.3f}%".format( float(busy * 100) / float(idle + busy) )
		print "========"

	else :
		delta_busy = busy - proc_stat_busy 
		delta_idle = idle - proc_stat_idle
		timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
		pct_util = float(delta_busy * 100) / float(delta_idle + delta_busy)
		print "{} {:6.3f}%".format( timestamp, pct_util )
		if len(proc_stat_hist) > (proc_stat_hist_n -1) :
			proc_stat_hist = proc_stat_hist[1:]
		proc_stat_hist.append( pct_util )

	proc_stat_busy = busy
	proc_stat_idle = idle

	# --------------------------------------------------------------------------------
	#    cpu  1935650 0 1395066 620192925 17828 0 23111 0 0 0
	#
	#   user: normal processes executing in user mode
	#   nice: niced processes executing in user mode
	#   system: processes executing in kernel mode
	#   idle: twiddling thumbs
	#   iowait: waiting for I/O to complete
	#   irq: servicing interrupts
	#   softirq: servicing softirqs
	# Time units are in USER_HZ or Jiffies (typically hundredths of a second).
	#
	#
	#  https://stackoverflow.com/questions/23367857/accurate-calculation-of-cpu-usage-given-in-percentage-in-linux
	#
	#       1       2      3       4         5      6     7        8      9      10
	#       user    nice   system  idle      iowait irq   softirq  steal  guest  guest_nice
	#  cpu  74608   2520   24433   1117073   6176   4054  0        0      0      0
	#
	#  Algorithmically, we can calculate the CPU usage percentage like:
	#
	#  PrevIdle = previdle + previowait
	#  Idle = idle + iowait
	#  Idle = int(tok[4]) + int(tok[5])
	#
	#  PrevNonIdle = prevuser + prevnice + prevsystem + previrq + prevsoftirq + prevsteal
	#  NonIdle = user + nice + system + irq + softirq + steal
	#  NonIdle = int(tok[1]) + int(tok[2]) + int(tok[3]) + int(tok[6]) + int(tok[7]) + int(tok[8])
	#
	#  PrevTotal = PrevIdle + PrevNonIdle
	#  Total = Idle + NonIdle
	#
	#  # differentiate: actual value minus the previous one
	#  totald = Total - PrevTotal
	#  idled = Idle - PrevIdle
	#
	#  CPU_Percentage = (totald - idled)/totald
	# --------------------------------------------------------------------------------




# ----------------------------------------------------------------------------------------
#  This is really a little demonstrator loop
#
#
#
#  Thinking about tracking the last so-many calls (10 here) average to approximate
#  the 3 load numbers given by uptime.
# 
# ----------------------------------------------------------------------------------------
if __name__ == '__main__':
	try:
		for iii in range(1, 240):
			proc_stat()
			sleep( interval )
		print "\nLast (up to) " + str(proc_stat_hist_n) + " samples:"
		print proc_stat_hist

	except KeyboardInterrupt:
		print "\nLast (up to) " + str(proc_stat_hist_n) + " samples:"
		print proc_stat_hist

# @#@
# ----------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------
