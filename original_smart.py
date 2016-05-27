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
	exit(-1)

base64d_password = argv[1]

directory = "/media/john/My Passport1/linux_home/code/cyber/cyberstakes_challenges/breaking_binaries_programs"

files = []
cracked_files = []

commands = []
filename_marker = "<!?filename?!>"
timeout_seconds = '.01'

characters_string = ascii_letters + digits + punctuation
characters_list = [x for x in characters_string]

def generate_garbage():
	shuffle(characters_list)
	garbage = "".join(characters_list)
	garbage = garbage.replace("'","")

	return garbage

def add_stdin_attack():
	info("Adding STDIN attack...")

	for scaled_length_of_buffer in range( 1, 10 ):
		command = 'echo \'' + generate_garbage() * scaled_length_of_buffer + '\' | timeout '+timeout_seconds+'s ./' + filename_marker
		
		#command = 'echo \'' + 'a'*50 * scaled_length_of_buffer + '\' | timeout '+timeout_seconds+'s ./' + filename_marker
		#command = command.replace('"', '\\"')
		#command = 'bash -c "' + command + '"'
		#print command
		commands.append( command )


def add_args_attack():
	info("Adding ARGS attack...")
	for number_of_arguments in range(1, 8):
		command = "timeout "+timeout_seconds+ "s ./" + filename_marker + (" '" + generate_garbage() + "'")*number_of_arguments
		commands.append( command )

def add_integer_attack():
	info("Adding INTEGER attack...")

	for number_of_arguments in range(1, 8):
		command = "timeout "+timeout_seconds+ "s ./" + filename_marker + (" '2147483646'")*number_of_arguments
		command = "timeout "+timeout_seconds+ "s ./" + filename_marker + (" '2147483647'")*number_of_arguments
		command = "timeout "+timeout_seconds+ "s ./" + filename_marker + (" '2147483648'")*number_of_arguments
		commands.append( command )

	for number_of_arguments in range(1, 8):
		command = "timeout "+timeout_seconds+ "s ./" + filename_marker + (" '-2147483646'")*number_of_arguments
		command = "timeout "+timeout_seconds+ "s ./" + filename_marker + (" '-2147483647'")*number_of_arguments
		command = "timeout "+timeout_seconds+ "s ./" + filename_marker + (" '-2147483648'")*number_of_arguments
		commands.append( command )

def add_options_attack():
	info("Adding OPTIONS attack...")
	argument_options = list(itertools.chain.from_iterable( ("-"+x, "--"+x) for x in characters_string))

	for number_of_arguments in range(1, 3):
		
		for option in argument_options:
			arguments = [generate_garbage()]* number_of_arguments
			arguments.append(option)
			for permutation in itertools.permutations(arguments):
				argument_string = "' '".join(permutation)
				argument_string = " '" + argument_string + "' "

				command = "timeout "+timeout_seconds+ "s ./" + filename_marker + argument_string 
				commands.append( command )

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
		success( "Succesfully cleaned dmesg!" )
		pass
	else:
		error( "Error cleaning dmesg!" )


def change_directory():
	info( "cd to " + directory + "...")

	try:
		os.chdir(directory)
	except:
		error( "Error changing into the directory!" )
		warning( "Does '" + directory + "' exist?"  )
		exit(-1)

def test_command( command, filename ):

	current_dmesg = subprocess.check_output("dmesg")

	p = subprocess.Popen(command, shell=True, stderr = subprocess.PIPE, stdout=subprocess.PIPE)	
	new_dmesg = subprocess.check_output("dmesg", shell=True)

	if (new_dmesg != current_dmesg):
		current_dmesg = new_dmesg
		try:
			current_dmesg.index(filename)
			#return True
			return (True, p.stdout.read() + "STDERR:\n" + p.stderr.read() )

		except:
			
			#return False
			return ( False, '' )

	return ( False, '' )	

def load_files():
	global files
	files = glob("*")

def loop():
	global cracked_files, output
	info( "Beginning to loop through all the files...") 

	for filename in files:
		
		if len (filename) != 10: continue; # THIS IS JUST FOR THIS CURRENT TESTING

		for command in commands:	
			command = command.replace( filename_marker, filename)
			
			broke, broken_output = test_command( command, filename )
			if ( broke ):
				cracked_files.append( filename )
				success("Broke " + filename + "! Current count: " + str(len(cracked_files)))
				
				new_command = command.replace( "timeout " + timeout_seconds + "s ", '' )
				broke, broken_output = test_command( new_command, filename )
				print broken_output

				break

	info( "All done looping!" )

def clean_current_setup():

	info( "Cleaning current setup..." )

	global cracked_files, files, commands

	for cracked_file in cracked_files:
		try:
			files.remove(cracked_file)
		except Exception as e:
			error("Something weird happened when cleaning...")
			print e

	commands = []

def main():

	global cracked_files

	info( "Beginning process to break everything..." )
	clean_dmesg()
	change_directory()
	load_files()

	add_stdin_attack()
	loop()
	clean_current_setup()
	add_args_attack()
	loop()
	clean_current_setup()
	add_integer_attack()
	loop()
	clean_current_setup()
	#add_options_attack()
	#loop()

	success( "\nScript complete!\n" )
	print cracked_files

if ( __name__ == "__main__" ):
	main()		