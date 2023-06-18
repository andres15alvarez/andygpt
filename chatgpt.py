import openai
from config import OPENAI_API_KEY, PROXY, OPENAI_MODEL, TEMPERATURE, N_CHOICES


class ChatGPTHelper:
    """
    ChatGPT helper class.
    """

    def __init__(self):
        """Initializes the OpenAI helper class with the given configuration."""
        openai.api_key = OPENAI_API_KEY
        openai.proxy = PROXY

    async def get_chat_response(self, query: str) -> str:
        """Get the answer from ChatGPT.

        Args:
            - query (str): question

        Raises:
            - Exception: _description_

        Returns:
            - str: ChatGPT's answer
        """
        try:
            response = await openai.ChatCompletion.acreate(
                model=OPENAI_MODEL,
                messages=[{'role': 'user', 'content': query}],
                temperature=TEMPERATURE,
                n=N_CHOICES,
            )
        except openai.error.InvalidRequestError as e:
            raise Exception(f"⚠️ _Solicitud inválida de OpenAI._ ⚠️\n{str(e)}") from e
        except Exception as e:
            raise Exception(f"⚠️ _Ha ocurrido un error._ ⚠️\n{str(e)}") from e
        answer = ''
        answer = response.choices[0]['message']['content'].strip()
        return answer
