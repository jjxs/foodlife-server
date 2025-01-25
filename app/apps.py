from django.apps import AppConfig
import app.common.message as Message
import app.log.logger as Logger


class AppConfig(AppConfig):
    name = 'app'

    def ready(self):
        try:
            Message.init_cache()
        except Exception as e:
            Logger.error(e)
            pass

        print("app starting...")
        pass  # startup code here
