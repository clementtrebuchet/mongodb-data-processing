#This document describes the steps that have been needed to perform data mining test.

##Notice
    Accuracy most of the code can be improved, including the accuracy of some data (geospatial, ngram ...). 
    In fact I wanted to focus on the delivery of the test in a short time.
    Also I had mongodb infrastructure problems, especially cases that should not happen by connecting to the customer's infrastructure.

###Working on linux (fedora 22)
   - Input file was corrupted and i get errors when loading data/file/microblogDataset_COMP6235_CW2.csv
   - Trying loading it with mongoimport fail: exception:Invalid UTF8 character detected
   - Need to convert it with iconv :
   - <code>iconv -f ISO-8859-15 -t utf-8 microblogDataset_COMP6235_CW2.csv > microblogDataset8_COMP6235_CW2.csv</code>
    ####After that mongoimport was ok:
      <pre>
        mongoimport -d microblog -c microblog_entries --type csv --file microblogDataset8_COMP6235_CW2.csv --headerline
      </pre>
      <pre> ... </pre>
      <pre> Fri Dec  4 01:41:39.913 [FileAllocator] allocating new datafile data/db/microblog.6, filling with zeroes... </pre>
      <pre> Fri Dec  4 01:41:39.941 [FileAllocator] done allocating datafile data/db/microblog.6, size: 511MB,  took 0.027 secs</pre>
      <pre> Fri Dec  4 01:41:41.001 Progress: 199508479/211312117   94%</pre>
      <pre> Fri Dec  4 01:41:41.001 1378300 30628/second</pre>
      <pre> Fri Dec  4 01:41:43.429 check 9 1459862</pre>
      <pre> Fri Dec  4 01:41:43.429 imported 1459861 objects</pre>
###Mongo Engine Details
<pre>[clement@clemopower microblog]$ Fri Dec  4 22:10:11.987 
Fri Dec  4 22:10:11.987 warning: 32-bit servers don't have journaling enabled by default. Please use --journal if you want durability.
Fri Dec  4 22:10:11.987 
Fri Dec  4 22:10:12.000 [initandlisten] MongoDB starting : pid=24496 port=27017 dbpath=/home/clement/Projects/Pyhton/BIGDATA/microblog/data/db 32-bit host=clemopower.teamat4cs
Fri Dec  4 22:10:12.000 [initandlisten] 
Fri Dec  4 22:10:12.000 [initandlisten] ** NOTE: This is a 32 bit MongoDB binary.
Fri Dec  4 22:10:12.001 [initandlisten] **       32 bit builds are limited to less than 2GB of data (or less with --journal).
Fri Dec  4 22:10:12.001 [initandlisten] **       Note that journaling defaults to off for 32 bit and is currently off.
Fri Dec  4 22:10:12.001 [initandlisten] **       See http://dochub.mongodb.org/core/32bit
Fri Dec  4 22:10:12.001 [initandlisten] 
Fri Dec  4 22:10:12.001 [initandlisten] db version v2.4.14
Fri Dec  4 22:10:12.001 [initandlisten] git version: 05bebf9ab15511a71bfbded684bb226014c0a553
Fri Dec  4 22:10:12.001 [initandlisten] build info: Linux ip-10-144-100-100 2.6.21.7-2.fc8xen #1 SMP Fri Feb 15 12:39:36 EST 2008 i686 BOOST_LIB_VERSION=1_49
Fri Dec  4 22:10:12.001 [initandlisten] allocator: system
Fri Dec  4 22:10:12.001 [initandlisten] options: { dbpath: "/home/clement/Projects/Pyhton/BIGDATA/microblog/data/db" }
Fri Dec  4 22:10:12.483 [initandlisten] waiting for connections on port 27017
Fri Dec  4 22:10:12.483 [websvr] admin web console waiting for connections on port 28017
Fri Dec  4 22:10:17.634 [initandlisten] connection accepted from 127.0.0.1:54985 #1 (1 connection now open)
Fri Dec  4 22:10:17.820 [initandlisten] connection accepted from 127.0.0.1:54987 #2 (2 connections now open)
Fri Dec  4 22:10:17.820 [initandlisten] connection accepted from 127.0.0.1:54986 #3 (3 connections now open)
Fri Dec  4 22:10:21.736 [initandlisten] connection accepted from 127.0.0.1:54989 #4 (4 connections now open)
</pre>

