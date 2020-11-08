from fuzzywuzzy import fuzz

def get_regions(summarised_text: list, transrcipt, SENTENCE_COUNT:int):

    regions = [] 
    for text in summarised_text:
        for t_dict in transrcipt:
            if fuzz.ratio(text, t_dict['text']) > 30:
                regions.append(
                    {'start': round(float(t_dict['start']), 2), 'end': round(float(t_dict['start'] + t_dict['duration']), 2), 'rating': fuzz.ratio(text, t_dict['text'])})
                print(t_dict['start'], '=>', t_dict['start'] + t_dict['duration'])
    
    score_sorted = sorted(regions,key= lambda x:x['rating'] , reverse=True) 
    sorted_regions = sorted(score_sorted[:SENTENCE_COUNT],key= lambda x:x['start'])
    print(cure_repetition(sorted_regions))
    return cure_repetition(sorted_regions)

def cure_repetition(regions):
    cured = []
    for region in regions:
        if len(cured) == 0:
            cured.append(region)
        else:
            last = cured[-1]
            if last['end'] >= region['start']:
                 last['end'] = region['end'] 
                 cured[-1] = last
            else:
                cured.append(region)
    return cured
