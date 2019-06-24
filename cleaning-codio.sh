if [ $# != 2 ]; then
		echo "Usage: $0 <codio-roster> <output-name>"
		echo "You should also double check what the fields are for email,completed date"
		exit -1
fi

codio=$1
output=$2

cat $codio | cut -d, -f6,20 | sed -e 's/@.*,/,/' | sed -e 's/email/uni/' | sed -e 's/completed //' > $output
