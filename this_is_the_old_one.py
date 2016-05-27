#!/usr/bin/env python

import base64 as b
import subprocess
from colorama import *
import os
from sys import argv, stderr
from glob import glob
from string import ascii_letters, digits, punctuation
from pprint import pprint
from random import shuffle
import itertools


debug = True
init( autoreset = True )


if (debug):

	def success( string ):
		print Fore.GREEN + Style.BRIGHT + "[+] " + string

	def error( string ):
		stderr.write( Fore.RED + Style.BRIGHT + "[-] " + string + "\n" )

	def warning( string ):
		print Fore.YELLOW + "[!] " + string

	def info( string ):
		print argv[0] + ": " + Fore.CYAN + Style.BRIGHT  + string
else:
	def success( string ): pass
	def error( string ): pass
	def warning( string ): pass
	def info( string ): pass

if ( len(argv) == 1 ):
	error("usage: " + argv[0] + " <base64ed password for sudo>")
	warning("If you want this script to clear dmesg for you, supply your password in base64.")
	warning("Or, clear dmesg on your own, and then just give garbage (aaaa) as the argument.")
	exit(-1)

base64d_password = argv[1]

directory = "/media/john/My Passport1/linux_home/code/cyber/cyberstakes_challenges/breaking_binaries_programs"

commands = []
filename_marker = "<!?filename?!>"
timeout_seconds = '.01'

characters_string = ascii_letters + digits + punctuation
characters_list = [x for x in characters_string]

commands_list_filename = '/home/john/commands_list.txt'
commands_list = open(commands_list_filename, 'w')
commands_list.close() # Do this just to clear out the file..

commands_list_filename = 'commands_list.txt'
commands_list = open(commands_list_filename, 'a')
#commands_list.close() # Do this just to clear out the file..

def generate_garbage():
	shuffle(characters_list)
	garbage = "".join(characters_list)
	garbage = garbage.replace("'","")

	return garbage

def create_commands():
	
	# JUST STANDARD INPUT FLOOD YIELDS ~29 CRASHES
	for scaled_length_of_buffer in range( 1, 10 ):
		command = 'echo \'' + generate_garbage() * scaled_length_of_buffer + '\' | timeout '+timeout_seconds+'s ./' + filename_marker
		commands.append( command )
		#commands_list.write(command + "\n")
	

	#  STDIN AND ARGS YIELD ~55 CRASHES
	for number_of_arguments in range(1, 8):
		command = "timeout "+timeout_seconds+ "s ./" + filename_marker + (" '" + generate_garbage() + "'")*number_of_arguments
		commands.append( command )
		#commands_list.write(command + "\n")

	# Integer attack and all others makes ~69 crashes
	for number_of_arguments in range(1, 8):
		command = "timeout "+timeout_seconds+ "s ./" + filename_marker + (" '" + str(2147483647) + "'")*number_of_arguments
		commands.append( command )
		#commands_list.write(command + "\n")

	for number_of_arguments in range(1, 8):
		command = "timeout "+timeout_seconds+ "s ./" + filename_marker + (" '" + str(-2147483647) + "'")*number_of_arguments
		commands.append( command )
		#commands_list.write(command + "\n")

	# I've currently seen up to ~107 crashes with all the above attacks

	'''
	argument_options = list(itertools.chain.from_iterable( ("-"+x, "--"+x) for x in characters_string))

	for number_of_arguments in range(1, 8):
		#garbage = generate_garbage()
		for option in argument_options:
			arguments = [generate_garbage()]* number_of_arguments
			arguments.append(option)
			for permutation in itertools.permutations(arguments):
				argument_string = "' '".join(permutation)
				argument_string = " '" + argument_string + "' "

				command = "timeout "+timeout_seconds+ "s ./" + filename_marker + argument_string 
				#commands.append( command )
				commands_list.write(command + "\n")



	'''
	commands_list.close()

def clean_dmesg():

	info( "Cleaning dmesg..." )
	try:
		command = "echo " + b.b64decode(base64d_password) + " | sudo -S dmesg -c"
	except TypeError as e:
		error( "Error in base64 decoding! Is that the right base64 string?"  )
		warning( str(e) ) 
		exit( -1 )
	subprocess.Popen( command, shell=True, stdout=subprocess.PIPE )
	
	if ( subprocess.check_output("dmesg") != "\n" ):
		#success( "Succesfully cleaned dmesg!" )
		pass
	else:
		error( "Error cleaning dmesg!" )


def change_directory():
	info( "cd to " + directory + "...")

	try:
		os.chdir(directory)
		#success( "Successfully changed into correct directory!" )
	except:
		error( "Error changing into the directory!" )
		warning( "Does '" + directory + "' exist?"  )

def loop():

	info( "Beginning to loop through all the files...") 

	current_dmesg = subprocess.check_output("dmesg")	
	files = glob("*")
	broken = 0
	previous_broken = -1
	for filename in files:

		#if len (filename) != 10: continue; # THIS IS JUST FOR THIS CURRENT TESTING

		new_dmesg = subprocess.check_output("dmesg", shell=True)

		for command in commands:
			command = command.replace( filename_marker, filename)
			subprocess.Popen(command, shell=True, stderr = subprocess.PIPE, stdout=subprocess.PIPE)
			new_dmesg = subprocess.check_output("dmesg", shell=True)

			if (new_dmesg != current_dmesg):
				current_dmesg = new_dmesg
				try:
					current_dmesg.index(filename)
					
					broken += 1
					break
				except:
					
					pass
			if broken != previous_broken:
				success(  str(broken) + "broken!" )
				previous_broken = broken
				

def main():

	info( "Beginning process to break everything..." )

	create_commands()

	clean_dmesg()
	change_directory()
	loop()

	success( "\nScript complete!\n" )

if ( __name__ == "__main__" ):
	main()		