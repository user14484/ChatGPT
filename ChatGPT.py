import openai
import mtranslate

class ChatGPT:

    def __init__(self, api_key):
        openai.api_key = api_key

    def getAnswer(self, message, chat_history=[], lang="ru", max_tokens=4000, temperature=0.5, engine_model="text-davinci-003"):
        try:
            # Формируем контекст и переводим всё на английский язык
            chat_history.append(mtranslate.translate(message.strip(), "en", "auto"))
            # Формируем сообщение для отправки боту
            prompt = " ".join(chat_history)
            if(len(prompt) > 4000):
                prompt = prompt[-4000]
            # Считаем количество токенов
            num_tokens = len(list(prompt))
            # Если количество токенов превышает допустимое количество, то отчищаем предыдущий контекст
            if(num_tokens > max_tokens):
                chat_history = []
                chat_history.append(mtranslate.translate(message.strip(), "en", "auto"))
                prompt = " ".join(chat_history)
                num_tokens = len(list(prompt))

            # Отправляем контекст на серверы OpenAI и получаем ответ
            response = openai.Completion.create(
                engine=engine_model,
                prompt=prompt,
                max_tokens=max_tokens-num_tokens,
                n=1,
                stop=None,
                temperature=temperature,
            )

            result = response["choices"][0]["text"].strip()

            # Если бот вернул пустой ответ
            if(not result):
                result = "Sorry, the bot didn't return the result.";

            chat_history.append(result)

            # Возращаем полученный и переводим его на нужный нам язык текст
            return {"message": mtranslate.translate(result, lang, "auto"), "history": chat_history}
        except Exception as e:
            if(e == "The server had an error while processing your request. Sorry about that!"):
                return {"message": mtranslate.translate(e, lang, "auto"), "history": chat_history}

            return {"message": f"Sorry, but an error has occurred:\n{e}", "history": chat_history}
