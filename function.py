__author__ = 'denislavrov'
FILEPATH = "auth.txt"  # File path for user database
def filewrite(file, *arg):  # little helper function to write lines to file separated by new line
    # notice the little asterisk next to arg, this means that the function will allow multiple arguments to be passed
    # for example insertuser(file, line1, line2, "completely random string") and it will still work
    if len(arg) != 0:  # check that the argument list is not 0, because all the arguments are stored in arg as a list
        for i in arg:  # for each item in arguments write it and then write a new line character
            file.write(i)
            file.write('\n')
          # be sure to close the file after writing to it


def readsec():  # little helpet function that returns the list of usenames in list of tuples [username, password]
    secfile = open(FILEPATH, mode='r+')  # open the file in read mode with some extra permissions
    ibuffer = secfile.readlines()  # read the file into buffer just because it is easier to work with while its in mem
    sec = []  # declare an output buffer
    i = 0
    while i < len(ibuffer) - 1:  # while loop to go through each username and password pair to make them into tuple
        u = ibuffer[i].strip('\n')  # stripping new line characters of those strings, take it off and see what happens
        i += 1
        p = ibuffer[i].strip('\n')
        i += 1
        sec.append([u, p])  # add each pair to list of pairs / output buffer
    secfile.close()  # be sure to close the file after all possible operations are done
    return list(sec)  # return the list we have obtained


# sample output of that function [[user1,pass1],[user2,pass2],[user3,pass3]]

def printUser():  # another little helper function that prints those usernames and passwords nicely
    print("%-20s %-20s" % ("Username:", "Password:"))
    for i in readsec():
        print("%-20s %-20s" % (i[0], i[1]))


def rmuser(username):
    buff = readsec()
    secfile = open(FILEPATH, mode='w+')
    for i in buff:
        if i[0] != username:
            filewrite(secfile, i[0], i[1])
        else:
            if input("Would you like to remove %s [Y,N]:" % i[0]).lower() == 'n':
                filewrite(secfile, i[0], i[1])
    secfile.close()


def formatUser():  # dirty function i use to locate usernames
    sout = []  # output buffer
    for i in readsec():  # for each pair
        sout.append("".join(i[0]))  # strip out the usernames only and turn them to strings
    return "".join(sout)  # connect all usernames in one long string