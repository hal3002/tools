#!/bin/bash

if [ ! $1 ]; then
	echo "Usage: $0 <pid>"
	exit
fi

if [ ! -f "/proc/$1/maps" ]; then
	echo "Unable to read memory maps"
	exit
fi

if [ ! -f "/proc/$1/mem" ]; then
	echo "Unable to read memory"
	exit
fi

for line in $( cat /proc/$1/maps | cut -f 1 -d " " ); do
	mem_start=$(( 0x$( echo $line | cut -f 1 -d '-' ) ))
	mem_end=$(( 0x$( echo $line | cut -f 2 -d '-' ) ))
	mem_size=$( expr $mem_end - $mem_start )
	dd status=none if=/proc/$1/mem skip=$mem_start count=$mem_size bs=1
done
