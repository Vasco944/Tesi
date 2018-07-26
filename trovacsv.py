import os
import glob

path = '/home/vasco/Documenti/Script'
extension = 'csv'
os.chdir(path)
result = [i for i in glob.glob('*.{}'.format(extension))]
