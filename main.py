
import infermedica
import speak
import process_voice


#Process Symptoms is the main function that connects the input, output, and
#infermedica AI together to make the medical diagnosis for the patient.

def ProcessSymptoms(actual, request, isPresent):
    """
    Process Symptoms is a recursive function that acts as the main function that guides the
    sequence of the medical diagnosis connecting Input, Output, and Infermedica AI system.
    :param actual: The symptoms that were found from patient's words spoken in the microphone.
    :param request: The request object that holds the session with Infermedica AI system.
    :param isPresent: Is the symptom present of absent?
    :return: Void.
    """
    if len(actual) > 0:
        # add_symptom_to_request adds a present or absent symptoms to
        # Infermedica Diagnosis session.
        request = infermedica.add_symptom_to_request(request, actual[0],isPresent)
        print(request.question)
        print(request.conditions)
        speak.speak_words(request.question.text)
        iterator = 0
        question_type = request.question.type
        if request.should_stop == True:
            print("Arrived to results!")
            print(request.conditions[0])
        for item in request.question.items:
            iterator += 1
            speak.speak_words((item["name"] if question_type == "group_multiple" or question_type == "group_single" else "")
                                  + "? Please Answer only Yes or No")
            result = process_voice.GetTextFromSpeechUsingGoogle()
            isPresent = True if result.lower() == "yes" else False
            if iterator == len(request.question.items):
                ProcessSymptoms([item['id']], request, isPresent)
            else:
                infermedica.add_symptom_to_request_multichoice(request, item["id"], isPresent)
    else:
        speak.speak_words("Sorry, I cannot understand your symptoms.. Please say again What do you feel.")
        symptom = process_voice.GetTextFromSpeechUsingGoogle()
        symps = infermedica.filter_words(symptom)
        actual_again = infermedica.find_symptoms_from_relevant_words(symps)
        ProcessSymptoms(actual_again, request, True)


#The program starts here by asking the patient about their name.
#speak.speak_words("Hello Patient! What's your name? Please only say your name")

#We save patient's name in an object called name.
#name = process_voice.GetTextFromSpeechUsingGoogle()
#print(name)

#We ask the patient to tell their age to use it in Infermedica diagnosis.
#speak.speak_words("How old are you?")
age = 26 #process_voice.GetTextFromSpeechUsingGoogle()
#print(age)

#Get the gender.
#speak.speak_words("Are you a boy or a girl?")
gender = 'male' #process_voice.GetTextFromSpeechUsingGoogle()
#print(gender)

#Starting this line, the actual Infermedica Artificial Intelligence
#  starts taking control of the program flow.
speak.speak_words("How do you feel?")
#We save what the patient says in the microphone in string object called symptom.
symptom = process_voice.GetTextFromSpeechUsingGoogle()

#Filtering what patient said to get what might be relevant to medical symptoms.

symps = infermedica.filter_words(symptom)
print(symps)

#Get the actual medical symptoms from filtered words.
actual = infermedica.find_symptoms_from_relevant_words(symps)
print(actual)

#Start Infermedica diagnosis session.
request = infermedica.initialize_request(age, gender)

#We set isPresent to True in the case because the patient said for ex:
# "I Have a Headache", so he must have headache present right? xDDD
isPresent = True

#Start the process.
ProcessSymptoms(actual, request, isPresent)

