"""
Module for comparing two python scripts files
Plagiat may be with the 0.9 and upper rate
"""
import argparse
from os.path import exists
import numpy as np


def argument_parser():
    """
    argument parser
    :return: namedtuple with parsed args
    """
    parser = argparse.ArgumentParser(description='command line needed arguments')

    parser.add_argument('input_file', type=str, help='Input file with filenames')
    parser.add_argument('output_file', type=str, help='Output file for results of comparing')
    args = parser.parse_intermixed_args()

    if not exists(args.input_file):
        raise FileNotFoundError("file must to exist")

    with open(args.input_file, encoding="utf-8") as in_file:
        content = in_file.readlines()
        for string in content:
            string.replace("\n", "")
            in_files = string.split()

            if not (exists(in_files[0]) and exists(in_files[-1]) and len(in_files) == 2):
                raise AttributeError("content not in right form")
    return args


def levenshtein(seq1, seq2):
    """
    computate diff between two words
    :param seq1: first word
    :param seq2: second word
    :return: deff by levenstein algo
    """
    size_x = len(seq1) + 1
    size_y = len(seq2) + 1
    matrix = np.zeros((size_x, size_y))

    for tab_row in range(size_x):
        matrix[tab_row, 0] = tab_row
    for tab_col in range(size_y):
        matrix[0, tab_col] = tab_col

    for tab_row in range(1, size_x):
        for tab_col in range(1, size_y):
            if seq1[tab_row - 1] == seq2[tab_col - 1]:
                matrix[tab_row, tab_col] = min(
                    matrix[tab_row - 1, tab_col] + 1,
                    matrix[tab_row - 1, tab_col - 1],
                    matrix[tab_row, tab_col - 1] + 1
                )
            else:
                matrix[tab_row, tab_col] = min(
                    matrix[tab_row - 1, tab_col] + 1,
                    matrix[tab_row - 1, tab_col - 1] + 1,
                    matrix[tab_row, tab_col - 1] + 1
                )

    return matrix[size_x - 1, size_y - 1]


def working_with_content(frst_cont, sec_cont):
    """
    computate diff between two files
    :param frst_cont: first content
    :param sec_cont: second content
    :return: diff between them
    """
    replaceable_symbols = [",", ".", "@", ":", "/", "\n", '"', "'", "<", ">", "!"]

    for rep_sym in replaceable_symbols:
        frst_cont.replace(rep_sym, "")
        sec_cont.replace(rep_sym, "")

    frst_cont = frst_cont.split(" ")
    sec_cont = sec_cont.split(" ")

    first_len = len(frst_cont)
    second_len = len(sec_cont)

    control_sum = max(first_len, second_len) - min(first_len, second_len) + 1
    control_amount = control_sum

    if first_len > second_len:
        up_board = second_len
    else:
        up_board = first_len

    for i in range(0, up_board):
        max_len = max(len(frst_cont[i]), len(sec_cont[i]))
        if max_len == 0:
            max_len = 1
        control_sum += (levenshtein(frst_cont[i], sec_cont[i]) / max_len)
        control_amount += max_len

    return str(1 - control_sum/control_amount) + "\n"


def main():
    """
    main funtion in module
    :return: None
    """
    in_args = argument_parser()
    input_file = in_args.input_file
    output_file = in_args.output_file
    result_comp = []

    with open(input_file, encoding="utf-8") as in_file:
        input_content = in_file.readlines()

    for in_string in input_content:
        in_files = in_string.split()

        with open(in_files[0], encoding="utf-8") as first_file:
            first_content = first_file.readlines()

        with open(in_files[1], encoding="utf-8") as second_file:
            second_content = second_file.readlines()

        result_comp.append(working_with_content("".join(first_content), "".join(second_content)))

    with open(output_file, "w", encoding="utf-8") as output_file:
        output_file.writelines(result_comp)


if __name__ == "__main__":
    main()
