import infermedica_api
import json

app_id =  '{get your key from infermedica}'
app_key = "{get your key from infermedica}" #https://infermedica.com
api = infermedica_api.API(app_id=app_id, app_key=app_key)

symptoms_list = []
conditions_list = []
with open('symptoms.json') as symfile:
    symptoms_list = json.load(symfile)

with open('conditions.json') as condfile:
    conditions_list = json.load(condfile)




def initialize_request(age, sex):
    """
    Creates initial diagnosis request.
    :param age: Patient's age.
    :param sex: Patient's gender.
    :return:
    """
    print("requesting " + str(age) + str(sex) )
    request = infermedica_api.Diagnosis(age=age, sex='male')
    return request

def add_symptom_to_request_multichoice(request, id, isPresent):
    present = "present" if isPresent else "absent"
    request.add_symptom(id, present)


def add_symptom_to_request(request, id, isPresent):
    present = "present" if isPresent else "absent"
    request.add_symptom(id, present)
    request = api.diagnosis(request)
    return request


def filter_words(sentence):
    """
    Filter what patient said to what might be a medical symptom. We require at least 4 characters
    per word to consider it as a candidate symptom before actually processing it.
    I did that to save processing time after checking the list of symptoms.
    :param sentence:
    :return: relevant_words is a list of possible symptoms.
    """
    words = sentence.split(' ')
    relevant_words = []
    for word in words:
        if len(word) > 4:
            relevant_words += [word]
            print(word)
        else:
            print(len(word))
    return relevant_words


def find_symptoms_from_relevant_words(relevant_words_list):
    """
    Iterate over the list of possibly relevant words and try to find it's corresponding in the
    symptoms json file. if found, add their ID to a list.
    :param relevant_words_list: list of words filtered from
    what patient said in the microphone in the first time.
    :return: found_symptoms is a list of symptom identifiers that are known to Infermedica.
    """
    found_symptoms = []
    for word in relevant_words_list:
        for symptom in symptoms_list:
            if symptom['name'].lower() == word:
                print(symptom['id'] + " " + word)
                found_symptoms += [symptom['id']]
    return found_symptoms


#print(api.info())


#symptoms_list = api.symptoms_list()

#conditions_list = api.conditions_list()


#with open('symptoms.json', 'w') as symfile:
#    json.dump(symptoms_list, symfile)


#with open('conditions.json', 'w') as condfile:
#    json.dump(conditions_list, condfile)