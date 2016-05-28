export HADOOP_STREAM="/usr/local/Cellar/hadoop/2.7.2/libexec/share/hadoop/tools/lib/hadoop-streaming-2.7.2.jar"
#echo "this is a  test " | ./mapper.py
#echo "this is a a a  test test " | ./mapper.py | sort -k1,1 | ./reducer.py
hadoop fs -mkdir -p /user/$(whoami)/test2/input
hadoop fs -put testdata /user/$(whoami)/test2/input

hadoop jar $HADOOP_STREAM -files ./mapper.py,./reducer.py -mapper ./mapper.py -reducer ./reducer.py \
    -input /user/$(whoami)/test2/input/testdata \
    -output /user/$(whoami)/test2/output

hadoop fs -ls /user/yanyiwu/test2/output
hadoop fs -cat /user/yanyiwu/test2/output/part-00000
