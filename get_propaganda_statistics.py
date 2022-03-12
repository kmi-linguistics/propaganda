import re
import os
import csv
import json
from indicnlp.tokenize import sentence_tokenize
from indicnlp.tokenize import indic_tokenize 


def run_validation():
    valid = True
    art_count = sum(binary_overall_count.values())
    s_count  = sum(binary_overall_sentence_count.values())
    t_count = sum(binary_overall_token_count.values())

    if all_article_counts != art_count:
        valid = False
        print ('Validation Failed: All of the following must be equal')
        print ('Total articles', all_article_counts)
        print ('Overall article count', art_count)
        print()

    if all_sentence_counts != s_count:
        valid = False
        print ('Validation Failed: All of the following must be equal')
        print ('Total Sentences', all_sentence_counts)
        print ('Overall sentence count', s_count)
        print()

    if all_token_counts != t_count:
        valid = False
        print ('Validation Failed: All of the following must be equal')
        print ('Total Tokens', all_token_counts)
        print ('Overall token count', t_count)        
        print()



    newspaper_prop = 0
    newspaper_non = 0
    for newspaper, tags in binary_count.items():
        newspaper_prop+=tags[prop_tags[1]]
        newspaper_non+=tags[prop_tags[0]]

    newspaper_prop_tok = 0
    newspaper_non_tok = 0
    for newspaper, tags in binary_token_count.items():
        newspaper_prop_tok+=tags[prop_tags[1]]
        newspaper_non_tok+=tags[prop_tags[0]]

    newspaper_prop_sent = 0
    newspaper_non_sent = 0
    for newspaper, tags in binary_sentence_count.items():
        newspaper_prop_sent+=tags[prop_tags[1]]
        newspaper_non_sent+=tags[prop_tags[0]]

    tot_tech = sum(tech_overall_count.values())
    tot_tech_tok = sum(tech_overall_token_count.values())
    tot_tech_sent = sum(tech_overall_sentence_count.values())


    newspaper_tech = 0
    for newspaper in tech_count:
        for count in tech_count[newspaper]:
            newspaper_tech += tech_count[newspaper][count]

    newspaper_tech_sent = 0
    for newspaper in tech_sentence_count:
        for count in tech_sentence_count[newspaper]:
            newspaper_tech_sent += tech_sentence_count[newspaper][count]

    newspaper_tech_tok = 0
    for newspaper in tech_token_count:
        for count in tech_token_count[newspaper]:
            newspaper_tech_tok += tech_token_count[newspaper][count]

    tech_counts = {}
    for newspaper, tech in tech_count.items():
        for tech_name, tech_c in tech.items():
            if tech_name in tech_counts:
                tech_counts[tech_name]+=tech_c
            else:
                tech_counts[tech_name] = tech_c

    tech_sent_counts = {}
    for newspaper, tech in tech_sentence_count.items():
        for tech_name, tech_c in tech.items():
            if tech_name in tech_sent_counts:
                tech_sent_counts[tech_name]+=tech_c
            else:
                tech_sent_counts[tech_name] = tech_c

    tech_tok_counts = {}
    for newspaper, tech in tech_token_count.items():
        for tech_name, tech_c in tech.items():
            if tech_name in tech_tok_counts:
                tech_tok_counts[tech_name]+=tech_c
            else:
                tech_tok_counts[tech_name] = tech_c

    
    
    overall_c = binary_overall_count[prop_tags[1]]
    overall_c_sent = binary_overall_sentence_count[prop_tags[1]]
    overall_c_tok = binary_overall_token_count[prop_tags[1]]

    if overall_c != newspaper_prop:
        valid = False
        print ('Validation Failed: All of the following must be equal')
        print ('Prop Article Count', overall_c)
        print ('Newspaper Prop Article Count', newspaper_prop)
        print()
    
    if tot_tech != newspaper_tech:
        valid = False
        print ('Validation Failed: All of the following must be equal')
        print ('Overall Tech Article Count', tot_tech)
        print ('Newspaper Tech Article Count', newspaper_tech)
        print()

    if overall_c_sent == newspaper_prop_sent == tot_tech_sent == newspaper_tech_sent:
        pass
    else:
        valid = False
        print ('Validation Failed: All of the following must be equal')
        print ('Prop Sentence Count', overall_c_sent)
        print ('Newspaper Prop Sentence Count', newspaper_prop_sent)
        print ('Overall Tech Sentence Count', tot_tech_sent)
        print ('Newspaper Tech Sentence Count', newspaper_tech_sent)
        print()

    if overall_c_tok == newspaper_prop_tok == tot_tech_tok == newspaper_tech_tok:
        pass
    else:
        valid = False
        print ('Validation Failed: All of the following must be equal')
        print ('Prop Token Count', overall_c_tok)
        print ('Newspaper Prop Token Count', newspaper_prop_tok)
        print ('Overall Tech Token Count', tot_tech_tok)
        print ('Newspaper Tech Token Count', newspaper_tech_tok)
        print()


    overall_c_non = binary_overall_count[prop_tags[0]]
    overall_c_sent_non = binary_overall_sentence_count[prop_tags[0]]
    overall_c_tok_non = binary_overall_token_count[prop_tags[0]]

    if overall_c_non != newspaper_non:
        valid = False
        print ('Validation Failed: All of the following must be equal')
        print ('Non Prop Article Count', overall_c_non)
        print ('Newspaper Non Prop Article Count', newspaper_non)
        print()

    if overall_c_sent_non != newspaper_non_sent:
        valid = False
        print ('Validation Failed: All of the following must be equal')
        print ('Non Prop Sentence Count', overall_c_sent_non)
        print ('Newspaper Non Prop Sentence Count', newspaper_non_sent)
        print()

    if overall_c_tok_non != newspaper_non_tok:
        valid = False
        print ('Validation Failed: All of the following must be equal')
        print ('Non Prop Token Count', overall_c_tok_non)
        print ('Newspaper Non Prop Token Count', newspaper_non_tok)
        print()

    for tech, tech_c in tech_overall_count.items():
        newspaper_count = tech_counts[tech]
        if tech_c != newspaper_count:
            valid = False
            print ('Validation Failed: The following counts (overall technique and individual newspaper technique) must be equal')
            print ('Articles', tech, tech_c, newspaper_count)
            print()

    for tech, tech_c in tech_overall_sentence_count.items():
        newspaper_count = tech_sent_counts[tech]
        if tech_c != newspaper_count:
            valid = False
            print ('Validation Failed: The following counts (overall technique and individual newspaper technique) must be equal')
            print ('Sentences', tech, tech_c, newspaper_count)
            print()

    for tech, tech_c in tech_overall_token_count.items():
        newspaper_count = tech_tok_counts[tech]
        if tech_c != newspaper_count:
            valid = False
            print ('Validation Failed: The following counts (overall technique and individual newspaper technique) must be equal')
            print ('Tokens', tech, tech_c, newspaper_count)
            print()

    if valid:
        print ('All Validation Test Passed!')



