import os

with open('config/config.txt') as f:
    configtxt = f.readlines()

config = ['' for i in range (len(configtxt))]
for i in range (len(configtxt)):
    for j in range (len(configtxt[i])):
        if configtxt[i][j] != '\n':
            config[i] += configtxt[i][j]

userAmount = int(config[1])

#user
with open('users/users.txt') as f:
    userstxt = f.readlines()


users = ['' for i in range (len(userstxt))]
for i in range (len(userstxt)):
    for j in range (len(userstxt[i])):
        if userstxt[i][j] != '\n':
            users[i] += userstxt[i][j]


with open('musics/musics.txt') as f:
    musicstxt = f.readlines()



i = 0
while i < userAmount:
    fileDirect = 'users/' + users[i * 2 + 1] + '.txt'
    os.remove(fileDirect)
    i += 1
    
f = open('config/config.txt', 'w')
f.write('user\n0\nsongs\n' + str(len(musicstxt)//6))
f.close()
f = open('users/users.txt', 'w')
f.write('user')
f.close()

