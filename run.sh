#!/bin/bash
# David Joffe

counter=0

while IFS= read -r line
do
  ((counter++))
  echo CALL python3 $counter djgenerate.py \"$line\"
  date>>_log.txt
  echo CALL generate $counter \"$line\" >>_log.txt
  python3 djgenerate.py "$line"
done < input.txt
