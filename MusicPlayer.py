import os
import numpy as np
import pygame

pygame.mixer.init()
pygame.mixer.music.set_volume(1)

class custom_random:
    def __init__(self, seed):
        self.seed = seed

    def generate(self, max_value):
        self.seed = (self.seed * 1103515245 + 12345) & 0x7FFFFFFF
        return self.seed % max_value

class Shuffle(list):
    def __init__(self, seed):
        self.random_generator = custom_random(seed)
        super().__init__()

    def do(self, l):
        song_order = []
        song_list = []

        while len(song_order) != 20:
            choice = self.random_generator.generate(20)
            if choice not in song_order:
                song_order.append(choice)
                song_list.append(l[choice])

        return song_list

def main():
    song = 0
    start_flag = False
    pauflag = False
    nextflag = False
    prevflag = False

    l = [song for song in os.listdir('Songs') if song.endswith('.mp3')]
    print(l)
    seed = int(input("Enter a seed value: "))
    s = Shuffle(seed)
    l = s.do(l)
    
    while True:
        if not start_flag:
            user_choice = input("Enter 'start' to enter, 'quit' to exit: ")
            if user_choice == "start":
                start_flag = True
                play = True
                curr_song = l[song]
                pygame.mixer.music.load(os.path.join('Songs', curr_song))
                pygame.mixer.music.play()
            elif user_choice == "quit":
                pygame.quit()
                break
            else:
                print("Invalid choice")

        print("Enter 'pause', 'play', 'quit', 'next', 'prev', or 'shuffle'")
        user_choice = input()

        if user_choice == "next":
            if pauflag:
                song += 1
                song %= 20
                nextflag = True
                curr_song = l[song]
                pygame.mixer.music.load(os.path.join('Songs', curr_song))
                print("Current song: ", curr_song)
                continue

            pygame.mixer.music.stop()
            song += 1
            song %= 20
            curr_song = l[song]
            pygame.mixer.music.load(os.path.join('Songs', curr_song))
            pygame.mixer.music.play()
            print("Current song: ", curr_song)

        elif user_choice == "prev":
            if pauflag:
                song -= 1
                song %= 20
                nextflag = True
                curr_song = l[song]
                pygame.mixer.music.load(os.path.join('Songs', curr_song))
                print("Current song: ", curr_song)
                continue

            pygame.mixer.music.stop()
            song -= 1
            song %= 20
            curr_song = l[song]
            pygame.mixer.music.load(os.path.join('Songs', curr_song))
            pygame.mixer.music.play()
            print("Current song: ", curr_song)

        elif user_choice == "quit":
            pygame.quit()
            break

        elif user_choice == "pause":
            pygame.mixer.music.pause()
            pauflag = True

        elif user_choice == "play":
            if pauflag and (nextflag or prevflag):
                pauflag = False
                nextflag = False
                prevflag = False
                pygame.mixer.music.play()
                continue

            pygame.mixer.music.unpause()
            pauflag = False

        elif user_choice == "shuffle":
            pygame.mixer.music.stop()
            seed = int(input("Enter a new seed value: "))
            s = Shuffle(seed)
            l = s.do(l)
            play = True
            curr_song = l[song]
            pygame.mixer.music.load(os.path.join('Songs', curr_song))
            pygame.mixer.music.play()
            pauflag = False
            nextflag = False
            prevflag = False
            print("Current song:", curr_song)

        else:
            print("Invalid input")

if __name__ == '__main__':
    main()

