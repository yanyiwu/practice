export STREAM="$HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-2.6.0.jar"
export HADOOP_CLASSPATH=$JAVA_HOME/lib/tools.jar

hdfs dfs -rm -r output input
hdfs dfs -put ./input

hadoop jar $STREAM  \
-files ./mapper.py,./reducer.py \
-mapper ./mapper.py \
-reducer ./reducer.py \
-input input \
-output output 

hdfs dfs -cat "output/*"
