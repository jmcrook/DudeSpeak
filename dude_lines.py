f = open('lebowski.txt', 'r')
out = open('dude_lines.txt', 'w')

is_dude = False
dude_lines = ''
for line in f.readlines():
    if 'DUDE' in line:
        is_dude = True
    elif is_dude:
        if line.isspace():
            is_dude = False
        else:
            out.write(line)

f.close()
out.close()

