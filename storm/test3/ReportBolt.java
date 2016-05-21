import java.util.HashMap;
import java.util.Map;
import java.util.List;
import java.util.ArrayList;
import java.util.Collections;

import backtype.storm.topology.base.BaseRichBolt;
import backtype.storm.task.OutputCollector;
import backtype.storm.task.TopologyContext;
import backtype.storm.topology.OutputFieldsDeclarer;
import backtype.storm.tuple.Tuple;

public class ReportBolt extends BaseRichBolt {
    private HashMap<String, Long> counts = null;
    public void prepare(Map config, TopologyContext context, OutputCollector collector) {
        this.counts = new HashMap<String, Long>();
    }
    public void execute(Tuple tuple) {
        String word = tuple.getStringByField("word");
        Long count = tuple.getLongByField("count");
        System.out.println("report execute " + word + count);
        this.counts.put(word, count);
    }
    public void declareOutputFields(OutputFieldsDeclarer declarer) {
        // do nothing
    }
    public void cleanup() {
        System.out.println("cleanup...");
        List<String> keys = new ArrayList<String>();
        keys.addAll(this.counts.keySet());
        Collections.sort(keys);
        for (String key: keys) {
            System.out.println(key + ":" + this.counts.get(key));
        }
        System.out.println("finished");
    }
}
