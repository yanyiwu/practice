./cmd1.sh &
p1=$!
#echo $p1
./cmd2.sh &
p2=$!
#echo $p2

wait $p1
if [ "x$?" != "x0" ]; then
    echo "$p1 failed"
    exit 1
fi

wait $p2
if [ "x$?" != "x0" ]; then
    echo "$p2 failed"
    exit 1
fi

echo "ok!"

