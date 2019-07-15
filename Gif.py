'''
The program make gifs from the jpg files to see how change abundance
of elements with phase. The code shouls be in the same directory, where all
folders with results of analyzing spectra are. Each folder should contain folder
"final" with jpg files named "Starname_Element.jpg". The resuts - gifs - will be
in the folder Elements.gif.
'''
import imageio
import os
if (not os.path.exists('Elements_gif')):
    os.mkdir('Elements_gif')
else:
    os.system('rm Elements_gif/*')
elementNames = []
Phase_data = [[] in range(2)]
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
print(Phase_data)

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
    for file in os.listdir('./Elements_gif'):
        file_name = file.replace('_0.jpg', '')
        file_name = file_name.replace('_1.jpg', '')
        file_name = file_name.replace('_2.jpg', '')
        if file_name == element:
            fileNames.append(file)
    with imageio.get_writer(path, mode='I', duration=Duration) as writer:
        for filename in fileNames:
            full_path = './Elements_gif/' + filename
            image = imageio.imread(full_path)
            writer.append_data(image)
os.system('rm ./Elements_gif/*.jpg')
