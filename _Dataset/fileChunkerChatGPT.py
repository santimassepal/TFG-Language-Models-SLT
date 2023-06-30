# -*- coding: utf-8 -*-
"""
Created on Sat May 13 19:35:28 2023

@author: Idener
"""
import os


def split_text_file(input_file, output_folder, words_per_file=2000):
    with open(input_file, 'r', encoding="utf-8") as file:
        content = file.read()

    sentences = []
    sentence = ""
    in_quotes = False

    for char in content:
        if char == '"':
            if in_quotes:
                in_quotes = False
                sentences.append(sentence.strip())
                sentence = ""
            else:
                in_quotes = True
        elif in_quotes:
            sentence += char

    file_count = 1
    file_index = 0
    word_count = 0
    output_file = None

    while file_index < len(sentences):
        if word_count + len(sentences[file_index].split()) <= words_per_file:
            if not output_file:
                output_file = open(os.path.join(output_folder, f"file_{file_count}.txt"), 'w', encoding='utf-8')
            output_file.write(sentences[file_index] + '\n')
            word_count += len(sentences[file_index].split())
            file_index += 1
        else:
            output_file.close()
            output_file = None
            word_count = 0
            file_count += 1

    if output_file:
        output_file.close()


input_file_path = 'Seq2Seq20-ENG.csv'  # Path to the input text file
output_folder_path = 'Seq2Seq20-ENG-double-inverted-commas'  # Path to the output folder


if not os.path.exists(output_folder_path):
    os.makedirs(output_folder_path)

split_text_file(input_file_path, output_folder_path)