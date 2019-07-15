'''
The program make gifs from the jpg files to see how change abundance
of elements with phase. The code shouls be in the same directory, where all
folders with results of analyzing spectra are. Each folder should contain folder
"final" with jpg files named "Starname_Element.jpg". The resuts - gifs - will be
in the folder Elements.gif.
'''
import imageio
import os
import numpy as np
elementNames = []
fileNames = []
with open('input.dat', 'r') as f:
    data = f.readlines()
i = 0
while (i < len(data)):
    if (data[i][0] == "#"):
        del data[i]
    else:
        i += 1
Parametrs = data[0].split()
Name = Parametrs[0]
Duration = Parametrs[1]
Phase_data = [[' ']*2 for i in range(len(data)-1)]
for i in range(1, (len(data))):
    a = data[i].split()
    Phase_data[i-1][0] = a[0]
    Phase_data[i-1][1] = a[1]
Y_min = {}
Y_max = {}

for repeat in range(len(data) - 1):
    path = os.getcwd() + '/' + Phase_data[repeat][0] + '/final'
    for file in os.listdir(path):
        filename = str(file)
        lenth = len(filename)
        if filename[(lenth - 4):(lenth)] == '.gnu':
            full_path = './' + Phase_data[repeat][0] + '/final/' + file
            element = file.replace('.gnu', '')
            element = element.replace('Abun_', '')
            with open(full_path, 'r') as f:
                code = f.readlines()
            for j in range(11, 25):
                if code[3][j] == ':':
                    point1 = j
                if code[3][j] == ']':
                    point2 = j
                    break
            if element in Y_min:
                Y_min[element] = min(float(code[3][11:point1]), Y_min[element])
            else:
                Y_min[element] = float(code[3][11:point1])
            if element in Y_max:
                Y_max[element] = max(float(code[3][(point1+1):point2]), Y_max[element])
            else:
                Y_max[element] = float(code[3][(point1+1):point2])

for repeat in range(len(data) - 1):
    path = os.getcwd() + '/' + Phase_data[repeat][0] + '/final'
    for file in os.listdir(path):
        filename = str(file)
        lenth = len(filename)
        if filename[(lenth - 4):(lenth)] == '.gnu':
            full_path = './' + Phase_data[repeat][0] + '/final/' + file
            element = file.replace('.gnu', '')
            element = element.replace('Abun_', '')
            with open(full_path, 'r') as f:
                code = f.readlines()
            code[3] = 'set yrange[' + str(Y_min[element]) + ':' + str(Y_max[element]) + ']\n'
            limit = Y_max[element] - 0.1*(Y_max[element] - Y_min[element])
            code[16] = "set label 'Phase = " + str(Phase_data[repeat][1]) + "' at -7," + str(limit) + "  font 'Helvetica,20' tc rgb '#4BC87D'\n"
            with open(full_path, 'w') as fr:
                fr.writelines(code)

with open('Do.sh', 'w+') as f:
    for repeat in range(len(data) - 1):
        full_path = os.getcwd() + '/' + Phase_data[repeat][0] + '/final'
        f.write('cd ' + full_path + '\n')
        f.write('./run_gnu.x\n')
        f.write('./runConvert.x\n')
os.system('chmod +x Do.sh')
os.system('./Do.sh')

if (not os.path.exists('Elements_gif')):
    os.mkdir('Elements_gif')
else:
    os.system('rm Elements_gif/*')
elementNames = []
for repeat in range(len(data) - 1):
    path = os.getcwd() + '/' + Phase_data[repeat][0] + '/final'
    for file in os.listdir(path):
        filename = str(file)
        lenth = len(filename)
        if filename[lenth-1] == 'g':
            if filename[lenth-2] == 'p':
                if filename[lenth-3] == 'j':
                    element_name = file.replace('_', '')
                    element_name = element_name.replace(Name, '')
                    element_name = element_name.replace('.jpg', '')
                    if not (element_name in elementNames):
                        elementNames.append(element_name)
                    for i in range(len(data) - 1):
                        command = 'cp ./' + Phase_data[i][0] + '/final/' + file + ' ./Elements_gif/' + element_name + '_' + str(i) + '.jpg'
                        os.system(command)

for element in elementNames:
    path = './Elements_gif/' + element + '.gif'
    fileNames = []
    '''
    for file in os.listdir('./Elements_gif'):
        file_name = file.replace('_0.jpg', '')
        file_name = file_name.replace('_1.jpg', '')
        file_name = file_name.replace('_2.jpg', '')
        if file_name == element:
            fileNames.append(file)
    '''
    for i in range(len(data) - 1):
        full_path = './Elements_gif/' + element + '_' + str(i) + '.jpg'
        if os.path.exists(full_path):
            fileNames.append(full_path)
    print fileNames
    with imageio.get_writer(path, mode='I', duration=Duration) as writer:
        for filename in fileNames:
            image = imageio.imread(filename)
            writer.append_data(image)
os.system('rm ./Elements_gif/*.jpg')
