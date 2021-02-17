import nltk
import enchant
class Utils:
    d = enchant.Dict("en_US")
    def find_closest_match(update,context,sample_space,word): # Finds the closest match for the given word in the provided sample space
        print(word)
        word = word.title().replace('And', 'and')
        if word.lower()=='us':
            print('fuck you')
            word = 'US'
        if word.lower()=='uk':
            word = 'United Kingdom'
        if len(word)==2:
            word = 'US'
        str_distance = []
        for item in sample_space:
            closeness = nltk.edit_distance(item, word) # Generates the Levenshtein distance of the two words. More http://en.wikipedia.org/wiki/Levenshtein_distance
            if closeness==0:
                return (word, True)
            if word in item:
                return item
            str_distance.append(closeness)
        max_index = 0
        for index in range(1, len(str_distance)):
            if str_distance[index]<str_distance[max_index]:
                max_index = index
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Couldn't find a match for {word}. Using {sample_space[max_index]} instead.")
        return (sample_space[max_index], False)

    def find_closest_state(update,context,sample_space,word): # Finds the closest match for the given word in the provided sample space
        str_distance = []
        for item in sample_space:
            closeness = nltk.edit_distance(item, word) # Generates the Levenshtein distance of the two words. More http://en.wikipedia.org/wiki/Levenshtein_distance
            if closeness==0:
                return word
            if word in item:
                print(word,item)
                return item
            str_distance.append(closeness)
        max_index = 0
        for index in range(1, len(str_distance)):
            if str_distance[index]<str_distance[max_index]:
                max_index = index
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Couldn't find a match for {word}. Using {sample_space[max_index]} instead.")
        return sample_space[max_index]
    def is_country(term, countries):
        return term.title().replace('And', 'and').replace('Us', 'US').replace('Uk', 'United Kingdom') in countries
    def is_state(term, states):
        return term.lower() in states
    def is_valid_word(word):
        return Utils.d.check(word)