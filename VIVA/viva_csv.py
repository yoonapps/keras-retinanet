import glob
import os
import csv


def extract_box(path):
    """extract_box
    Extract annotation box positions for each labels from VIVA hand dataset.
    output is a list of tuples.

    :param path: text file path
    """

    with open(path) as temp:
        output = []

        for i, line in enumerate(temp):

            if i != 0 and line:
                label, x_1, y_1, x_off, y_off, *_ = line.split()
                pt_1 = (int(x_1), int(y_1))
                pt_2 = (pt_1[0] + int(x_off), (pt_1[1] + int(y_off)))
                output.append((label, pt_1, pt_2))

    return output


def create_csv(data_dir, csv_path):
    images_dir = data_dir + 'pos/'
    annotations_dir = data_dir + 'posGt/'

    image_paths = sorted(glob.glob(images_dir + '*'))
    annotations_paths = sorted(glob.glob(annotations_dir + '*'))

    with open(csv_path, 'w') as csv_file:
        writer = csv.writer(csv_file)
        for image_path, annotations_path in zip(image_paths, annotations_paths):
            annotations = extract_box(annotations_path)
            for annotation in annotations:
                # label, (x1, y1), (x2, y2)
                writer.writerow([image_path,
                                 annotation[1][0], annotation[1][1],
                                 annotation[2][0], annotation[2][1],
                                 annotation[0]])

create_csv('../../datasets/detectiondata/train/', './train_data.csv')
create_csv('../../datasets/detectiondata/test/', './test_data.csv')