###Migrating data to my docker cloud infrastructure as my old laptop didn't get the trick
####Cannot allocate memory during map reduce on question 5 :(
#####can't map file memory - mongo requires 64 bit build for larger datasets
<pre>
Fri Dec  4 23:41:42.271 [conn35] ERROR:   mmap() failed for /home/clement/Projects/Pyhton/BIGDATA/microblog/data/db/microblog.6 len:536608768 errno:12 Cannot allocate memory
Fri Dec  4 23:41:42.271 [conn35] ERROR: mmap failed with out of memory. You are using a 32-bit build and probably need to upgrade to 64
Fri Dec  4 23:41:42.356 [conn35] warning: ClientCursor::YieldLock not closed properly
Fri Dec  4 23:41:42.417 [conn35] CMD: drop microblog.tmp.mr.microblog_entries_4
Fri Dec  4 23:41:43.013 [conn35] command microblog.$cmd command: { drop: "tmp.mr.microblog_entries_4" } ntoreturn:1 keyUpdates:0 locks(micros) w:619073 reslen:143 619ms
Fri Dec  4 23:41:43.047 [conn35] CMD: drop microblog.tmp.mr.microblog_entries_4_inc
Fri Dec  4 23:41:43.102 [conn35] mr failed, removing collection :: caused by :: 10084 can't map file memory - mongo requires 64 bit build for larger datasets
Fri Dec  4 23:41:43.128 [conn35] CMD: drop microblog.tmp.mr.microblog_entries_4
Fri Dec  4 23:41:43.128 [conn35] CMD: drop microblog.tmp.mr.microblog_entries_4_inc
Fri Dec  4 23:41:43.245 [conn35] command microblog.$cmd command: { mapreduce: "microblog_entries", map: 
</pre>
####Private Cloud infrastructure ( Atomic Fedora 21 cluster ): 
    - Mongodb engine location dockerapp.clementtrebuchet.cloudns.pw:27017
        - Name:   dockerapp.clementtrebuchet.cloudns.pw
        - Address: 195.154.52.167
    - Just deploy 'as is' from docker official image, no secure except a sandboxed shared volume
    - Will be destroy as soon as the test finish
    - MapReduce seems to run fine :)
<pre>
     db.currentOp()
{
        "inprog" : [
                {
                        "desc" : "conn25",
                        "threadId" : "0x352dba0",
                        "connectionId" : 25,
                        "opid" : 1460057,
                        "active" : true,
                        "secs_running" : 892,
                        "microsecs_running" : NumberLong(892229299),
                        "op" : "query",
                        "ns" : "microblog.tmp.mr.microblog_entries_0_inc",
                        "query" : {
                                "mapreduce" : "microblog_entries",
                                "map" : function () {
                        try {
                    this.text.split(" ").forEach(function(word){
                        if(word && word.length )
                            emit(word, {'count':1});
                    } );
                                }
                                catch(err) {
                                    print(err)
                                }
                        },
                                "reduce" : function (key, value) {
                        var total = 0;
                        for(var i = 0 ; i < value.length ; ++i ) {
                                total += value[i].count;
                        }
                        return {'count':total};
                },
                                "out" : "myres"
                        },
                        "client" : "78.240.230.142:34409",
                        "msg" : "m/r: (1/3) emit phase M/R: (1/3) Emit Progress: 825199/1459861 56%",
                        "progress" : {
                                "done" : 825199,
                                "total" : 1459861
                        },
                        "numYields" : 14470,
                        "locks" : {
                                "Global" : "w",
                                "MMAPV1Journal" : "w"
                        },
                        "waitingForLock" : true,
                        "lockStats" : {
                                "Global" : {
                                        "acquireCount" : {
                                                "r" : NumberLong(3791551),
                                                "w" : NumberLong(3746099)
                                        }
                                },
                                "MMAPV1Journal" : {
                                        "acquireCount" : {
                                                "r" : NumberLong(22726),
                                                "w" : NumberLong(7492229)
                                        },
                                        "acquireWaitCount" : {
                                                "r" : NumberLong(99),
                                                "w" : NumberLong(3607)
                                        },
                                        "timeAcquiringMicros" : {
                                                "r" : NumberLong(553227),
                                                "w" : NumberLong(94748084)
                                        }
                                },
                                "Database" : {
                                        "acquireCount" : {
                                                "r" : NumberLong(3),
                                                "w" : NumberLong(3746096),
                                                "R" : NumberLong(22723),
                                                "W" : NumberLong(5)
                                        }
                                },
                                "Collection" : {
                                        "acquireCount" : {
                                                "R" : NumberLong(3),
                                                "W" : NumberLong(3746099)
                                        },
                                        "acquireWaitCount" : {
                                                "W" : NumberLong(34)
                                        },
                                        "timeAcquiringMicros" : {
                                                "W" : NumberLong(8300)
                                        }
                                },
                                "Metadata" : {
                                        "acquireCount" : {
                                                "W" : NumberLong(26)
                                        }
                                }
                        }
                }
        ]
}
</pre>
     