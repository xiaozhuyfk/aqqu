"""
A module for extracting features from a query candidate.

Copyright 2015, University of Freiburg.

Elmar Haussmann <haussmann@cs.uni-freiburg.de>

"""

from query_candidate import QueryCandidate
from collections import defaultdict
import math
from wikiAPI import Wiki
from util import writeFile, readFile, kstem
import os
from collections import Counter
import string

N_GRAM_STOPWORDS = {'be', 'do', '?', 'the', 'of', 'is', 'are', 'in', 'was',
                    'did', 'does', 'a', 'for', 'have', 'there', 'on', 'has',
                    'to', 'by', 's', 'some', 'were', 'at', 'been', 'do',
                    'and', 'an', 'as'}

mid_bow = {}

rel_bow = {}

relation_set = set()

aws_raw_dir = "/data/raw/"
aws_dump_dir = "/data/dump/"
aws_query_dir = "/data/query/"
aws_bow_dir = "/data/bow/"
boston_dump_dir = "/home/hongyul/aqqu/testresult/dump/"
boston_query_dir = "/home/hongyul/aqqu/testresult/query/"
boston_bow_dir = "/home/hongyul/aqqu/testresult/bow"

print "Extracting Relation BOWs..."
rel_bowlong = {}
rel_bowshort = {}
bow_long_dir = "/research/backup/aqqu/testresult/bowlong/"
bow_short_dir = "/research/backup/aqqu/testresult/bowlongscore/"

'''
for line in readFile("/research/backup/aqqu/testresult/relations.log").split("\n"):
    if (line == ""):
        continue
    relation_set.add(line)
'''


#writeFile("/research/backup/aqqu/testresult/relation_fail.log", "", "w")
bowlong_total = {}
bowshort_total = {}

for filename in os.listdir(bow_long_dir):
    if (not filename.endswith(".log")):
        continue

    print "Processing relation file: " + filename
    rel = filename[:-4]

    counter = Counter()
    lines = readFile(bow_long_dir + filename).split("\n")
    total = 0
    for line in lines:
        if (line == ""):
            continue
        tokens = line.split(" ")
        term = " ".join(tokens[:-1])
        tf = float(tokens[-1])
        counter[term] = tf
        total += tf
    rel_bowlong[rel] = counter
    bowlong_total[rel] = total

for filename in os.listdir(bow_short_dir):
    if (not filename.endswith(".log")):
        continue

    print "Processing relation file: " + filename
    rel = filename[:-4]

    counter = Counter()
    lines = readFile(bow_short_dir + filename).split("\n")
    total = 0
    for line in lines:
        if (line == ""):
            continue
        tokens = line.split(" ")
        term = " ".join(tokens[:-1])
        tf = float(tokens[-1])
        counter[term] = tf
        total += tf
    rel_bowshort[rel] = counter
    bowshort_total[rel] = total




def get_n_grams(tokens, n=2):
    """Return n-grams for the given text tokens.

    n-grams are "_"-concatenated tokens.
    :param n:
    :return:
    """
    grams = zip(*[tokens[i:] for i in range(n)])
    return grams


def get_n_grams_features(candidate):
    """Get ngram features from the query of the candidate.

    :type candidate: QueryCandidate
    :param candidate:
    :return:
    """
    query_text_tokens = [x.lower() for x in get_query_text_tokens(candidate)]
    # First get bi-grams.
    n_grams = get_n_grams(query_text_tokens, n=2)
    # Then get uni-grams.
    n_grams.extend(get_n_grams(query_text_tokens, n=1))
    return n_grams


def get_query_text_tokens(candidate):
    """
    Return the query text for the candidate.
    :param candidate:
    :return:
    """
    # The set of all tokens for which an entity was identified.
    entity_tokens = set()
    for em in candidate.matched_entities:
        entity_tokens.update(em.entity.tokens)
    query_text_tokens = ['STRTS']
    # Replace entity tokens with "ENTITY"
    for t in candidate.query.query_tokens:
        if t in entity_tokens:
            # Don't replace if the previous token is an entity token
            if len(query_text_tokens) > 0 and query_text_tokens[-1] == 'ENTITY':
                continue
            else:
                query_text_tokens.append('ENTITY')
        else:
            query_text_tokens.append(t.lemma)
    return query_text_tokens


