# coding: utf8
"""
Simple mongodb utilities

"""
import json

import pandas as teddy
import pymongo
from bson import Code

__author__ = 'clement'

REMOTE = 'mongodb://dockerapp.clementtrebuchet.cloudns.pw:27017/'


def import_content():
    """

    :return: load csv file to mongodb pragmatically
    """
    db_cm = mongodb_client()
    csv_data = teddy.read_csv(
        '/home/clement/Projects/Pyhton/BIGDATA/microblog/data/file/microblogDataset8_COMP6235_CW2.csv', sep=',', )
    data_json = csv_data.to_json()
    data_json = json.loads(data_json)
    # db_cm.remove()
    print data_json
    db_cm.insert(data_json)


def mongo_db():
    mng_client = pymongo.MongoClient('{}'.format(REMOTE))
    mng_db = mng_client['microblog']
    return mng_db


def mongodb_client():
    mng_client = pymongo.MongoClient('{}'.format(REMOTE))
    mng_db = mng_client['microblog']
    collection_name = 'microblog_entries'
    db_cm = mng_db[collection_name]
    return db_cm


def get_mongodb_data_frame():
    """

    :return:pandas dataframe from microblog (aka: The easy way)
    """
    input_data = mongodb_client()
    df = teddy.DataFrame(list(input_data.find()))
    return df


def get_hash_tag_avg():
    """

    :return:
    """
    total_microblog = mongo_db().microblog_entries.find().count()
    mapper = """
                function() {
                try {
                        var re = /#/g;
                        count = 0;
                        this.text.split(" ").forEach(function(word){
                            if(word && word.length ){
                               while (re.exec(word) !== null) {
                                        ++count;
                               }
                               emit('#',  ++count);
                            }
                        });
                    }
                    catch(err) {
                        print(err);
                    }
                }
                """
    reducer = """
            function(key, value) {
                var total = 0;
                value.forEach(function(v){
                    total += v;
                });
                    return total;
                }


            """
    results = mongo_db().microblog_entries.map_reduce(Code(mapper), Code(reducer), 'myres', full_response=False)
    for doc in results.find():
        avg = float(doc['value']) / float(total_microblog)
        print(u'Average number of hashtags({}) used within a message : {:.2f}'.format(doc['_id'], avg))
        print(u'Total hashtags({}) in collections : {}'.format(doc['_id'], int(doc['value'])))
        print(u'Total messages in collections : {}'.format(int(total_microblog)))


def get_ten_most_common_bi_gram():
    mapper = """
                function() {
                try {
                        this.text.split(" ").forEach(function(word){
                            if(word && word.length )
                                for (var i = 0; i < word.length; i++) {
                                       var tmp = word.charAt(i) + word.charAt(i+1);
                                       if(tmp.length < 2){
                                            continue;
                                       }
                                       else {
                                           emit(tmp, 1);
                                           i += 2;
                                       }
                                }

                        } );
                    }
                    catch(err) {
                        print(err)
                    }
                }
                """
    reducer = """
            function(key, value) {
                var total = 0;
                value.forEach(function(v){
                    total += v
                });
                    return total
                }


            """
    results = mongo_db().microblog_entries.map_reduce(Code(mapper), Code(reducer), 'myres', full_response=False,
                                                      limit=100)
    m_doc = {}
    for doc in results.find():
        # print doc
        try:
            count = m_doc[u'{}'.format('_id')]
            m_doc[u'{}'.format('_id')] = count + int(doc['value'])
        except KeyError as e:
            print e
            m_doc[u'{}'.format(doc['_id'])] = int(doc['value'])

    sorted_m_doc = sorted(m_doc.items(), key=lambda x: x[1], reverse=True)
    for m_tup in sorted_m_doc[:10]:
        print(u'bigram {} occurrences {}'.format(m_tup[0], m_tup[1]))


def get_ten_most_common_u_gram():
    total_microblog = mongo_db().microblog_entries.find().count()

    mapper = """
                function() {
                try {
                        this.text.split(" ").forEach(function(word){
                            if(word && word.length )
                                for (var i = 0; i < word.length; i++) {
                                       emit(word.charAt(i), 1);
                                }

                        } );
                    }
                    catch(err) {
                        print(err)
                    }
                }
                """
    reducer = """
            function(key, value) {
                var total = 0;
                value.forEach(function(v){
                    total += v
                });
                    return total
                }


            """
    results = mongo_db().microblog_entries.map_reduce(Code(mapper), Code(reducer), 'myres', full_response=False,
                                                      limit=2)
    m_doc = {}
    for doc in results.find():
        # print doc
        try:
            count = m_doc[u'{}'.format('_id')]
            m_doc[u'{}'.format('_id')] = count + int(doc['value'])
        except KeyError as e:
            print e
            m_doc[u'{}'.format(doc['_id'])] = int(doc['value'])

    sorted_m_doc = sorted(m_doc.items(), key=lambda x: x[1], reverse=True)
    for m_tup in sorted_m_doc[:10]:
        print(u'unigram {} occurrences {}'.format(m_tup[0], m_tup[1]))


