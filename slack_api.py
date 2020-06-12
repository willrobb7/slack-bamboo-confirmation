from slack import WebClient


class Slack:

    def __init__(self, token: str):
        self.__token = token
        self._client = WebClient(token=self.__token)

    def get_user(self, email: str):
        user = self._client.users_lookupByEmail(email=email)

        if user.get("ok"):
            return user.get("user")
        else:
            return user

    def message_user(self, email: str, text: str, blocks: str = None):
        user = self.get_user(email)
        user_id = user.get("id")

        conversation = self._client.conversations_open(users=user_id)
        channel = conversation.get("channel").get("id")

        return self._client.chat_postMessage(channel=channel, text=text, blocks=blocks)
