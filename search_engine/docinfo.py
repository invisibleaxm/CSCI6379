#!/usr/local/bin/python3
import json

class docinfo:
    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
            sort_keys=True, indent=4)

    def __init__(self):
        self.id = ''
        self.filename = ''
        self.url = ''
        self.title = ''
        self.snip = ''

