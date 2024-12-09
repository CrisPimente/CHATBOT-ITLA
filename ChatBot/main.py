import re
import random
from itla_responses import responses_data  # Importamos las preguntas y respuestas

# Función principal para procesar la entrada del usuario
def get_response(user_input):
    split_message = re.split(r'\s|[,:;.?!-_]\s*', user_input.lower())
    response = check_all_messages(split_message)
    return response

# Función para calcular la probabilidad de coincidencia de un mensaje
def message_probability(user_message, recognized_words, single_response=False, required_words=[]):
    message_certainty = 0
    has_required_words = True

    for word in user_message:
        if word in recognized_words:
            message_certainty += 1

    percentage = float(message_certainty) / float(len(recognized_words)) if recognized_words else 0

    for word in required_words:
        if word not in user_message:
            has_required_words = False

    if has_required_words or single_response:
        return int(percentage * 100)
    else:
        return 0

# Función para verificar todas las posibles respuestas
def check_all_messages(message):
    highest_probability = {}

    def response(bot_response, list_of_words, single_response=False, required_words=[]):
        nonlocal highest_probability
        highest_probability[bot_response] = message_probability(
            message, list_of_words, single_response, required_words
        )

    # Importamos las respuestas desde el archivo itla_responses.py
    for item in responses_data:
        response(item['response'], item['keywords'], item['single_response'], item['required_words'])

    best_match = max(highest_probability, key=highest_probability.get)
    return unknown() if highest_probability[best_match] < 1 else best_match

# Función para manejar respuestas desconocidas
def unknown():
    responses = [
        '¿Puedes repetir tu pregunta?', 
        'No tengo información sobre eso.', 
        '¿Podrías ser más específico?',
        'No estoy seguro, pero puedes buscar en la página oficial del ITLA.'
    ]
    return random.choice(responses)

# Bucle principal
if __name__ == "__main__":
    while True:
        print("Bot: " + get_response(input("You: ")))
