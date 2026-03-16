class Person:
    def __init__(self, name):
        self.name=name
    def greet(self):
        print("Hello, my name is "+ self.name)
p1=Person("Emil")
p1.greet()
#2 with parameters
class Calculator:
    def add(self, a,b):
        return a+b
    def multiply(self,a,b):
        return a*b
calc=Calculator()
print(calc.add(5,3))
print(calc.multiply(4,7))

#3 multiple methods
class Playlist:
    def __init__(self,name):
        self.name=name
        self.songs = []
    def add_song(self,song):
        self.songs.append(song)
        print(f"Added:{song}")

    def remove_song(self, song):
        if song in self.songs:
            self.songs.remove(song)
            print()
    def show_songs(self):
        print(f"Playlist '{self.name}':")
        for song in self.songs:
            print(f"-{song}")

my_playlist=Playlist("Favorites")
my_playlist.add_song("Bohemian Rhapsody")
my_playlist.add_song("Stairway to Heaven")
my_playlist.show_songs()

#4 delete methods
class Persond:
    def __init__(self, name):
        self.name=name
    def greet(self):
        print("Hello!")
p3 = Persond ("Emil")

del Persond.greet

#p3.greet()


#Challenge
class Rectangle:
    def __init__(self, width, height):
        self.width=width
        self.height=height
    def areas(self):
        area = self.width * self.height
        return area
r1 =Rectangle(5,3)

print(r1.areas())