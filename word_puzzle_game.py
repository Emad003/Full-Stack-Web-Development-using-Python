import random
GAME_DATA = ["SAURABH", "NAVIN", "PRATEEK","ADITYA","SHRIDHAR"]
score=0
i=0
while i<5:
    print("Arrange the letters to form a valid word:")
    print(''.join(random.sample(GAME_DATA[i],len(GAME_DATA[i]))))
    inpt=input()
    if len(inpt)==len(GAME_DATA[i]) and inpt.upper() in GAME_DATA[i]: 
        print("\nCorrect\n")
        score+=1
    else:
        print("\nWrong\n")
        score-=1
    i+=1
else:
    print("Net Score ",score)