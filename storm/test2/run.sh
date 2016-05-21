for f in `ls apache-storm-0.9.1-incubating/lib/`
do
    export CLASSPATH="apache-storm-0.9.1-incubating/lib/$f:$CLASSPATH"
done
export CLASSPATH="./src/:$CLASSPATH"
javac src/com/practice/spouts/*.java
javac src/com/practice/bolts/*.java
javac src/com/practice/HelloStorm.java
java com.practice.HelloStorm data.txt
