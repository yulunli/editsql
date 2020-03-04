import pickle

f = open('data/sparc_data_removefrom/train.pkl', 'rb')
es = pickle.load(f)

of = open('ins', 'w')
for e in es:
    of.write('{} : {}\n'.format(e['database_id'], e['interaction_id']))
    for inter in e['interaction']:
        of.write('{}\n'.format(inter['utterance']))
    of.write('\n')

of.close()
