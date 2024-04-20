#Function to calculate Moving Average Type Token Ratio
def MATTR(text, windowsize):
    #process text using spaCy
    text = nlp(text)
    if (len(text) <= windowsize):
        return np.nan
    else:
        # moving average TTR
        MATTR = 0
        # Sum of all TTR scores
        TTR_sum = 0
        # Number of TTR values calculates, used to calculate mean from sun.
        TTR_n = 0
        #starting index for window to calc TTR
        start_window_idx = 0
        # Check that text is longer than window size from the start of window index
        if len(text) > (start_window_idx + windowsize):
            TTR_n += 1
            #slide window along text to calculate TTR score for each window
            text_in_window = text[start_window_idx: (start_window_idx + windowsize)]
            TTR_sum += calcTTR(text_in_window)
            start_window_idx += 1
        else:
            # Calculate moving average as mean TTR value for text.
            MATTR = TTR_sum / TTR_n
            return MATTR

def calcTTR(text):
    TTR = 0
    # get list of words
    words = []
    types = set()
    for token in text:
        if token.is_alpha:
            #print(token.text)
            words.append(token.text)
            types.add(token.text)

    # TTR = Count of types (unique words) / count of words
    TTR = len(words) / len(types)
    print(f'TTR: {TTR}')
    return TTR