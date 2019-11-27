from os.path import isfile, join
from os import listdir
import re


def get_files(folder, regex_string='', full_path=True):
    if regex_string != '':
        regex = re.compile(regex_string)
        if full_path:
            files = [join(folder, f) for f in listdir(folder) if isfile(join(folder, f)) and re.match(regex_string, f)]
        else:
            files = [f for f in listdir(folder) if isfile(join(folder, f)) and re.match(regex_string, f)]
    else:
        if full_path:
            files = [join(folder, f) for f in listdir(folder) if isfile(join(folder, f))]
        else:
            files = [f for f in listdir(folder) if isfile(join(folder, f))]
    files = sorted(files)
    return files


def match_files_with_skeleton(frames_nr, file_names):
    new_files = []
    frames_files = []
    for file in file_names:
        # find last occurance of the character "_"
        idx = [m.start() for m in re.finditer('_', file)][-1]
        substr = file[idx:]
        result = re.search('_(.+?).png', substr)
        if result is not None:
            frame = int(result.group(1))
            frames_files.append(frame)
            if frame in frames_nr:
                new_files.append(file)

    return new_files
