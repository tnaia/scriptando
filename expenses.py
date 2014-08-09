#!/usr/local/bin/python3

# Next:
# - sort lines of output in order of increasing totals (currently it is random)
# - average monthly expenses per category
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
    '''Extract fields, assuning a well-formed line.

    The line would be 

        dd,dd,value,comment

    where `d` means a digit `[0-9]`, value is a simple floating point,
    `[0-9]*` optionally followed by `decimal_separator` and
    `[0-9]*`. Finall, comment is a string with some occurrences of
    `#[^# ]+`.'''

    line = line.strip()
    i = 0
    month = 0
    while line[i] != field_separator:
        month = month * 10 + ord(line[i]) - ord('0')
        i += 1

    i += 1 # get past the comma

    # get past the day field
    while line[i] != field_separator:
        i += 1

    i += 1 # get past the comma

    # obtain the value
    value = 0.0
    while line[i] != field_separator and line[i] != decimal_separator:
        value = 10 * value + ord(line[i]) - ord('0')
        i += 1

    if line[i] == decimal_separator:
        i += 1
        dividend = 10.0
        while line[i] != field_separator:
            value += (ord(line[i]) - ord('0')) / dividend
            dividend *= 10
            i += 1

    i += 1 # get past the comma    

    # obtain the tags
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
# monthly-categories.

fin = open(filename,'r')

monthly_totals = dict()
category_totals = dict()

line_counter = 0
for line in fin:
    line_counter += 1

#    print(monthly_totals,category_totals)
    month, value, tags = extract_fields(line)
#     print(month, value, tags)
    monthly_totals[ month ] = monthly_totals.get(month,0.0) + value
    if not tags:
        print('! warning (line %d): no tags found).' % line_counter)

    for tag in tags:
        aux = category_totals.get(tag,dict())
        aux[month] = aux.get(month,0.0) + value
        category_totals[tag] = aux

# print(monthly_totals)
# print(category_totals)

fin.close()

# print results ############################################
month_values = monthly_totals.keys()

max_category_width = 15
month_col_width = 4 # does not count the space between each column and the next

print (("%" + str(max_category_width) + "s ") % ('months'),end='')

month_names = [ 'jan', 'fev', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec' ]
for month in sorted(month_values):
    print (("%" + str(month_col_width) + "s ") % month_names[month -1], end='')


print( '\n' + '-' * (max_category_width + len(month_values)*(month_col_width + 1)), end='\n')

for category in category_totals.keys():
    print (("%" + str(max_category_width) + "s ") % (category),end='')
    mtot = 0.0
    for month in sorted(month_values):
        v = category_totals[category].get(month,0)
        if v > 0:
            print (("%" + str(month_col_width) + ".0f ") % (v), end='')
            mtot += v
        else:
            print( " " * (month_col_width + 1),end='')
    print((" --> %" + str(month_col_width) + ".0f\n") % mtot,end='')

print('-' * (max_category_width + len(month_values)*(month_col_width + 1)), end='\n')

print(("%" + str(max_category_width) + "s ") % ('totals'),end='')
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
