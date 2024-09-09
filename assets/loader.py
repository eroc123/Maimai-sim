#assets/loader.py
import os
import math

chart = [['note', 0, 0, False, False],['note', 1, 0, False, False],['note', 2, 0 , False, False],['slide', 3, 0, 3, 2, [1,2,3,4,5], False, False],['slide', 3, 0, 3, 3, [1,2,3,4,5], False, False]]

def load(type, chart):
    for i in chart:
        type = i['type']
        if type == 'slide':
            note = [type, i[1], i[2], i[3], i[4], i[5], i[6], i[7]]
        elif type == 'note':
            note = [type, i[1], i[2], i[3]]
        elif type == 'hold':
            note = [type, i[1], i[2], i[3], i[4]]

def save(chart):
    with open('./test.csv', 'w') as f:
        f.write('#Python MAIMAI simulator chart file\n')
        f.write('#Version 0.1 Alpha\n\n')
        for i in chart:
            line = ''
            for j in i[:-1]:
                line += f'{j},'
            line += str(i[-1])
            line += '\n'
            f.write(line)
def open(file):
    with open(file, 'r') as f:
        line = f.readline()
        if f.readline().list()[0] == '#':
            pass
        else:
            pass

'''
[type, bar, bar_fraction, button_start, button_end, duration, [cord], break, double] #slide
[type, bar, bar_fraction, button, break, double] #note
[type, bar, bar_fraction, button, duration, break, double] #hold
'''

def phraseHold(speed : float, button : int, beat : int, duration : float, breaknote, doublenote, timesig , bar) -> list:
    # bolierplate code that hopefully works
    # splits the hold into 3 parts
    # head body and tail
    # head is the start of note
    # body is the note every 0.1 of the duration
    # tail is the ending of the note

    head = ['hold-head', bar, beat , 0, button, breaknote, doublenote]
    body = []

    for i in range(1, int(duration*10)):
        # detect if note goes over one bar
        beatoffset = beat + i/10
        if beatoffset > timesig:
            beatoffset -= int(beatoffset/timesig) + beatoffset % timesig
            baroffset = int(beatoffset/timesig)
        else:
            baroffset = 0
        
        body.append(['hold-body', baroffset, beatoffset, 0, button, breaknote, doublenote])
    
    end = ['hold-end', beat + duration, 0, button, breaknote, doublenote]

    
    
    return head+body+end

def phrase_simai(chart):
    chart = chart.replace('\n','')
    chart = chart.split(',')
    bpm = chart[0].split(')')[0].split('(')[1]
    #print(bpm)
    bar = 1
    lastbar = -1
    chartlist = []
    for i in chart:
        try:
            notefraction = 1/int(i.split('{')[1].split('}')[0])
            #print(notefraction, ' notefraction')
        except IndexError: #shows that there is no {}, therefore no notefraction change
            button = i
            if i == '': #no note, rest
                bar += notefraction
                if bar > lastbar: #new bar
                    lastbar = bar
                continue
            if len(button) > 1: #more than one means its not a single tap note
                if '/' in button:
                    notes = button.split('/')
                    isbreak = False
                    if 'b' in notes[0]:
                        note = ['tap', math.trunc(bar), ((bar - math.trunc(bar))/notefraction), int(notes[0][0])-1, True, True]
                    else:
                        note = ['tap', math.trunc(bar), ((bar - math.trunc(bar))/notefraction), int(notes[0])-1, False, True]
                    if 'b' in notes[1]:
                        note = ['tap', math.trunc(bar), ((bar - math.trunc(bar))/notefraction), int(notes[1][0])-1, True, True]
                    else:
                        note = ['tap', math.trunc(bar), ((bar - math.trunc(bar))/notefraction), int(notes[1])-1, False, True]
                if 'h' in button:
                    holdnote = button.split('h')
                    duration = int(holdnote[1].split(':')[1][0])*int(holdnote[1].split(':')[0][1])
                    note = ['hold', math.trunc(bar), ((bar - math.trunc(bar))/notefraction), int(holdnote[0])-1, duration, False, False]
                chartlist.append(note)
                bar += notefraction
                if bar > lastbar: #new bar
                    lastbar = bar
                continue
            elif button == 'E':
                #print('Finished Chart')
                continue
            elif button == ' ':
                bar += notefraction
                if bar > lastbar: #new bar
                    lastbar = bar
                continue
            else:
                button = int(button)
            
            note = ['tap', math.trunc(bar), (bar - math.trunc(bar))/notefraction, button-1, False, False]
            chartlist.append(note)
            bar += notefraction
            if bar > lastbar: #new bar
                lastbar = bar
        else:
            button = i.split('}')[1]
            if button == '':
                continue
            else:
                if len(button) > 1:
                    continue
                else:
                    button = int(button)
            
            note = ['tap', math.trunc(bar), (bar - math.trunc(bar))/notefraction,  button-1, False, False]
            chartlist.append(note)
            bar += notefraction
            if bar > lastbar: #new bar
                lastbar = bar

    # for i in chartlist:
    #     if i[2] != 0:
    #         i[2] = int(1/i[2])
    #     else:
    #         i[2] = 0
    return chartlist, int(bpm)

