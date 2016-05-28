#export HADOOP_CLASSPATH=${JAVA_HOME}/lib/tools.jar
hadoop com.sun.tools.javac.Main WordCount.java
jar cf wc.jar WordCount*.class
hadoop fs -mkdir /user/yanyiwu/test1
hadoop fs -mkdir /user/yanyiwu/test1/input
hadoop fs -put testdata /user/yanyiwu/test1/input
hadoop fs -cat /user/yanyiwu/test1/input/testdata

#hadoop fs -mkdir /user/yanyiwu/test1/output
hadoop jar wc.jar WordCount /user/yanyiwu/test1/input /user/yanyiwu/test1/output
hadoop fs -ls /user/yanyiwu/test1/output
hadoop fs -cat /user/yanyiwu/test1/output/part-r-00000
