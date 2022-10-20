import zipfile

with zipfile.ZipFile('../data-20221017T113041Z-005.zip', 'r') as z:
    z.extractall('data2')