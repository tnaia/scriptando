#!/usr/local/bin/python3

# Next:
# - values which are bigger than zero less than one appear as "0"
# - sort lines of output in order of increasing totals (currently it is random)
# - average monthly expenses per tag
# - add option to generate output in csv format
import sys

if len(sys.argv) < 2:
    print ('''Usage: %s filename
    Draws a table of expenses. 
    `filename` is the name of the input file.''' % sys.argv[0])
    exit(-1)
filename = sys.argv[-1]

# Este é um programa para processar nossas despesas.
field_separator = ','
decimal_separator = '.'

def extract_fields(line):
    '''Extract fields, assuming a well-formed line.

    The line would be 

        mm,dd,value,comment

    where `mm` and `dd` are a month and day number, respectively:
    two `[0-9]` digits each. 
    Value is a simple floating point:
      `[0-9]*` optionally followed by `decimal_separator` and
      `[0-9]*`. 
    Finally, comment is a string with some occurrences of `#[^# ]+`.

    Examples
    ========

    extract_fields("12,25,30.45, #food #feast xmas turkey")
      # --> [12, 30.45, ['food', 'feast']]
    extract_fields("01,04,300, #rent") 
      # --> [01, 300, ['rent']]
    extract_fields("13,04,20, #magic") 
      # no checks on weird month values...--> [13, 20, ['magic']] 
    extract_fields("10,10,-20, #breaks") 
      # RRRooAAARRrrr! this breaks, on income as expenses!
    '''

    line = line.rstrip()
    i = 0
    month = 0
    while line[i] != field_separator:
        month = month * 10 + ord(line[i]) - ord('0')
        i += 1

    i += 1 # get past the field_separator

    # get past the day field
    while line[i] != field_separator:
        i += 1

    i += 1 # get past the field_separator

    # obtain the value
    value = 0.0
    while line[i] != field_separator and line[i] != decimal_separator:
        value = 10 * value + ord(line[i]) - ord('0')
        i += 1

    if line[i] == decimal_separator:
        i += 1 # get past the decimal_separator    
        dividend = 10.0
        while line[i] != field_separator:
            value += (ord(line[i]) - ord('0')) / dividend
            dividend *= 10
            i += 1

    i += 1 # get past the field_separator    

    # obtain the tags (eg: food, transport.
    # They appear as `#food #transport#another`)
    tags = []
    l = len(line)
    while i < l:
        if line[i] == '#':
            j = i+1
            while j < l and line[j] != '#' and line[j] != ' ':
                j += 1
            tags += [line[i+1:j]]
            i = j
        else:
            i += 1

    # assemble result
    return [month,value,tags]


# When we process a file, which we'll assume is called `filename`, we
# build two dictionaries. One for the monthly totals, and one of the
# tag-totals.

fin = open(filename,'r')

monthly_totals = dict()
tag_totals = dict()

line_counter = 0
for line in fin:
    line_counter += 1

#    print(monthly_totals,tag_totals)
    month, value, tags = extract_fields(line)
#     print(month, value, tags)
    monthly_totals[ month ] = monthly_totals.get(month,0.0) + value
    if not tags:
        print('! warning (line %d): no tags found).' % line_counter)

    # For each tag, keep a dictionary: keys are months, value is the
    # total expense of the tag in the month. We do essentially
    #
    #     for tag in tags:
    #         tag_totals[tag][month] += value
    #
    for tag in tags:
        aux = tag_totals.get(tag,dict())
        aux[month] = aux.get(month,0.0) + value
        tag_totals[tag] = aux

# print(monthly_totals)
# print(tag_totals)

fin.close()

# print results ############################################
#
# Example table:
#
#              months  jun  jul  aug      total      avg
#     --------------------------------------------------
#           transport   50   50   50   |    150  |    50
#              stamps    0             |      0  |
#                food   72   83   81   |    235  |    78
#                gift        19        |     19  |     6
#              outing        40        |     40  |    33
#     --------------------------------------------------
#              totals  112  164  113

month_values = monthly_totals.keys()

max_tag_width = 15
month_col_width = 4 # does not count the space between each column and the next
tag_tot_width = 5

print (("%" + str(max_tag_width) + "s ") % ('months'),end='')

month_names = [ 'jan', 'fev', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec' ]
for month in sorted(month_values):
    print (("%" + str(month_col_width) + "s ") % month_names[month -1], end='')

print(('%' + str(tag_tot_width + 5) + 's%' + str(month_col_width + 5) + 's') % ("total", "avg"), end='\n')
dash_line_length = max_tag_width + len(month_values)*(month_col_width + 1) +1 + tag_tot_width + 5 + month_col_width + 5
print('-' * dash_line_length, end='\n')

for tag in tag_totals.keys():
    print (("%" + str(max_tag_width) + "s ") % (tag),end='')
    curr_tag_total = 0.0
    for month in sorted(month_values):
        v = tag_totals[tag].get(month,0)
        if v > 0:
            print (("%" + str(month_col_width) + ".0f ") % (v), end='')
            curr_tag_total += v
        else:
            print( " " * (month_col_width + 1),end='')
    print(("  |  %" + str(tag_tot_width) + ".0f") % (curr_tag_total),end='')
    if curr_tag_total/len(month_values) >= 1:
        print(("  |  %" + str(month_col_width) + ".0f\n") % (curr_tag_total/len(month_values)),end='')        
    else:
        print('  |\n',end='')

print('-' * dash_line_length, end='\n')

print(("%" + str(max_tag_width) + "s ") % ('totals'),end='')
for month in sorted(month_values):
    print (("%" + str(month_col_width) + ".0f ") % (monthly_totals[month]), end='')
    
print('\n',end='')

# Tests ####################################################

def check_line(line,ans):
    assert extract_fields(line) == ans

def test_extract_fields():
    cases = [ ['11,22,33,nada  nada tudo', [11,33.0,[]]],
              ['11,22,33,nada #nada #tudo', [11,33.0,['#nada', '#tudo']]],
              ['11,22,2.50,nada#nada#tudo', [11,2.5,['#nada', '#tudo']]]
    ]
    for line,ans in cases:
        yield check_line, line, ans