def get_mean_length_messages():
    """

    :return:
    """

    """
    mean length of a message = ((sum every_word in field text) for each document) / total_entries
    get and work on (gonna reuse it for multiple purpose)
    Collection(Database(MongoClient(host=['dockerapp.clementtrebuchet.cloudns.pw:27017'], document_class=dict, tz_aware=False, connect=True), u'microblog'), u'myres')
    {u'_id': u'!', u'value': {u'count': 1.0}}
    {u'_id': u'#Audi', u'value': {u'count': 1.0}}
    {u'_id': u'#Automobile', u'value': {u'count': 1.0}}
    {u'_id': u'#Car', u'value': {u'count': 1.0}}
    {u'_id': u'#Cleeve', u'value': {u'count': 1.0}}
    {u'_id': u'#Fresh', u'value': {u'count': 1.0}}
    {u'_id': u'#KeepSafe', u'value': {u'count': 1.0}}
    {u'_id': u'#London', u'value': {u'count': 1.0}}
    {u'_id': u'#ModballRally', u'value': {u'count': 1.0}}
    """
    total_microblog = mongo_db().microblog_entries.find().count()

    mapper = """
                function() {
                try {
                        this.text.split(" ").forEach(function(word){
                            if(word && word.length )
                                emit(word, {'count':1});
                        } );
                    }
                    catch(err) {
                        print(err)
                    }
                }
                """
    reducer = """
            function(key, value) {
                var total = 0;
                for(var i = 0 ; i < value.length ; ++i ) {
                    total += value[i].count;
                }
                return {'count':total};
            }
            """
    results = mongo_db().microblog_entries.map_reduce(Code(mapper), Code(reducer), 'myres', full_response=False)
    # limit=100
    # print results
    m_doc = {}
    for doc in results.find():
        # print doc['_id'], doc['value']['count']
        try:
            m_count = int(m_doc[u'{}'.format(doc['_id'])])
            m_add = doc['value']['count']
            m_count += int(m_doc['{}'.format(m_add)])
        except KeyError as e:
            m_doc[u'{}'.format(doc['_id'])] = int(doc['value']['count'])

    total_document_words = 0
    for k, v in m_doc.items():
        total_document_words += v

    print total_document_words
    result = float(total_document_words) / float(total_microblog)
    print('Mean length of a message {:.2f} words'.format(result))


def geo_collection():
    mapper = """
                function() {
                try {
                      emit(this._id, {
                      type: 'Point',
                      coordinates: [parseFloat(this.geo_lng), parseFloat(this.geo_lat)]
                      });
                    }
                    catch(err) {
                        print(err)
                    }
                }
                """
    reducer = """
            function(key, value) {
                return value;
            }
            """
    results = mongo_db().microblog_entries.map_reduce(Code(mapper), Code(reducer), out='microblog.microgeo',
                                                      full_response=False)
    print results


def get_most_message_by_area():
    """
    say with out any other precisions that we have three area in England
    SCOTLAND:                                                                                       [[-5.009766,58.608334],
                                                                                                    [-5.668945, 55.329144],
                                                                                                    [-1.845703, 57.586559],
                                                                                                    [-5.009766,58.608334]]

    ENGLAND:                                                                                        [[-5.668945, 50.176898],
                                                                                                    [-1.230469, 54.597528],
                                                                                                    [2.988281, 51.563412],
                                                                                                    [-5.668945, 50.176898]]


    IRELAND:                                                                                        [[-7.734375, 56.047500],
                                                                                                    [-14.809570, 50.625073],
                                                                                                    [-3.823242, 53.435719],
                                                                                                    [-7.734375, 56.047500]]

    :return:
    """
    # SCOTLAND
    SCOTLAND = mongo_db().microblog.microgeo.find({'value': {'$geoWithin': {'$geometry': {'type': 'Polygon',
                                                                                          'coordinates':
                                                                                              [[[-5.009766, 58.608334],
                                                                                                [-5.668945, 55.329144],
                                                                                                [-1.845703, 57.586559],
                                                                                                [-5.009766,
                                                                                                 58.608334]]]}}}}).count()
    print('SCOTLAND area have above {} published messages'.format(SCOTLAND))

    # ENGLAND
    ENGLAND = mongo_db().microblog.microgeo.find({'value': {'$geoWithin': {'$geometry': {'type': 'Polygon',
                                                                                         'coordinates':
                                                                                             [[[-5.668945, 50.176898],
                                                                                               [-1.230469, 54.597528],
                                                                                               [2.988281, 51.563412],
                                                                                               [-5.668945,
                                                                                                50.176898]]]}}}}).count()
    print('ENGLAND area have above {} published messages'.format(ENGLAND))

    # IRELAND
    IRELAND = mongo_db().microblog.microgeo.find({'value': {'$geoWithin': {'$geometry': {'type': 'Polygon',
                                                                                         'coordinates':
                                                                                             [[[-7.734375, 56.047500],
                                                                                               [-14.809570, 50.625073],
                                                                                               [-3.823242, 53.435719],
                                                                                               [-7.734375,
                                                                                                56.047500]]]}}}}).count()
    print('IRELAND area have above {} published messages'.format(IRELAND))


if __name__ == '__main__':
    # df = get_mongodb_data_frame()
    # print df.text.count
    # get_mean_length_messages()
    # get_most_message_by_area()
    # get_ten_most_common_u_gram()
    # get_ten_most_common_bi_gram()
    get_hash_tag_avg()
