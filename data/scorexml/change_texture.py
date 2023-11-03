from pathlib import Path

# File
name = 'sonata_16_2nd_arpeggio'
file_path = Path(name + '.xml')

# Change
change = '16_to_24'  # 'minor_to_major'
name += '_' + '24'

# Paths
input_file = open(file_path, 'r')
output_file = open(Path(name + '.xml'), 'w')

# Correspondences

# Loop
den = None
num = None
find_duration = False
for i, line in enumerate(input_file.readlines()):
    # new_line = line
    # re.compile('<degree>(.*?)</degree>')
    # print(line)
    # m = start_tag.match(line)

    # Duration tag
    if find_duration:
        dur_num = int(line.split('num="')[1].split('"')[0])
        dur_den = int(line.split('den="')[1].split('"')[0])

        assert den == 16

        new_end = int((num + dur_num) * 24 / 16)
        new_dur_num = new_end - int(num * 24 / 16)
        new_dur_den = 24

        new_line = line.replace('num="' + str(dur_num) + '"', 'num="' + str(new_dur_num) + '"')
        new_line = new_line.replace('den="' + str(den) + '"', 'den="' + str(new_dur_den) + '"')

        find_duration = False

    if '<start' in line:
        num = int(line.split('num="')[1].split('"')[0])
        den = int(line.split('den="')[1].split('"')[0])
        if den == 16:
            # Start tag
            new_num = int(num * 24 / 16)
            new_den = 24
            new_line = line.replace('num="' + str(num) + '"', 'num="' + str(new_num) + '"')
            new_line = new_line.replace('den="' + str(den) + '"', 'den="' + str(new_den) + '"')
            output_file.write(new_line)
            find_duration = True
        else:
            output_file.write(line)
    else:
        output_file.write(line)


input_file.close()
output_file.close()
