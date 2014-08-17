__author__ = 'denislavrov'

import function_sqlite as function  # import my helper functions as a module
function.DATABASE = 'test.db'  # Defining file database file

comList = {  # List of all commands
           'adduser': 'function.adduser()',
           'listuser': 'function.listuser()',
           'rmuser': 'function.rmuser()',
           'login': 'function.login()',
           'logout': "function.logout()",
           'exit': 'exit()',
           'shell': 'function.shell()',
           'createdb': 'function.createdb()',
           'switchdb': 'function.switchdb()',
           'passwd': 'function.passwd()',

}

function.checkdb(function.DATABASE, create=True)
# pre-check on the database just to make sure it exists and everything is fine
try:
    while 1:
        useri = input("#" + function.DATABASE + "#" + function.cUser + ">").lower()
        if useri in comList.keys():
            exec(comList.get(useri))  # Statement to execute user input.
        else:
            print("I accept the following commannds: \n    %s" % '\n    '.join(sorted(comList.keys())))
except KeyboardInterrupt:  # Possible exit handling or just something not to give me errors.
    print("\nY u so mean?\nY u force quit me?\nUse [exit] command next time!")
    exit()