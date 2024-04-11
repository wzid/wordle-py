import functools
from blessed import Terminal

from word import get_word_of_day

ALPHA = 'abcdefghijklmnopqrstuvwxyz'

def echo(value: str):
    print(value, end='', flush=True)

def main():
    term = Terminal()
    
    setup_menu(term)

    # move to starting spot
    echo(term.move_xy(2, 5))

    with term.cbreak():
        handle_input(term)
                

def setup_menu(term):
    print(term.home + term.clear)
    print(term.white + term.bold + 'wordle-py')
    print(term.normal + term.mediumseagreen + term.italic + 'by cameron')

    print(term.move_down(1) + term.white(term.aquamarine3  + term.bold('Guess the word:')))
    
    # Bold doesn't do anything to these characters but we use it to get a more defined white
    blank_formatting = term.normal + term.white + term.bold
    
    # starts at (x, y) = (2, 5)
    # this is the setup
    print(term.move_right(2) + blank_formatting + '█ '*5)
    for _ in range(5):
        print()
        print(term.move_right(2) + blank_formatting + '□ '*5)

def handle_input(term: Terminal):
    val = ''
    # This is for showing either an error message or a completion message
    showing_msg = False

    finished = False
    while True:
        # Process every 200 ms
        inp_key = term.inkey(timeout=.02)
        
        # If finished then accept no other input unless it is 'q'
        if finished:
            if inp_key == 'q':
                break
            continue

        # If the inp_key is null
        if not inp_key:
            continue

        blank_formatting = term.normal + term.white + term.bold
        # Make sure the key is an alphabetic char and the val string is less than 5 to add a char
        if inp_key in ALPHA and len(val) < 5:
            val += inp_key
            
            # gray1_on_gray100 = black on white
            output = term.normal + term.bold + term.gray1_on_gray100 + inp_key
            if len(val) < 5:
                output += term.normal + ' '
            echo(output)
            
            if showing_msg:
                clear_msg(term)
                showing_msg = False
        elif inp_key.code in (term.KEY_BACKSPACE, term.KEY_DELETE) and len(val) != 0:
            val = val[:-1]
            # This allows us to go back and reset the box we are on
            if len(val) == 4:
                echo(term.move_left(1) + blank_formatting + '█' + term.move_left(1))
            else:
                echo(term.move_left(2) + blank_formatting + '█ ' + term.move_left(2))
            
            if showing_msg:
                clear_msg(term)
                showing_msg = False
        elif inp_key.code == term.KEY_ENTER:
            if showing_msg:
                clear_msg(term)
                showing_msg = False
            
            if len(val) != 5:
                showing_msg = True
                current_loc = term.get_location()
                echo(term.move_xy(0, 17) + term.brown1 + 'Word is incomplete!' + term.move_yx(*current_loc))
            else:
                y_coord = term.get_location()[0]
                
                # Get result string (see handle_submission for formatting of it)
                result = handle_submission(term, val, y_coord)

                if result == 'GGGGG':
                    echo(term.move_xy(0, 17) + term.normal + term.mediumseagreen + 'Congratulations!\nPress \'q\' to exit.')
                    finished = True
                elif y_coord == 15: # This is the y coordinate of the last input box
                    echo(term.move_xy(0, 17) + term.normal + term.rosybrown + 'Better luck next time :(\nPress \'q\' to exit.')
                    finished = True
                else: # Continue onto the next row of input
                    # Set the next row of input to white blocks
                    echo(term.move_xy(2, y_coord + 2) + term.normal + term.white + term.bold + '█ '*5 + term.move_xy(2, y_coord+2))
                    val = ''



# Returns result string
def handle_submission(term: Terminal, submission: str, y_coord : int):
    word_of_day = get_word_of_day()
    
    # will be a combonation of G, Y, N
    # G = Green - correct letter in correct position
    # Y = Yellow - correct letter in wrong position
    # N = None - letter is not in word_of_day
    result = ''

    # make sure we dont double count characters
    visited = []
    for index, c in enumerate(word_of_day):
        submission_ch = submission[index]
        if c == submission_ch:
            result += 'G'
            visited.append(index)
        elif submission_ch in word_of_day:
            # we cant use index because that only gets the index of the first char
            works = False
            for i, ch in enumerate(word_of_day):
                if submission_ch == ch and i not in visited:
                    works = True
                    break
            visited.append(index)
            if works:
                result += 'Y'
        else:
            result += 'N'
    
    # now that we have gathered the result string we need to replace the old one
    output = term.normal + term.bold
    for i, c in enumerate(result):
        match c:
            case 'G':
                output += term.white_on_palegreen4
            case 'Y':
                output += term.white_on_goldenrod
            case 'N':
                output += term.white_on_gray22

        output += submission[i] + term.normal + term.bold + ' '
    
    # set the current row to the correct colors
    echo(term.move_xy(2, y_coord) + output)
    
    # return the result string to see if we have gone to a completion state or not
    return result



def clear_msg(term : Terminal, y_coord=17):
    current_loc = term.get_location()
    # arbitrary value 50
    echo(term.move_xy(0, y_coord) + term.normal + ' '*50 + term.move_yx(*current_loc))


if __name__ == '__main__':
    main()