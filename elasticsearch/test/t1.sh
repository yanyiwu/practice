#curl 'http://localhost:9200/megacorp/employee/_search?pretty=true' -d '
#{
#    "query" : {
#        "filtered" : {
#            "filter" : {
#            "range" : {
#                "age":{"gt":30} }
#            },
#            "query" : {
#                "match" : {
#                    "last_name" : "smith"
#                } 
#            }
#        } 
#    }
#}
#'
#exit 1
curl 'http://localhost:9200/_count?pretty=true'
curl 'http://localhost:9200/_cluster/health?pretty=true'
#exit 1
#curl 'http://localhost:9200/megacorp/employee/1?pretty=true'
#curl 'http://localhost:9200/megacorp/employee/_search?q:first_name=yanyiwu&pretty=true'
#curl 'http://localhost:9200/megacorp/employee/_search?pretty=true' -d '
#{
#    "query" : {
#        "match_phrase" : {
#            "first_name" : "y z"
#        } 
#    }
#}
#'
curl 'http://localhost:9200/_analyze?pretty' -d '
Smith
'

#curl 'http://localhost:9200/megacorp/_mapping/employee?pretty=true'
curl 'http://localhost:9200/megacorp/_mapping/?pretty=true'

exit 1

curl 'http://localhost:9200/megacorp/employee/_search?pretty=true' -d '
{
    "aggs" : {
        "allinterests" : {
            "terms" : {"field": "interests"}
        } 
    }
}
'
#exit 1
curl -XPOST 'http://localhost:9200/megacorp/employee/?pretty=true' -d '
{
        "first_name" : "y x",
        "last_name" :  "Smith",
        "age" :        31,
        "about" :      "I love to go rock climbing 22",
        "interests": [ "sports", "music" ]
}
'
