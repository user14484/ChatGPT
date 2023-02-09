import ChatGPT

if __name__ == "__main__":
    # Создаём объект класса ChatGPT
    chat = ChatGPT.ChatGPT("your_api_key_here")

    # Список который хранит нашу историю чата
    chat_history = []


    while(True):
        try:
            # Считываем ввод пользователя
            question = input("Вы: ")

            # Если пользователь хочет выйти, завершаем программу
            if(question == "/exit"):
                break;

            # Получаем ответ от бота
            result = chat.getAnswer(question, chat_history, lang="ru")

            #Записываем текст ответа
            generated_text = result["message"]

            # Обновляем историю чата
            chat_history = result["history"]

            # Выводим ответ бота пользователю
            print(f"ChatGPT: {generated_text}")

        except Exception as e:
            print(f"[Error] {e}")