from fuzzywuzzy import fuzz

def get_regions(summarised_text: list, transrcipt):

    regions = [] 
    for text in summarised_text:
        for t_dict in transrcipt:
            print(t_dict)
            if fuzz.partial_ratio(text, t_dict['text']) > 70:
                regions.append(
                    {'start': t_dict['start'], 'end': t_dict['start'] + t_dict['duration']})
    

  