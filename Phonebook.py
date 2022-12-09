import json
from json import JSONEncoder

filename = 'book.txt'


class Contact:

    def __init__(self, iid, fname, lname, phone):
        self.id = iid
        self.fname = fname
        self.lname = lname
        self.phone = phone


class Phonebook:

    def __init__(self):
        self.data = []

    def add(self, x):
        self.data.append(x)

    def save(self):
        with open(filename, "w") as openfile:
            json.dump(self.data, fp=openfile, cls=ContactEncoder, indent=4)
        self.data.clear()

    def load(self):
        with open(filename, "r") as readfile:
            self.data = json.load(readfile)

    def delete_cont(self, contid):
        for cont in self.data:
            if contid == cont['id']:
                self.data.remove(cont)

class ContactEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__

