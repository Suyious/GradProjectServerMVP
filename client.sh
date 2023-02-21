#!/bin/sh

if [[ "$#" -eq 0 ]]
then
	echo "Usage: client <endpoint> <method=GET>"
	exit 1
fi

data=""
editinput(){
	# tempf=$(mktemp /tmp/tmp.XXXXXXX.json)
	tempf="input.tmp.json"
	$EDITOR $tempf
	data=$(cat $tempf)
	# rm $tempf
}

conttype=""
body=""
response=""

methodparam=$(echo $2 | tr '[:lower:]' '[:upper:]')

case $methodparam in
	GET|POST|PUT|DELETE)
		method="-X$methodparam";;
	*) 
		method="";;
esac

case $methodparam in 
	POST|PUT) 
		editinput
		if [[ $data == "" ]]
		then
			echo "[ABORT] Request Cancelled"
			exit 1
		fi
		response=$(curl -svL -H 'Content-Type: application/json' -d "$data" $method http://127.0.0.1:8000/$1);;
	DELETE) 
		response=$(curl -svL $method http://127.0.0.1:8000/$1);;
	*)
	response=$(curl -svL http://127.0.0.1:8000/$1);;
esac

html=$(echo "$response" | w3m -dump -T text/html)
json=$(echo "$response" | jq 2> /dev/null)
exit_code="$?"

if [[ "$exit_code" -eq 0 ]]
then
	echo "$json"
else
	echo "$html"
fi
