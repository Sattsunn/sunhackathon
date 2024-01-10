import os

import boto3


def get_slack_signing_secret() -> str:
    """
    SlackのSigning Secretをパラメーターストアから取得します。
    :return: SlackのSigning Secret
    """
    client = boto3.client('ssm')
    slack_signing_secret_parameter_name = os.environ["SLACK_SIGNING_SECRET_PARAMETER_NAME"]

    response = client.get_parameter(
        Name=slack_signing_secret_parameter_name,
        WithDecryption=True
    )
    signing_secret = response['Parameter']['Value']

    return signing_secret


def get_slack_bot_token() -> str:
    """
    SlackのBot Tokenをパラメーターストアから取得します。
    :return: SlackのBot Token
    """
    client = boto3.client('ssm')
    slack_bot_token_parameter_name = os.environ["SLACK_BOT_TOKEN_PARAMETER_NAME"]

    response = client.get_parameter(
        Name=slack_bot_token_parameter_name,
        WithDecryption=True
    )
    bot_token = response['Parameter']['Value']

    return bot_token


def get_azure_openai_service_api_key() -> str:
    """
    Azure OpenAI ServiceのAPI Keyをパラメーターストアから取得します。
    :return: Azure OpenAI ServiceのAPI Key
    """
    client = boto3.client('ssm')
    azure_openai_api_key_parameter_name = os.environ["AZURE_OPENAI_API_KEY_PARAMETER_NAME"]

    response = client.get_parameter(
        Name=azure_openai_api_key_parameter_name,
        WithDecryption=True
    )
    api_key = response['Parameter']['Value']

    return api_key