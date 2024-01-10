import os
import openai


def get_answer(chat_message, azure_openai_service_api_key: str) -> str:
    """
    Azure OpenAI Serviceから回答を取得します。
    :param chat_message: Azure OpenAI Serviceに渡す会話履歴
    :param azure_openai_service_api_key: Azure OpenAI ServiceのAPI Key
    :return: Azure OpenAI Serviceから取得した回答
    """
    openai.api_type = "azure"
    openai.api_base = os.environ['AZURE_OPENAI_SERVICE_ENDPOINT']
    openai.api_version = os.environ['AZURE_OPENAI_SERVICE_API_VERSION']
    openai.api_key = azure_openai_service_api_key

    response = openai.ChatCompletion.create(
        engine=os.environ['AZURE_OPENAI_SERVICE_ENGINE'],
        messages=chat_message,
        temperature=0.7,
        max_tokens=800,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None)

    return response["choices"][0]["message"]["content"]