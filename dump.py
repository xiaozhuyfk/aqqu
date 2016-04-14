
import logging
import globals
from query_translator.util import writeFile, readFile
from query_translator.FreebaseDumpParser import FreebaseDumpParserC
from query_translator.FreebaseDumpReader import FreebaseDumpReaderC
from query_translator.util import sftp_get, sftp_put, sftp_execute
import thread



aws_raw_dir = "/data/raw/"
aws_dump_dir = "/data/dumpaqqu/"
aws_query_dir = "/data/query/"
aws_bow_dir = "/data/bow/"
boston_dump_dir = "/home/hongyul/aqqu/testresult/dump/"
boston_query_dir = "/home/hongyul/aqqu/testresult/query/"
boston_bow_dir = "/home/hongyul/aqqu/testresult/bow"


PAIR_QUERY_FORMAT = '''
        SELECT ?e1 ?e2 where {
            ?e1 %s ?e2.
            FILTER (lang(?e1) = "en")
        } LIMIT 2000
    '''

ENTITY_NAME_FORMAT = '''
PREFIX fb: <http://rdf.freebase.com/ns/>
SELECT DISTINCT ?0 where {
    fb:%s fb:type.object.name ?0 .
}
'''

RELATION_QUERY_FORMAT = '''
SELECT ?r where {
    ?e1 ?r ?e2.
} LIMIT 20000
'''

QUERY_FORMAT = "#uw20(#1(%s) #1(%s))"


def process_relations(backend, relations, size, index):
    num = len(relations) / size
    if (num == 0):
        num = 1

    if (index == size-1):
        rels = relations[index*num:]
    else:
        rels = relations[index*num:(index+1)*num]

    for relation_name in rels:
        if relation_name == "":
            continue

        rel = relation_name.replace(".", "_")
        edge = "http://rdf.freebase.com/ns/" + relation_name
        aws_raw_file = aws_raw_dir + rel + ".log"
        aws_dump_file = aws_dump_dir + rel + ".log"

        # construct search engine queries
        writeFile(aws_raw_file, "", "w")
        writeFile(aws_dump_file, "", "w")

        result = backend.query_json(PAIR_QUERY_FORMAT % edge)
        if (result == None):
            writeFile("/research/backup/aqqu/testresult/relation_fail.log", relation_name + "\n", "a")
            continue

        for pair in result:
            e1 = pair[0]
            e2 = pair[1]

            if (not e1.startswith("m.")):
                continue

            e1_result = backend.query_json(ENTITY_NAME_FORMAT % e1)
            if (e1_result == [] or e1_result == None):
                continue
            e1_name = e1_result[0][0].encode("utf-8", 'ignore')
            e1_paren = e1_name.find("(")
            if (e1_paren != -1):
                e1_name = e1_name[:e1_paren]

            if (e2.startswith("m.")):
                e2_result = backend.query_json(ENTITY_NAME_FORMAT % e2)
                if (e2_result == [] or e2_result == None):
                    continue
                e2_name = e2_result[0][0].encode("utf-8", 'ignore')
                e2_paren = e2_name.find("(")
                if (e2_paren != -1):
                    e2_name = e2_name[:e2_paren]
            else:
                e2_name = e2.encode('utf-8', 'ignore')

            pair = e1 + "\t" + e2 + "\n"
            query = QUERY_FORMAT % (e1_name, e2_name) + "\n"

            try:
                writeFile(aws_raw_file, pair, "a")
                writeFile(aws_dump_file, query, "a")
            except:
                continue


def process(backend, reader, Parser):
    print "Processing dump file..."

    # process all triples and extract relation pairs and queries
    relations = set()
    filenames = set()
    for cnt,lvCol in enumerate(reader):
        if 0 == (cnt % 1000):
            print 'read [%d] obj' %(cnt)

        for vCol in lvCol:
            e1 = vCol[0]
            e1 = Parser.DiscardPrefix(e1).decode('utf-8', 'ignore')
            edge = vCol[1].decode('utf-8')
            e2 = Parser.DiscardPrefix(vCol[2]).decode('utf-8', 'ignore')
            if e1.startswith("m.") and edge.startswith("<http://rdf.freebase.com"):
                at_index = e2.find("@")
                url_index = e2.find("^")

                if (at_index != -1 and url_index != -1):
                    e2 = e2[:min(at_index, url_index)]
                elif (at_index != -1):
                    e2 = e2[:at_index]
                elif (url_index != -1):
                    e2 = e2[:url_index]

                e1_result = backend.query_json(ENTITY_NAME_FORMAT % e1)
                if (e1_result == []):
                    continue
                e1_name = e1_result[0][0].encode("utf-8", 'ignore')
                e1_paren = e1_name.find("(")
                if (e1_paren != -1):
                        e1_name = e1_name[:e1_paren]

                if (e2.startswith("m.")):
                    e2_result = backend.query_json(ENTITY_NAME_FORMAT % e2)
                    if (e2_result == []):
                        continue
                    e2_name = e2_result[0][0].encode("utf-8", 'ignore')
                    e2_paren = e2_name.find("(")
                    if (e2_paren != -1):
                        e2_name = e2_name[:e2_paren]
                else:
                    e2_name = e2.encode('utf-8', 'ignore')


                relation_name = Parser.DiscardPrefix(edge)
                rel = relation_name.replace(".", "_")

                aws_raw_file = aws_raw_dir + rel + ".log"
                aws_dump_file = aws_dump_dir + rel + ".log"

                '''
                if (edge not in relations):
                    writeFile(aws_raw_file, "", "w")
                    writeFile(aws_dump_file, "", "w")
                    relations.add(edge)
                    filenames.add(rel)
                '''

                pair = e1 + "\t" + e2 + "\n"
                query = QUERY_FORMAT % (e1_name, e2_name) + "\n"

                try:
                    writeFile(aws_raw_file, pair, "a")
                    writeFile(aws_dump_file, query, "a")
                except:
                    continue

    print "Done processing dump file."
    #return (relations, filenames)

def run_indri(filenames):
    print "Start fetching BOW with indri."

    for rel in filenames:
        aws_dump_file = aws_dump_dir + rel + ".log"
        boston_dump_file = boston_dump_dir + rel + ".log"
        sftp_put(aws_dump_file, boston_dump_file)
        sftp_execute("../init_env/python indri.py " + rel)



def main():
    import argparse
    parser = argparse.ArgumentParser(description = "Console based translation.")
    parser.add_argument("ranker_name",
                        default = "WQ_Ranker",
                        help = "The ranker to use.")
    parser.add_argument("--config",
                        default = "config.cfg",
                        help = "The configuration file to use.")
    args = parser.parse_args()
    globals.read_configuration(args.config)
    config_params = globals.config
    backend = globals.get_sparql_backend(config_params)


    file = "/data/freebase-rdf-latest.gz"
    reader = FreebaseDumpReaderC()
    reader.open(file)
    Parser = FreebaseDumpParserC()

    #relations, filenames = process(backend, reader, Parser)


    content = readFile("/research/backup/aqqu/testresult/relations.log")
    relations = content.split("\n")
    for i in xrange(8):
        thread.start_new_thread(process_relations, (backend, relations, 8, i))





if __name__ == "__main__":
    main()