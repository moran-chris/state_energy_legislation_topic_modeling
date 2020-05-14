from sklearn.feature_extraction.stop_words import ENGLISH_STOP_WORDS


def get_stop_words(new_stop_words=None):
    # Retrieve stop words and append any additional stop words
    stop_words = list(ENGLISH_STOP_WORDS)
    if new_stop_words:
        stop_words.extend(new_stop_words)
    return set(stop_words)

states = ['alabama','alaska','arizona','arkansas','california','colorado',
            'connecticut','delaware','florida','georgia','hawaii','idaho','illinois',
            'indiana','iowa','kansas','kentucky','louisiana','maine','maryland',
            'massachusetts','michigan','minnesota','mississippi','missouri',
            'montana','nebraska','nevada','hampshire','jersey',
            'mexico','york','carolina','dakota','ohio',
            'oklahoma','oregon','pennsylvania','rhode','carolina',
            'dakota','tennessee','texas','utah','vermont',
            'virginia','washington','virginia','wisconsin','wyoming']

new_stop_words = states + ['section', 'shall', 'state','law','including','chapter','cost',
                    'service','pursuant','act','provided','amended','public','plan',
                    'board','project','department','year','purpose','person','authority',
                    'agency','subdivision','program','commissioner','new','paragraph',
                    'provision','commission','mean','county','use','subsection','following',
                    'required','effective','authorized','article','date','read','federal',
                    'provide','requirement','day','prior','include','general','minnesota',
                    'office','available','code','district','director','york','subject',
                    'statute','sec','approved','follows','hawaii','customer','change','ha',
                    'senate','local','legislature','member','standard','effect','enacted',
                    'order','unit','necessary','ii','thousand','defined','limited','committee'
                    'period','jersey','council','2020','january','account','title',
                    'division','annual','municipality','eligible','adding','california',
                    'resolved','revised','city','proposed','governor','action','et','10',
                    'july','accordance','secretary','le','2019','line','thereof','cent',
                    'establish','related','adopted','adaptation','imposed','applicable',
                    'adopt','30','issued','determined','make','vermont','said',
                    'reccomendation','appointed','notwithstanding','regional','unless',
                    'ensure','virginia']
custom_lematize_dict = {'electrical': 'electric','electricity': 'electric'}
custom_stop_words = get_stop_words(new_stop_words)

cluster_one_words = ['111d','pl2007','111d','al','c340','c262c45','rcw']
cluster_two_words = ['c23','pl1999','c48349','ey','c48349']
cluster_four_words = ['tax','credit','taxpayer','revenue','2355','taxable']
cluster_five_words = ['energy',]
cluster_three_words = ['vehicle']
cluster_six_words = ['committee','task','house','representative']
