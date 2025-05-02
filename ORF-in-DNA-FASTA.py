#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
The goal of this file is to go through a FASTA file
a check for how many records are in it, what is the
longest and shortest records. How many open reading frames
are in each record and for each frame (1,2, or 3)
"""

import os 


os.getcwd()
os.chdir("/Users/ahmedkhair/Desktop/Final Project")

# Part 1
# In this section, I will go through the FASTA file and check for 
# The reads in the file. These can be identefied by checking for the ">"
# Symbol in the file



# This function will list all the sequences stored in a FASTA file and but it
# into a dictionary


#This is the counter for how many reads are in the FASTA file
reads_counter = 0
    
 #This is where I would store the reads and their IDs
reads_dictionary = {}

# Here the length of every record will be stored along its ID
length_dictionary = {}



with open("FASTA_input.fasta.txt", 'r') as fasta_file:
    
    read_id = None
    
    line_sequence = []
    sequence_length = 0
    
    #Looping through the lines in the FASTA file
    for reading_line in fasta_file:
        
        # Removing the new line charechter from the file
        reading_line = reading_line.strip("\n")

        
        # Lines where the ID is will start with ">"
        if reading_line[0] == ">":

            if read_id is not None:

                reads_dictionary[read_id] = ''.join(line_sequence)
                length_dictionary[read_id] = sequence_length

            reads_counter = reads_counter + 1
            
            spilited_read_title = reading_line.split()
            
            read_id = spilited_read_title[0][1:]
            
            line_sequence = []
            sequence_length = 0
            
        
        else:
            
            line_sequence.append(reading_line)

            sequence_length = sequence_length + len(reading_line)

    if read_id is not None:

        reads_dictionary[read_id] = ''.join(line_sequence)
        length_dictionary[read_id] = sequence_length


print(f" There are {reads_counter}  ")




# Part 2

                
# This function will find the longest and shortest sequences
# Also, it will find if there are mutliple sequences that share the 
# shortest and longest lengths


longest_record_length = max(length_dictionary.values())
shortest_record_length = min(length_dictionary.values())

longest_counter = 0
shortest_counter = 0
longest_record_ID = []
shortest_record_ID = []
# This will find the ID of the longest and shortest records

for i in length_dictionary.keys():
    if length_dictionary[i] == longest_record_length:
        longest_record_ID.append(i)
        longest_counter = longest_counter + 1

    elif length_dictionary[i] == shortest_record_length:
        shortest_record_ID.append(i)
        shortest_counter = shortest_counter + 1
    else: 
        pass


print("The longest record is ",longest_record_ID, 'Its lengths is ', longest_record_length)
print("The shortest record is ",shortest_record_ID, 'Its lengths is ', shortest_record_length)




    

# Part 3

# An open reading frame (ORF) is a sequence that contains a starintg codon (ATG)
# and has a stopping codon {TAG, TGA, TAA}
# These open frames have a high chance to code for a protein

# Now I will work on a code that takes the reading frame (1,2, or 3)
# and takes a DNA sequence, and tells if there is an ORF


starting_codon = "ATG"
starting_codon_status = False
starting_codon_position = {}

stop_codon = ["TAA", 'TAG', 'TGA']
stop_codon_status = False

ORF_Dictionary = {}

reading_frame = 3
actual_reading_frame = reading_frame - 1

# note: the code is can correclty store records in dictionaries. Do not test for that again
# This loop will go through the records dictionary   
for checked_record in reads_dictionary.keys():

    with open("The results.txt", 'a') as results_file:
        results_file.write(f"Now we are checking the record {checked_record}\n")
        results_file.write(f"{reads_dictionary[checked_record]}\n")
        results_file.write('__________________________________________________________________\n')


    # This loop will check every record if it contains a starting codon
    for codon_position in range(actual_reading_frame, len(reads_dictionary[checked_record]), 3):

        codon = reads_dictionary[checked_record][codon_position:codon_position + 3]

        with open("The results.txt", 'a') as results_file:
            results_file.write(f"Now we are reading the codon {codon} at position {codon_position} which is in the record {checked_record} of length {len(reads_dictionary[checked_record])}\n")
            results_file.write(f'The status of the starting codon is {starting_codon_status}\n')
            results_file.write(f'The status of the stop codon is {stop_codon_status}\n')


        # This part will be excecuted if the starting codon was found
        # The goal is to find a stop codon if any which will mean the presence of a ORF
        if starting_codon_status == True:

            current_orf += codon


            if codon in stop_codon:
                stop_codon_status = True
                starting_codon_status = False
                ORF_Dictionary[checked_record].append(current_orf)
                
                with open("The results.txt", 'a') as results_file:
                    results_file.write(f"the stop codon was found, the ORF is {current_orf} of length {len(current_orf)}\n")
                    results_file.write("__________________________________________________________________\n")

                current_orf = ''
                stop_codon_status = False


            elif codon not in stop_codon and codon_position >= len(reads_dictionary[checked_record]) - 3:

                starting_codon_status = False
                stop_codon_status = False
                current_orf = ''


        else:

            
        
            # This will be the start of our search for ORF, they start with ATG
            if codon == starting_codon:
                starting_codon_status = True
                stop_codon_status = False
                current_orf = codon
                starting_codon_position[checked_record] = codon_position

                with open("The results.txt", 'a') as results_file:
                    results_file.write(f"The starting codon was found at position, the current ORF is {current_orf}\n")
                    results_file.write("__________________________________________________________________\n")



                
                if checked_record not in ORF_Dictionary:
                    ORF_Dictionary[checked_record] = []
                
                

            else:

                pass


with open("ORF Reads", 'a') as results_file:
            
            for i in ORF_Dictionary.keys():
                results_file.write(f" The record {i} has {len(ORF_Dictionary[i])} ORFs:\n")
                for j in ORF_Dictionary[i]:
                    results_file.write(f"(Length: {len(j)})\n")
                results_file.write("\n")

print(ORF_Dictionary.keys())
print("The loop is done")


        
        
        

with open('Exam answers.txt','a') as exam_answers:

    exam_answers.write(f' The number of reads in the FASTA file is {reads_counter}\n')
    exam_answers.write("__________________________________________________________________\n")
    
    for i in length_dictionary.items():
        exam_answers.write(f' record {i[0]} : Length {i[1]}\n\n')
    
    exam_answers.write(f"The longest reads is {longest_record_ID} and its lenght is {longest_record_length}. There are {longest_counter} records with this length\n")
    exam_answers.write("__________________________________________________________________\n")
    exam_answers.write(f'The shortest reads is {shortest_record_ID} and its length is {shortest_record_length}. There are {shortest_counter} records with this length\n')
    exam_answers.write("__________________________________________________________________\n")
    