chart = '''
(119){1},
{4}3,3,4,4,
{4}5,5,6,,
{4}7,7,8,8,
{4}1,1,2,,
{4}3,3/4,3,3/4,
{4}6,5/6,6,5/6,
{4}4/5,3/6,4/5,3/6,
{4}4/5,3/6,2b/7b,,
{4}5/6,5/6,3/4,3/4,
{4}5/6,3/4,5b/6b,,
{4}3/4,3/4,5/6,5/6,
{4}3/4,5/6,3b/4b,,
{4}6h[4:1],5,6h[4:1],5,
{4}3h[4:1],4,3h[4:1],4,
{4}6h[4:1],5,6h[4:1],5,
{4}3h[4:1],4,4/5,,
{4}7/8,7/8,1/2,1/2,
{4}7/8,1/2,7b/8b,,
{4}1/2,1/2,7/8,7/8,
{4}1/2,7/8,1b/2b,,
{4}7h[4:1],8,7h[4:1],8,
{4}2h[4:1],1,2h[4:1],1,
{4}7h[4:1],8,7h[4:1],8,
{4}2h[4:1],1,1/8,,
{4}3h[4:3],,4,4,
{4}6h[4:3],,5,5,
{4}7h[4:3],,8,8,
{4}2h[4:3],,1,1,
{4}8,8,7,7,
{4}6,6,5,5,
{4}4,4,3,3,
{4}2,2,1h[4:1],8b,
{4}1,2,3,4,
{4}5,6,7,1/8,
{4}8,7,6,5,
{4}4,3,2,1/8,
{4}8,1/7,8,1/7,
{4}1,2/8,1,2/8,
{4}8,1/7,1,2/8,
{4}1/8,2/7,3b/6b,,
{1}3-8[2:1]/4-7[2:1],
{4}1,1,2h[4:1],,
{1}1-6[2:1]/2-5[2:1],
{4}7,7,8h[4:1],,
{4}8,7,6,5,
{4}1,2,3,4,
{4}4/5,3/6,4/5,3/6,
{4}2/7,2/7,2b/7b,,
{4}7/8,1/6,1/2,3/8,
{4}7/8,1/2,7b/8b,,
{4}1/2,3/8,7/8,1/6,
{4}1/2,7/8,1b/2b,,
{4}7h[4:1],8,2h[4:1],1,
{4}7h[4:1],8,2h[4:1],1,
{4}1/8,1/8,2/7,2/7,
{4}1/8,2/7,3b/6b,,
{4}3/4,2/5,5/6,4/7,
{4}3/4,5/6,3b/4b,,
{4}5/6,4/7,3/4,2/5,
{4}5/6,3/4,5b/6b,,
{4}3h[4:1],4,6h[4:1],5,
{4}3h[4:1],4,6h[4:1],5,
{4}4/5,4/5,3/6,3/6,
{4}4/5,3/6,2b/7b,,
{4}8,8,1,1,
{4}2,2,3,,
{4}4,4,5,5,
{4}6,6,7,,
{4}2,1/2,2,1/2,
{4}7,7/8,7,7/8,
{4}1/8,2/7,1/8,2/7,
{4}1/8,2/7,3b/6b,,
{1},
{1},
{1},
E'''

chart, bpm = phrase_simai(chart)
for i in chart:
    print(i)