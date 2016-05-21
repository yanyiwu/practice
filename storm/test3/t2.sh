for f in `ls apache-storm-0.9.1-incubating/lib/`
do
    jar tf apache-storm-0.9.1-incubating/lib/$f | grep BaseRichBolt
done
