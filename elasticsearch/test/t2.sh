curl -XPUT 'http://localhost:9200/us/user/1?pretty=1' -d '
{
   "email" : "john@smith.com",
      "name" : "John Smith",
     "username" : "@john"
 }
 '

 curl -XPUT 'http://localhost:9200/gb/user/2?pretty=1' -d '
 {
    "email" : "mary@jones.com",
   "name" : "Mary Jones",
      "username" : "@mary"
  }
  '

  curl -XPUT 'http://localhost:9200/gb/tweet/3?pretty=1' -d '
  {
     "date" : "2014-09-13",
    "name" : "Mary Jones",
   "tweet" : "Elasticsearch means full text search has never been so easy",
      "user_id" : 2
  }
  '

  curl -XPUT 'http://localhost:9200/us/tweet/4?pretty=1' -d '
  {
     "date" : "2014-09-14",
    "name" : "John Smith",
   "tweet" : "@mary it is not just text, it does everything",
      "user_id" : 1
  }
  '

  curl -XPUT 'http://localhost:9200/gb/tweet/5?pretty=1' -d '
  {
     "date" : "2014-09-15",
    "name" : "Mary Jones",
   "tweet" : "However did I manage before Elasticsearch?",
      "user_id" : 2
  }
  '

  curl -XPUT 'http://localhost:9200/us/tweet/6?pretty=1' -d '
  {
     "date" : "2014-09-16",
    "name" : "John Smith",
   "tweet" : "The Elasticsearch API is really easy to use",
      "user_id" : 1
  }
  '

  curl -XPUT 'http://localhost:9200/gb/tweet/7?pretty=1' -d '
  {
     "date" : "2014-09-17",
    "name" : "Mary Jones",
   "tweet" : "The Query DSL is really powerful and flexible",
      "user_id" : 2
  }
  '

  curl -XPUT 'http://localhost:9200/us/tweet/8?pretty=1' -d '
  {
     "date" : "2014-09-18",
    "name" : "John Smith",
   "user_id" : 1
   }
   '

   curl -XPUT 'http://localhost:9200/gb/tweet/9?pretty=1' -d '
   {
      "date" : "2014-09-19",
     "name" : "Mary Jones",
    "tweet" : "Geo-location aggregations are really cool",
   "user_id" : 2
   }
   '

   curl -XPUT 'http://localhost:9200/us/tweet/10?pretty=1' -d '
   {
      "date" : "2014-09-20",
     "name" : "John Smith",
    "tweet" : "Elasticsearch surely is one of the hottest new NoSQL products",
   "user_id" : 1
   }
   '

   curl -XPUT 'http://localhost:9200/gb/tweet/11?pretty=1' -d '
   {
      "date" : "2014-09-21",
     "name" : "Mary Jones",
    "tweet" : "Elasticsearch is built for the cloud, easy to scale",
   "user_id" : 2
   }
   '

   curl -XPUT 'http://localhost:9200/us/tweet/12?pretty=1' -d '
   {
      "date" : "2014-09-22",
     "name" : "John Smith",
    "tweet" : "Elasticsearch and I have left the honeymoon stage, and I still love her.",
   "user_id" : 1
   }
   '

   curl -XPUT 'http://localhost:9200/gb/tweet/13?pretty=1' -d '
   {
      "date" : "2014-09-23",
     "name" : "Mary Jones",
    "tweet" : "So yes, I am an Elasticsearch fanboy",
   "user_id" : 2
   }
   '

   curl -XPUT 'http://localhost:9200/us/tweet/14?pretty=1' -d '
   {
      "date" : "2014-09-24",
     "name" : "John Smith",
    "tweet" : "How many more cheesy tweets do I have to write?",
   "user_id" : 1
   }
   '

