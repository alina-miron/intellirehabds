from collections import Counter
import os.path


def majority_idx_body(file_name):
    indexes = []
    with open(file_name) as f:
        for line in f.readlines():
            line = line.strip()
            if "Version" in line:
                continue
            words = line.split(",")
            idx_body = int(words[1])
            indexes.append(idx_body)
    # return the most common index
    if len(indexes) == 0:
        return -1
    return Counter(indexes).most_common(1)[0][0]


def load_skeleton(file_name):
    # Find most common body index
    majority_id = majority_idx_body(file_name)
    skeleton_list5d = []
    frames_nr = []

    if majority_id == -1:
        return skeleton_list5d, frames_nr

    line_length = 3 + 25 * 7
    with open(file_name) as f:
        for line in f.readlines():
            line = line.strip()
            if "Version" in line:
                continue
            words = line.split(",")
            frame_nr = int(words[0])
            idx_body = int(words[1])
            # check if this is the body index we are looking for
            if idx_body != majority_id:
                continue
            timestamp = float(words[2])
            joints5d = {}
            # print(line)
            # print(len(words), line_length)
            if len(words) != line_length:
                continue

            for idx in range(25):
                joint_name = words[3 + idx * 7].strip('(')
                joint_tracked = words[3 + idx * 7 + 1]
                joint_x = float(words[3 + idx * 7 + 2])
                joint_y = float(words[3 + idx * 7 + 3])
                joint_z = float(words[3 + idx * 7 + 4])
                if joint_x == 0 and joint_y == 0 and joint_z == 0:
                    joint_dx = 0
                    joint_dy = 0
                else:
                    joint_dx = float(words[3 + idx * 7 + 5])
                    joint_dy = float(words[3 + idx * 7 + 6].strip(')'))
                joints5d[joint_name] = [joint_x, joint_y, joint_z, joint_dx, joint_dy]

            skeleton_list5d.append(joints5d)
            frames_nr.append(frame_nr)

    return skeleton_list5d, frames_nr



