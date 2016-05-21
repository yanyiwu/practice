for f in `ls apache-storm-0.9.1-incubating/lib/`
do
    export CLASSPATH="apache-storm-0.9.1-incubating/lib/$f:$CLASSPATH"
done
#export CLASSPATH="$CLASSPATH"
javac *.java
java WordCountTopology data.txt
