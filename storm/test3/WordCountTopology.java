import backtype.storm.Config;
import backtype.storm.LocalCluster;
import backtype.storm.topology.TopologyBuilder;
import backtype.storm.tuple.Fields;

public class WordCountTopology {
    public static void main(String[] args) throws Exception {
        SentenceSpout spout = new SentenceSpout();
        SplitSentenceBolt splitBolt = new SplitSentenceBolt();
        WordCountBolt countBolt = new WordCountBolt();
        ReportBolt recordBolt = new ReportBolt();

        TopologyBuilder builder = new TopologyBuilder();
        builder.setSpout("sentence-spout", spout);
        builder.setBolt("split-bolt", splitBolt)
            .shuffleGrouping("sentence-spout");
        builder.setBolt("count-bolt", countBolt)
            .fieldsGrouping("split-bolt", new Fields("word"));
        builder.setBolt("record-bolt", recordBolt)
            .globalGrouping("count-bolt");

        Config config = new Config();
        LocalCluster cluster = new LocalCluster();
        cluster.submitTopology("word-count-topo", config, builder.createTopology());
        Thread.sleep(60*1000);
        cluster.killTopology("word-count-topo");
        cluster.shutdown();
    }
}