def write_statistics():
    w_fname = 'propaganda_counts.txt'
    print ('Writing Statistics to', w_fname)

    with open (w_fname, 'w') as f_w:
        f_w.write('Total Count\n')
        f_w.write('===================================\n')

        f_w.write('Article Count\n')
        # f_w.write('-----------------------------------\n')
        f_w.write(json.dumps(binary_overall_count, indent=3))
        f_w.write('\n')
        f_w.write('-----------------------------------\n\n')

        f_w.write('Token Count\n')
        # f_w.write('-----------------------------------\n')
        f_w.write(json.dumps(binary_overall_token_count, indent=3))
        f_w.write('\n')
        # f_w.write(str(binary_overall_token_count)+'\n')
        f_w.write('-----------------------------------\n\n')

        f_w.write('Sentence Count\n')
        # f_w.write('-----------------------------------\n')
        f_w.write(json.dumps(binary_overall_sentence_count, indent=3))
        f_w.write('\n')
        # f_w.write(str(binary_overall_sentence_count)+'\n')

        f_w.write('===================================\n\n\n')



        f_w.write('Newspaper-wise Total Count\n')
        f_w.write('===================================\n')

        f_w.write('Article Count\n')
        # f_w.write('-----------------------------------\n')
        f_w.write(json.dumps(binary_count, indent=3))
        f_w.write('\n')
        # f_w.write(str(binary_count)+'\n')
        f_w.write('-----------------------------------\n\n')

        f_w.write('Token Count\n')
        # f_w.write('-----------------------------------\n')
        f_w.write(json.dumps(binary_token_count, indent=3))
        f_w.write('\n')
        # f_w.write(str(binary_token_count)+'\n')
        f_w.write('-----------------------------------\n\n')

        f_w.write('Sentence Count\n')
        # f_w.write('-----------------------------------\n')
        f_w.write(json.dumps(binary_sentence_count, indent=3))
        f_w.write('\n')
        # f_w.write(str(binary_sentence_count)+'\n')

        f_w.write('===================================\n\n\n')



        f_w.write('Total Technique Count\n')
        f_w.write('===================================\n')

        f_w.write('Article Count\n')
        # f_w.write('-----------------------------------\n')
        f_w.write(json.dumps(tech_overall_count, indent=3))
        f_w.write('\n')
        # f_w.write(str(tech_overall_count)+'\n')
        f_w.write('-----------------------------------\n\n')

        f_w.write('Token Count\n')
        # f_w.write('-----------------------------------\n')
        f_w.write(json.dumps(tech_overall_token_count, indent=3))
        f_w.write('\n')
        # f_w.write(str(tech_overall_token_count)+'\n')
        f_w.write('-----------------------------------\n\n')

        f_w.write('Sentence Count\n')
        # f_w.write('-----------------------------------\n')
        f_w.write(json.dumps(tech_overall_sentence_count, indent=3))
        f_w.write('\n')
        # f_w.write(str(tech_overall_sentence_count)+'\n')

        f_w.write('===================================\n\n\n')



        f_w.write('Newspaper-wise Total Technique Count\n')
        f_w.write('===================================\n')

        f_w.write('Article Count\n')
        f_w.write('-----------------------------------\n')
        f_w.write(json.dumps(tech_count, indent=3))
        f_w.write('\n')
        # f_w.write(str(tech_count))
        f_w.write('-----------------------------------\n')

        f_w.write('Token Count\n')
        f_w.write('-----------------------------------\n')
        f_w.write(json.dumps(tech_token_count, indent=3))
        f_w.write('\n')
        # f_w.write(str(tech_token_count))
        f_w.write('-----------------------------------\n')

        f_w.write('Sentence Count\n')
        f_w.write('-----------------------------------\n')
        f_w.write(json.dumps(tech_sentence_count, indent=3))
        f_w.write('\n')
        # f_w.write(str(tech_sentence_count))

        f_w.write('===================================\n\n')



