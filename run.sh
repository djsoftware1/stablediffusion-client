#!/bin/bash
while IFS= read -r line
do
  echo CALL python3 djgenerate.py \"$line\"
  python3 djgenerate.py "$line"
done < input.txt
