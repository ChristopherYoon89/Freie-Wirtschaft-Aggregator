# cd C:\Users\User\Documents\Python_Developing\Python\Freie-Wirtschaft-Crawler\


import menu_configuration as MC
import menu_crawling as MCR
import menu_help as MH
import menu_update as MU
from os import system, name




def clear():
    if name == 'nt':
        _ = system('cls') # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')




menu_options = {
    1: 'Crawl websites',
    2: 'Configure bot',
    3: 'Info',
    4: 'Exit program',
}




def print_menu():
    for key in menu_options.keys():
        print (key, '--', menu_options[key] )




def option1():
    clear()
    MCR.crawling_menu()




def option2():
    clear()
    MC.configuration_menu()


def option3():
    clear()
    MU.update_menu()


def option4():
    clear()
    MH.info_menu()


     

clear()


if __name__ == "__main__":
    while(True):

        
        print("""

         

 _______________________________________________________________
|                                                               |
|                  Welcome to Econ Auto Scanner                 |
|                          beta version                         |
|                                                               |
|                        + + + + + + + + +                      |
|                                                               |
|                     developed by Chris Yoon                   |
|                https://www.freie-wirtschaft.org               |
|                                                               |
|_______________________________________________________________|

""")


        print("""        

 _______________________________________________________________
|                                                               |
|                                                               |
|                           MAIN MENU                           | New Version
|                                                               |
|_______________________________________________________________|

""")

            

        print_menu()
        option = ''
        try:
            option = int(input('Enter your choice: '))
        except:
            print('Wrong input. Please enter a number ...')


        if option == 1:
            option1()
        elif option == 2:
            option2()
        elif option == 3:
            option3()
        elif option == 4:
            option4()
        elif option == 5:
            print('Good Bye')
            exit()     
        else:
            clear()
            print('Invalid option. Please enter a number between 1 and 4.')







