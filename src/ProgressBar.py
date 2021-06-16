from progress.bar import Bar


class ProgressBar(Bar):

    suffix = '%(percent)d%%'

    def __init__(self, *args, **kwargs):
        super(Bar, self).__init__(*args, **kwargs)
        self.max = 9

    def update_message(self, message: str):
        message = (message[:35] + '..') if len(message) > 35 else message
        self.message = message.ljust(37, ".")
        self.update()
