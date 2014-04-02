#!/bin/bash 
declare -i i
declare -i seqcount
declare -i basecount
i=0
seqcount=0
basecount=0
while read line; do
	(( i++ ))
	if (($i == 4));
		then
			i=$((0))
	elif (($i == 1))
		then
  			((seqcount++))
  	elif (($i == 2))
		then
  			((basecount = basecount + ${#line}))
	fi
done < $1
echo $seqcount
echo $basecount
