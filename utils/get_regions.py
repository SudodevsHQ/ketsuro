from fuzzywuzzy import fuzz

def get_regions(summarised_text: list, transrcipt):

    regions = [] 
    for text in summarised_text:
        for t_dict in transrcipt:
            if fuzz.partial_ratio(text, t_dict['text']) > 80:
                regions.append(
                    {'start': float(t_dict['start']), 'end': float(t_dict['start'] + t_dict['duration'])})
                break
    return regions

  