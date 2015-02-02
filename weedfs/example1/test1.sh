for ((i=0; i < 1000; i++))
do
    curl -s -F "file=1234" "http://localhost:9334/submit" | awk -F'"' '{print $12}'
done
