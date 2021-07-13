from NER_modules import extractors

def name_extracting_service(text):
    articles_matches = extractors.NamesExtractor()
    result = articles_matches(text)
    return result

def location_extracting_service(text):
    articles_matches = extractors.LocationExtractor()
    result = articles_matches(text)
    return result

def date_extracting_service(text):
    articles_matches = extractors.DatesExtractor()
    result = articles_matches(text)
    return result

def person_extracting_service(text):
    articles_matches = extractors.PersonExtractor()
    result = articles_matches(text)
    return result


def earley_parser(option, text):
    if option == 0:
        parser_result = person_extracting_service(text)
    elif option == 1:
        parser_result = name_extracting_service(text)
    elif option == 2:
        parser_result = location_extracting_service(text)
    elif option == 3:
        parser_result = date_extracting_service(text)
    return parser_result


