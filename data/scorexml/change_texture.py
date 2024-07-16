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
correspondences_16 = {
    0: 0,
    1: 2,
    2: 4,
    3: 5,
}

correspondences_32 = {
    0: 0,
    6: 4,
    7: 5,
}

# Loop
# den = None
# num = None
num_sta = None
new_num_sta = None

find_duration = False
for i, line in enumerate(input_file.readlines()):
    # Start tag
    if '<start' in line:
        num_sta = int(line.split('num="')[1].split('"')[0])
        den = int(line.split('den="')[1].split('"')[0])

        if den == 16:
            offset = num_sta // 4
            value = num_sta % 4

            new_num_sta = correspondences_16[value] + offset * 6
            new_den = 24

            new_line = line.replace('num="' + str(num_sta) + '"', 'num="' + str(new_num_sta) + '"')
            new_line = new_line.replace('den="' + str(den) + '"', 'den="' + str(new_den) + '"')

            find_duration = True
        elif den == 32:
            offset = num_sta // 8
            value = num_sta % 8

            new_num_sta = correspondences_32[value] + offset * 6
            new_den = 24

            new_line = line.replace('num="' + str(num_sta) + '"', 'num="' + str(new_num_sta) + '"')
            new_line = new_line.replace('den="' + str(den) + '"', 'den="' + str(new_den) + '"')

            find_duration = True
        else:
            new_line = line

    # Duration tag
    elif '<duration' in line:
        if find_duration:
            num_dur = int(line.split('num="')[1].split('"')[0])
            den = int(line.split('den="')[1].split('"')[0])

            new_den = 24

            num_end = num_sta + num_dur

            if den == 16:
                correspondences = correspondences_16
                offset = num_end // 4
                value = num_end % 4
            elif den == 32:
                correspondences = correspondences_32
                offset = num_end // 8
                value = num_end % 8
            else:
                raise ValueError('Correspondences not found for den = ' + str(den))

            try:
                new_num_end = correspondences[value] + offset * 6
                new_num_dur = new_num_end - new_num_sta
            except KeyError:
                raise KeyError('Value %d not found in correspondences %d' % (value, den))

            new_line = line.replace('num="' + str(num_dur) + '"', 'num="' + str(new_num_dur) + '"')
            new_line = new_line.replace('den="' + str(den) + '"', 'den="' + str(new_den) + '"')

            find_duration = False
        else:
            new_line = line
    else:
        new_line = line

    # Write line
    output_file.write(new_line)


input_file.close()
output_file.close()
