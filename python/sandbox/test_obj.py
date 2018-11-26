
class Book:
    data = {}

    def __init__(self, value1: str, value2: int):
        self.data = {}
        self.data["value"] = value1
        self.data["int"] = value2

    def __repr__(self):
        return "{{ {}, {} }}".format(self.data["value"], self.data["int"])


myBook_1 = Book("stringvalue", 10)
myBook_2 = Book("anothervalue", 20)

print(myBook_1)
print(myBook_2)
