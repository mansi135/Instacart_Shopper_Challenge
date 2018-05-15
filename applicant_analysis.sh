#!/bin/bash -e
# Assumes that this is run in the same folder as the applicants.sqlite3
if [[ $# -ne 2 ]]; then
    echo "Illegal arguments, please specify to and from dates only"
    exit 1
fi
file=applicants.sqlite3
if [[ ! -f $file ]]; then
    echo "Can't find the file $file in the current directory"
    exit 1
fi
from="$1"
to="$2"
query="select count(1) as count, week, workflow_state from (select strftime('%Y-%m-%d', created_at, 'weekday 1', case when strftime('%w', created_at) = '1' then '0 days' else '-7 days' end) week, workflow_state from applicants where date(created_at) between '$from' and '$to') subquery group by week, workflow_state;"
echo $query | sqlite3 -csv $file
