from loader import *
def phrase_simai(chart):
    chart = chart.split('\n')
    bpm = 120
    phrasedchart = []
    for bar in chart:
        if 'E' in bar:
            continue
        if '(' in bar and ')' in bar:
            bpm = bar[1:bar.index(')')]
            bar = bar[bar.index(')')+1:]
        
        timesig = bar[bar.index('{')+1:bar.index('}')]
        bar = bar[:bar.index('{')] + bar[bar.index('}')+1:]
        barNumber = 0
        barFraction = 0
        notes = bar.split(',')
        notes = notes[:-1]
        phrasednotes = []
        
        for i in notes:
            isbreak = False
            if 'b' in i:
                isbreak = True
                while True:
                    try:
                        i = i[:i.index('b')] + i[i.index('b')+1:]
                    except:
                        break
            
            if len(i) == 1:
                note = TapNote()
                note.ButtonNumber = i
                note.barNumber = barNumber
                note.barFraction = barFraction
                note.breakNote = isbreak
                phrasednotes.append(note)
            
            if '/' in i and len(i) == 3:
                note = TapNote()
                note.ButtonNumber = i.split('/')[0]
                note.barNumber = barNumber
                note.barFraction = barFraction
                note.breakNote = isbreak
                phrasednotes.append(note)
                note = TapNote()
                note.ButtonNumber = i.split('/')[1]
                note.barNumber = barNumber
                note.barFraction = barFraction
                note.breakNote = isbreak
                phrasednotes.append(note)
            if 'h' in i and not '/' in i:
                note = HoldNote()
                note.ButtonNumber = i[0]
                note.barNumber = barNumber
                note.barFraction = barFraction
                note.divider = i.split(':')[0][-1]
                note.duration = i.split(':')[1][0]
                note.breakNote = isbreak
                phrasednotes.append(note)

            barFraction += 1
            if barFraction == timesig:
                barFraction = 0
                barNumber += 1
        bar = {
            'bpm': int(bpm), #beats per minute, to get time
            'timesig': int(timesig), #number e.g. 4. Fraction is always out of 4 (4)quarter notes so 7 would be 7/4 time signature            
            'notes':phrasednotes, #list type
            }
        phrasedchart.append(bar)
    print(phrasedchart, bpm)
    #print(bpm)
    bar = 1
    lastbar = -1
    chartlist = []

    
    return chartlist



chart = '''(119){1},
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

(phrase_simai(chart))