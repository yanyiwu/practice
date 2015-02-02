while read file
do
    v=`curl -s "$file"`
    if [ "$v" != "1234" ]; then
        echo $v
        echo "failed."
        exit 1
    fi
done
echo "ok."