class FeatureExtractor(object):
    """Extracts features from a candidate.

    This is a class because this way it is easiest to have all logic
    in one place. Furthermore, it can carry some state, e.g. additional
    classifiers that compute scores etc.
    """

    def __init__(self,
                 generic_features,
                 n_gram_features,
                 relation_score_model=None,
                 entity_features=True):
        self.generic_features = generic_features
        self.n_gram_features = n_gram_features
        # If we use n-gram features this is set before to determine relevant
        # n-grams.
        self.ngram_dict = None
        # If this is provided each candidate is scored using this model
        # and the resulting score is added as an extracted feature.
        self.relation_score_model = relation_score_model
        self.entity_features = entity_features


    def extract_features(self, candidate):
        """Extract features from the query candidate.

        :type candidate: QueryCandidate
        :param candidate:
        :return:
        """
        # The number of literal entities.
        n_literal_entities = 0
        # The sum of surface_score * mention_length over all entity mentions.
        em_token_score = 0.0
        # A flag whether the candidate contains a mediator.
        is_mediator = 0.0
        # The number of relations that are matched literally at least once.
        n_literal_relations = 0
        # The number of tokens that are part of a literal entity match.
        literal_entities_length = 0
        # The number of tokens that match literal in a relation.
        n_literal_relation_tokens = 0
        # The number of tokens that match via weak synoynms in a relation.
        n_weak_relation_tokens = 0
        # The number of tokens that match via derivation in a relation.
        n_derivation_relation_tokens = 0
        # The number of tokens that match via relation context in a relation.
        n_context_relation_tokens = 0
        # The sum of all weak match scores.
        sum_weak_relation_tokens = 0
        # The sum of all weak match scores.
        sum_context_relation_tokens = 0
        # The size of the result.
        result_size = candidate.get_result_count()
        cardinality = 0
        # Each entity match represents a matched entity.
        n_entity_matches = len(candidate.matched_entities)
        em_surface_scores = []
        em_pop_scores = []
        n_entity_tokens = 0
        for em in candidate.matched_entities:
            # A threshold above which we consider the match a literal match.
            threshold = 0.8
            n_entity_tokens += len(em.entity.tokens)
            if em.entity.perfect_match or em.entity.surface_score > threshold:
                n_literal_entities += 1
                literal_entities_length += len(em.entity.tokens)
            em_surface_scores.append(em.entity.surface_score)
            em_score = em.entity.surface_score
            em_score *= len(em.entity.tokens)
            em_token_score += em_score
            if em.entity.score > 0:
                em_pop_scores.append(math.log(em.entity.score))
            else:
                em_pop_scores.append(-1)
        token_name_match_score = defaultdict(float)
        token_weak_match_score = defaultdict(float)
        token_word_match_score = defaultdict(float)
        token_derivation_match_score = defaultdict(float)
        for rm in candidate.matched_relations:
            if rm.name_match:
                for (t, _) in rm.name_match.token_names:
                    token_name_match_score[t] += 1.0
                n_literal_relations += 1
            if rm.words_match:
                for (t, s) in rm.words_match.token_scores:
                    token_word_match_score[t] += s
            if rm.name_weak_match:
                for (t, _, s) in rm.name_weak_match.token_name_scores:
                    token_weak_match_score[t] += s
            if rm.derivation_match:
                for (t, _) in rm.derivation_match.token_names:
                    token_derivation_match_score[t] += 1.0
            # cardinality is only set for the answer relation.
            if rm.cardinality > 0:
                # Number of facts in the relation (like in FreebaseEasy).
                cardinality = rm.cardinality[0]

        n_literal_relation_tokens = len(token_name_match_score)
        n_derivation_relation_tokens = len(token_derivation_match_score)
        n_context_relation_tokens = len(token_word_match_score)
        n_weak_relation_tokens = len(token_weak_match_score)
        sum_weak_relation_tokens = sum(token_weak_match_score.values())
        sum_context_relation_tokens = sum(token_word_match_score.values())
        avg_em_surface_score = sum(em_surface_scores) / len(em_surface_scores)
        sum_em_surface_score = sum(em_surface_scores)
        avg_em_popularity = sum(em_pop_scores) / len(em_pop_scores)
        sum_em_popularity = sum(em_pop_scores)
        cardinality = int(math.log(cardinality)) if cardinality > 0 \
            else cardinality

        # Each of these maps from a token to a relation matching score.
        # We are interested in the set of all tokens.
        token_matches = [token_derivation_match_score,
                         token_weak_match_score,
                         token_name_match_score,
                         token_word_match_score]
        n_rel_tokens = len(set.union(*[set(x.keys()) for x in token_matches]))
        # If we ignore entity features we need to compute coverage differently
        if not self.entity_features:
            coverage = (n_rel_tokens /
                        float(len(candidate.query.query_tokens)))
        else:
            coverage = ((n_rel_tokens + n_entity_tokens) /
                        float(len(candidate.query.query_tokens)))
        features = {}
        result_size_0 = 1 if result_size == 0 else 0
        result_size_1_to_20 = 1 if 1 <= result_size <= 20 else 0
        result_size_gt_20 = 1 if result_size >= 20 else 0
        matches_answer_type = 1 if candidate.matches_answer_type else 0
        if self.generic_features:
            if self.entity_features:
                features.update({
                    'n_literal_entities': n_literal_entities,
                    'n_entity_matches': n_entity_matches,
                    'literal_entities_length': literal_entities_length,
                    'avg_em_surface_score': avg_em_surface_score,
                    'sum_em_surface_score': sum_em_surface_score,
                    'avg_em_popularity': avg_em_popularity,
                    'sum_em_popularity': sum_em_popularity,
                    'total_literal_length': (literal_entities_length
                                             + n_literal_relations),
                })
            features.update({
                # "Relation Features"
                'n_relations': len(candidate.get_relation_names()),
                'n_literal_relations': n_literal_relations,
                'n_literal_relation_tokens': n_literal_relation_tokens,
                'n_derivation_relation_tokens': n_derivation_relation_tokens,
                'n_context_relation_tokens': n_context_relation_tokens,
                'n_weak_relation_tokens': n_weak_relation_tokens,
                'sum_weak_relation_tokens': sum_weak_relation_tokens,
                'sum_context_relation_tokens': sum_context_relation_tokens,
                'cardinality': cardinality,
                # Changed this
                # 'is_mediator': is_mediator,
                # 'em_token_score': em_token_score,
                # "General Features
                'coverage': coverage,
                'matches_answer_type': matches_answer_type,
                'result_size_0': result_size_0,
                'result_size_1_to_20': result_size_1_to_20,
                'result_size_gt_20': result_size_gt_20,
            })
        if self.n_gram_features:
            features.update(self.extract_ngram_features(candidate))
        if self.relation_score_model:
            pass
            #rank_score = self.relation_score_model.score(candidate)
            #features['relation_score'] = rank_score.score



        # extract relation wiki bow score
        # self.extract_relations(candidate)

        #features["relation_bow"] = extract_wiki_rel_feature(candidate)
        #features["relation_wiki"] = self.extract_wiki_rel_feature(candidate)

        kl, kl_exclude, kl_short, kl_exclude_short = self.extract_kl_rel_feature(candidate)
        features["relation_kl"] = kl
        features["relation_kl_exclude_entity"] = kl_exclude
        features["relation_kl_short"] = kl_short
        features["relation_kl_exclude_entity_short"] = kl_exclude_short

        return features

    def extract_relations(self, candidate):
        backend = candidate.sparql_backend

        for relation in candidate.relations:
            relation_name = relation.name
            rel = relation_name.replace(".", "_")
            if (relation_name not in relation_set):
                print "Processing relation: ", relation_name

                relation_set.add(relation_name)
                content = relation_name + "\n"
                writeFile("/research/backup/aqqu/testresult/relations.log", content, "a")

                """
                edge = "http://rdf.freebase.com/ns/" + relation_name
                aws_raw_file = aws_raw_dir + rel + ".log"
                aws_dump_file = aws_dump_dir + rel + ".log"

                PAIR_QUERY_FORMAT = '''
                SELECT ?e1 ?e2 where {
                    ?e1 <%s> ?e2.
                }
                '''

                ENTITY_NAME_FORMAT = '''
                PREFIX fb: <http://rdf.freebase.com/ns/>
                SELECT DISTINCT ?0 where {
                    fb:%s fb:type.object.name ?0 .
                }
                '''

                QUERY_FORMAT = "#uw20(#1(%s) #1(%s))"

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
                """


    def extract_kl_rel_feature(self, candidate):
        relation = candidate.relations[-1]
        relation_name = relation.name
        tokens = [x for x in candidate.query_stems if x not in string.punctuation]
        tokens_exclude = tokens[:candidate.root_node.entity.start] + tokens[candidate.root_node.entity.end:]

        rel = relation_name.replace(".", "_")
        if (rel in rel_bowlong):
            bowlong = rel_bowlong[rel]
            bowshort = rel_bowshort[rel]
        else:
            writeFile("/research/backup/aqqu/testresult/relation_fail.log", "%s\n" % relation_name, "a")
            return (0.0, 0.0, 0.0, 0.0)

        kl = 0.0
        total = bowlong_total[rel]
        q_inv = 1.0 / len(tokens)
        if (total <= 0.0):
            return (0.0, 0.0, 0.0, 0.0)

        for token in tokens:
            if (token in bowlong):
                p = (bowlong[token] + 1.0) / (total + 1.0)
            else:
                p = 1.0 / (total + 1.0)
            kl -= q_inv * math.log(q_inv / p)

        kl_exclude = 0.0
        q_inv = 1.0 / len(tokens_exclude)
        for token in tokens_exclude:
            if (token in bowlong):
                p = (bowlong[token] + 1.0) / (total + 1.0)
            else:
                p = 1.0 / (total + 1.0)
            kl_exclude -= q_inv * math.log(q_inv / p)

        kl = math.pow(math.e, kl)
        kl_exclude = math.pow(math.e, kl_exclude)



        kl_short = 0.0
        total = bowshort_total[rel]
        q_inv = 1.0 / len(tokens)
        if (total <= 0.0):
            return (0.0, 0.0, 0.0, 0.0)

        for token in tokens:
            if (token in bowshort):
                p = (bowshort[token] + 1.0) / (total + 1.0)
            else:
                p = 1.0 / (total + 1.0)
            kl_short -= q_inv * math.log(q_inv / p)

        kl_exclude_short = 0.0
        q_inv = 1.0 / len(tokens_exclude)
        for token in tokens_exclude:
            if (token in bowlong):
                p = (bowshort[token] + 1.0) / (total + 1.0)
            else:
                p = 1.0 / (total + 1.0)
            kl_exclude_short -= q_inv * math.log(q_inv / p)

        kl_short = math.pow(math.e, kl_short)
        kl_exclude_short = math.pow(math.e, kl_exclude_short)

        return (kl, kl_exclude, kl_short, kl_exclude_short)


    def extract_wiki_rel_feature(self, candidate):
        # extract relation wiki bow score
        wiki = Wiki()
        results = candidate.get_result()
        score = 1.0
        bow = Counter()
        rels = set()

        for result in results[:5]:
            if result[0].startswith("m."):
                r_mid = result[0]
                r_mid = "/" + r_mid.replace(".", "/")

                if (r_mid in mid_bow):
                    bow += mid_bow[r_mid]
                else:
                    new, total = wiki.bag_of_words(r_mid)
                    if (new == None):
                        continue
                    mid_bow[r_mid] = new
                    bow += new
            else:
                rels.add(result[0])

        source = candidate.root_node
        mid = source.entity.entity.id
        mid = "/" + mid.replace(".", "/")

        if (mid in mid_bow):
            bow += mid_bow[mid]
        else:
            new, total = wiki.bag_of_words(mid)
            if (new == None):
                #print "Root mid %s has no bow." % mid
                return 0.0

            mid_bow[mid] = new
            bow += new

        for relation in candidate.relations:
            for token in relation.name.split("."):
                rels.add(token)

        size = len(rels)
        for token in rels:
            p = (bow[token] + 1.0) / (sum(bow.values()) + 1.0)
            score *= math.pow(p, 1.0 / size)

        '''
        relation = candidate.relations[-1]
        relation_tokens = relation.name.split(".")
        source = relation.source_node
        mid = source.entity.entity.id

        results = candidate.get_result()
        for result in results:
            if len(result) == 2:
                r_mid = result[0]
            else:
                pass

        if (mid in mid_bow):
            (bow, total) = mid_bow[mid]
        else:
            (bow, total) = wiki.bag_of_words(mid)
            mid_bow[mid] = (bow, total)

        # compute relation score
        if (bow and total):
            score = 0.0
            for token in relation_tokens:
                if (token in bow):
                    score += (bow[token] + 1.0) / (total + 1.0)
                else:
                    score += 1.0 / (total + 1.0)

            return score
        else:
            return 0
        '''
        return score

    def extract_ngram_features(self, candidate):
        """Extract ngram features from the single candidate.

        :param candidate:
        :return:
        """
        ngram_features = dict()
        relations = '_'.join(sorted(candidate.get_relation_names()))
        n_grams = get_n_grams_features(candidate)
        for ng in n_grams:
            # Ignore ngrams that only consist of stopfwords.
            if set(ng).issubset(N_GRAM_STOPWORDS):
                continue
            f_name = 'rel:%s+word:%s' % (relations, '_'.join(ng))
            if self.ngram_dict is None or f_name in self.ngram_dict:
                ngram_features[f_name] = 1
        return ngram_features
