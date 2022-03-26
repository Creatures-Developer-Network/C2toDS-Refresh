# Some very ameteur code that really only exists to take the files in
# the dev folder and put them in one folder and generates a "Core Cos"
# so it's easy to compile them with monk.

import shutil, errno, os

agent_title = "C2 to DS Refresh.agents"
injector_title = "C2 to DS Refresh"
injector_desc = "C2 to DS Refresh!!!" 
agent_animation_file = "blnk.c16"
agent_sprite_first_image = "1"
agent_animation_gallery = "blnk"
web_url = "https://github.com/Creatures-Developer-Network/C2toDS-Refresh/"
web_label = "C2toDS-Refresh on GitHub"


if os.path.isdir(os.getcwd() + "/dev"):
	# If the compile dir exists, delete and remake it
	if os.path.isdir(os.getcwd() + "/compile_temp"):
		shutil.rmtree(os.getcwd() + "/compile_temp")
	os.mkdir(os.getcwd() + "/compile_temp")
	
	# dev folder path
	current_folder = os.getcwd() + "/dev"
	  
	# list of folders to be merged
	list_dir = ['Backgrounds', 'Images', 'Sounds', 'Scripts', 'Catalogue']
	  
	# enumerate on list_dir to get the 
	# content of all the folders ans store 
	# it in a dictionary
	content_list = {}
	for index, val in enumerate(list_dir):
		path = os.path.join(current_folder, val)
		content_list[ list_dir[index] ] = os.listdir(path)
	  
	# folder in which all the content will
	# be merged
	merge_folder = os.getcwd() + "/compile_temp"
	 
	  
	# loop through the list of folders
	for sub_dir in content_list:
	  
		# loop through the contents of the 
		# list of folders
		for contents in content_list[sub_dir]:
	  
			# make the path of the content to move 
			path_to_content = sub_dir + "/" + contents  
	  
			# make the path with the current folder
			dir_to_move = os.path.join(current_folder, path_to_content )
	  
			# move the file
			shutil.copy(dir_to_move, merge_folder)
			
	print("Files were copied to /compile_temp")
	
	# Now we gotta write the big pray file
	with open(merge_folder + '/!core.cos', 'w', encoding='utf-8') as f:
		f.write("*# Pray-File \"" + agent_title + "\"\n")
		f.write("*# DS-Name \"" + injector_title + "\"\n")
		f.write("*# desc = \"" + injector_desc + "\"\n")
		f.write("*# Agent Animation File = \"" + agent_animation_file + "\"\n")
		f.write("*# Agent Sprite First Image = \"" + agent_sprite_first_image + "\"\n")
		f.write("*# Agent Animation Gallery = \"" + agent_animation_gallery + "\"\n")
		f.write("*# Web URL = \"" + web_url + "\"\n")
		f.write("*# Web Label = \"" + web_label + "\"\n")
		
		for sub_dir in content_list:
			if sub_dir != "Scripts":
				for contents in content_list[sub_dir]:
					f.write("*# attach " + contents + "\n")
		f.write("*# link ")
		for contents in sorted(content_list["Scripts"]):
			f.write(contents + " ")
	
	print("To complete the compile process, find the file in /compile_temp called \"!core.cos\" and drag it into Monk.")
	print("Make sure 'merge scripts' is UNCHECKED in Monk's edit options")
	print("and that PRAY Chunk is selected")
	print("After compiling the .agents file and moving it out of the folder,")
	print("you may delete the compile_temp folder.\n")
	input("Press enter to exit")
	
else:
	print("Could not find /dev")
	print("Make sure you are running this script from the directory that it is in.")
	input("Press enter to exit")