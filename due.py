import datetime

class Due:

    # exp: Due('date':)
    def __init__(self, **kwargs):
        self.date = kwargs.get('date')
        self.text = kwargs.get('text')
