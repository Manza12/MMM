from pathlib import Path

# File
name = 'sonata_16_2nd'  # 'sonata_16', 'hungarian', 'moonlight'
file_path = Path(name + '.xml')

# Change
change = 'major_to_minor'  # 'minor_to_major'

# Paths
input_file = open(file_path, 'r')
output_file = open(Path(name + '_' + change[-5:] + '.xml'), 'w')

# Correspondences
major_to_minor = {
    'I': 'i',
    'ii': 'iiº',
    'IV': 'iv',
    'vi': 'VI',

    'Maj': 'MinH',
}

minor_to_major = {
    'i': 'I',
    'iiº': 'ii',
    'iv': 'IV',
    'VI': 'vi',

    'Np': 'ii',

    'MinH': 'Maj',
    'Min': 'Maj',
}

# Functionality
correspondence = locals()[change]

for line in input_file.readlines():
    new_line = line

    for key, value in correspondence.items():
        new_line = new_line.replace('<degree>' + key + '</degree>', '<degree>' + value + '</degree>')

    output_file.write(new_line)

input_file.close()
output_file.close()
