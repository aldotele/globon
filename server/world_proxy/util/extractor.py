def extract_factbook_population(raw):
    # raw is like "61,021,855 (2023 est.)"
    number_piece = raw.split()[0]
    return int(number_piece.replace(',', ''))