prop_tags = ['0', '1']

pat = '([a-zA-Z]+)'
working_dir = os.getcwd()

all_dirs = os.listdir()

tech_count = {}
tech_token_count = {}
tech_sentence_count = {}

tech_overall_count = {}
tech_overall_token_count = {}
tech_overall_sentence_count = {}

all_article_counts = 0
all_token_counts = 0
all_sentence_counts = 0

binary_count = {}
binary_token_count = {}
binary_sentence_count = {}

binary_overall_count = {prop_tags[0]:0, prop_tags[1]:0}
binary_overall_token_count = {prop_tags[0]:0, prop_tags[1]:0}
binary_overall_sentence_count = {prop_tags[0]:0, prop_tags[1]:0}

for cur_dir, sub_dir, all_files in os.walk(working_dir):
    for cur_file in all_files:
        file_path = os.path.join(cur_dir, cur_file)
        if file_path.endswith('.ann'):
            all_article_counts+=1
            print('Current working file', file_path)
            prefix = re.match(pat, cur_file).groups()[0]
            txt_file = file_path.replace('.ann', '.txt')
            
            with open(txt_file) as f_t:
                article = f_t.read().strip()
                all_sents = len(sentence_tokenize.sentence_split(article, lang='hi'))
                all_tokens = len(indic_tokenize.trivial_tokenize(article))
                all_sentence_counts+=all_sents
                all_token_counts+=all_tokens


            prop_sent_count = 0
            prop_token_count = 0
            prop = False
            prop_tag = prop_tags[0]
            with open(file_path) as f_r:
                reader = csv.reader(f_r, delimiter='\t')                  
                for row in reader:                    
                    technique = row[1].strip().split()[0]
                    prop_txt = row[-1].strip()
                    sent_count = len(sentence_tokenize.sentence_split(prop_txt, lang='hi'))
                    token_count = len(indic_tokenize.trivial_tokenize(prop_txt))
                    prop_sent_count+=sent_count
                    prop_token_count+=token_count
                    prop = True 
                    prop_tag =  prop_tags[1]                 

                    if technique in tech_overall_count:
                        tech_overall_count[technique] += 1
                        tech_overall_sentence_count[technique] += sent_count
                        tech_overall_token_count[technique] += token_count

                        if prefix in tech_count:
                            if technique in tech_count[prefix]:
                                tech_count[prefix][technique] += 1
                                tech_sentence_count[prefix][technique] += sent_count
                                tech_token_count[prefix][technique] += token_count
                            else:
                                tech_count[prefix][technique]= 1
                                tech_sentence_count[prefix][technique] = sent_count
                                tech_token_count[prefix][technique] = token_count
                        else:
                            tech_count[prefix] = {technique: 1}
                            tech_sentence_count[prefix]= {technique: sent_count}
                            tech_token_count[prefix] = {technique: token_count}
                    else:
                        tech_overall_count[technique] = 1
                        tech_overall_sentence_count[technique] = sent_count
                        tech_overall_token_count[technique] = token_count

                        if prefix in tech_count:
                            if technique in tech_count[prefix]:
                                tech_count[prefix][technique] += 1
                                tech_sentence_count[prefix][technique] += sent_count
                                tech_token_count[prefix][technique] += token_count
                            else:
                                tech_count[prefix][technique]= 1
                                tech_sentence_count[prefix][technique] = sent_count
                                tech_token_count[prefix][technique] = token_count
                        else:
                            tech_count[prefix] = {technique: 1}
                            tech_sentence_count[prefix]= {technique: sent_count}
                            tech_token_count[prefix] = {technique: token_count}
                
                
                non_sent_count = all_sents - prop_sent_count
                non_token_count = all_tokens - prop_token_count

                if prop:
                    prop_tag = prop_tags[1]
                    binary_overall_count[prop_tag] += 1
                    binary_overall_sentence_count[prop_tag] += prop_sent_count
                    binary_overall_token_count[prop_tag] += prop_token_count

                    binary_overall_sentence_count[prop_tags[0]] += non_sent_count
                    binary_overall_token_count[prop_tags[0]] += non_token_count
                    
                    if prefix in binary_count:
                        if prop_tag in binary_count[prefix]:
                            binary_count[prefix][prop_tag] += 1
                            binary_sentence_count[prefix][prop_tag] += prop_sent_count
                            binary_token_count[prefix][prop_tag] += prop_token_count

                            binary_sentence_count[prefix][prop_tags[0]] += non_sent_count
                            binary_token_count[prefix][prop_tags[0]] += non_token_count
                        else:
                            binary_count[prefix][prop_tag] = 1
                            binary_sentence_count[prefix][prop_tag] = prop_sent_count
                            binary_token_count[prefix][prop_tag] = prop_token_count

                            binary_sentence_count[prefix][prop_tags[0]] += non_sent_count
                            binary_token_count[prefix][prop_tags[0]] += non_token_count
                    else:
                        binary_count[prefix] = {prop_tag: 1, prop_tags[0]: 0}
                        binary_sentence_count[prefix] = {prop_tag: prop_sent_count, prop_tags[0]: non_sent_count}
                        binary_token_count[prefix] = {prop_tag: prop_token_count, prop_tags[0]: non_token_count}
                else:
                    prop_tag = prop_tags[0]
                    binary_overall_count[prop_tag] += 1
                    binary_overall_sentence_count[prop_tag] += non_sent_count
                    binary_overall_token_count[prop_tag] += non_token_count
                    
                    if prefix in binary_count:
                        if prop_tag in binary_count[prefix]:
                            binary_count[prefix][prop_tag] += 1
                            binary_sentence_count[prefix][prop_tag] += non_sent_count
                            binary_token_count[prefix][prop_tag] += non_token_count
                        else:
                            binary_count[prefix][prop_tag] = 1
                            binary_sentence_count[prefix][prop_tag] = non_sent_count
                            binary_token_count[prefix][prop_tag] = non_token_count
                    else:
                        binary_count[prefix] = {prop_tag: 1, prop_tags[1]: 0}
                        binary_sentence_count[prefix] = {prop_tag: non_sent_count, prop_tags[1]: 0}
                        binary_token_count[prefix] = {prop_tag: non_token_count, prop_tags[1]: 0}


run_validation()
write_statistics()

    

    

    