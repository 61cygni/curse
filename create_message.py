

#   ____________________
# @=____________________=@
#   \                  \
#   |                  |
#   |                  |
#   | This is a scroll |
#   \__________________\
#  @=__________________=@


def create_scroll (printme) :

    lines = printme.split('\n')
    max_len = 0
    for line in lines:
        if len(line) > max_len :
            max_len = len(line) 

    scroll = []
    scroll.append( "  _"+'_'*max_len+"__")
    scroll.append( "@=_"+'_'*max_len+"__=@")
    scroll.append( "  \\"+' '*max_len+"  \ ")
    scroll.append( "  |"+' '*max_len+"  | ")
    for line in lines:
        scroll.append( "  | "+line+' '*(max_len - len(line))+" | ")
    scroll.append( "  |"+' '*max_len+"  | ")
    scroll.append( "  |"+' '*max_len+"  | ")
    scroll.append( "  \\"+'_'*max_len+"__\ ")
    scroll.append( "@=_"+'_'*max_len+"__=@")
    return scroll

def create_dialog (printme) :

    lines = printme.split('\n')
    max_len = 0
    for line in lines:
        if len(line) > max_len :
            max_len = len(line) 

    dialog = []
    dialog.append( "+-"+'-'*max_len+"-+")
    for line in lines:
        dialog.append( "| "+line+' '*(max_len - len(line))+" |")
    dialog.append( "+-"+'-'*max_len+"-+")
    return dialog
