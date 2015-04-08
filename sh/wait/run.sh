./cmd1.sh &
p1=$!
pids[1]=$p1
#echo ${pids[1]}

./cmd2.sh &
p2=$!
pids[2]=$p2
#echo ${pids[2]}

for i in `seq ${#pids[*]}`
do
    wait ${pids[$i]}
    if [ "x$?" != "x0" ]
    then
        echo "${pids[$i]} failed."
        exit 1
    fi
done

echo "ok!"

#wait $p1
#if [ "x$?" != "x0" ]; then
#    echo "$p1 failed"
#    exit 1
#fi
#
#wait $p2
#if [ "x$?" != "x0" ]; then
#    echo "$p2 failed"
#    exit 1
#fi
#
#echo "ok!"
#
