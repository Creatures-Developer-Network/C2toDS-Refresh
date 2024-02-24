# Some very ameteur code that really only exists to take the files in
# the dev folder and compile them.

import glob
import os
import re
import struct
import zlib

def pray_write_binary_block(f, block_type, block_name, data):
	assert len(block_type) == 4
	f.write(block_type)
	f.write(block_name.encode('cp1252'))
	f.write(b'\0' * (128 - len(block_name)))
	compressed_data = zlib.compress(data)
	f.write(struct.pack('<III', len(compressed_data), len(data), 1))
	f.write(compressed_data)

def pray_write_tag_block(f, block_type, block_name, tags):
	int_tags = {}
	string_tags = {}
	for k, v in tags.items():
		if isinstance(v, int):
			int_tags[k.encode('cp1252')] = v
		elif isinstance(v, str):
			string_tags[k.encode('cp1252')] = v.encode('cp1252')
		else:
			raise Exception("Bad type for %r=%r: %r" % (k, v, type(v)))
	data = b''
	data += struct.pack('<I', len(int_tags))
	for k, v in sorted(int_tags.items()):
		data += struct.pack('<I', len(k))
		data += k
		data += struct.pack('<I', v)
	data += struct.pack('<I', len(string_tags))
	for k, v in sorted(string_tags.items()):
		data += struct.pack('<I', len(k))
		data += k
		data += struct.pack('<I', len(v))
		data += v
	pray_write_binary_block(f, block_type, block_name, data)

agent_title = "C2 to DS Refresh.agents"
injector_title = "C2 to DS Refresh"
injector_desc = "C2 to DS Refresh!!!" 
agent_animation_file = "blnk.c16"
agent_sprite_first_image = "1"
agent_animation_gallery = "blnk"
web_url = "https://github.com/Creatures-Developer-Network/C2toDS-Refresh/"
web_label = "C2toDS-Refresh on GitHub"

if __name__ == '__main__':
	current_folder = os.path.dirname(os.path.abspath(__file__))

	# list of folders to be merged
	list_dir = ['Backgrounds', 'Images', 'Sounds', 'Scripts', 'Catalogue']
	  
	# enumerate on list_dir to get the 
	# content of all the folders
	dependencies = []
	dependency_basenames = set()
	scripts = []
	for dir in list_dir:
		filenames = glob.glob(os.path.join(current_folder, 'dev', dir, '**', '*'), recursive=True)
		for fname in filenames:
			extname = fname.split('.')[-1].lower()
			if extname in ('cos',):
				scripts.append(fname)
			else:
				basename = os.path.basename(fname).lower()
				# check for non-unique dependency names, which will turn into block names
				if basename in dependency_basenames:
					raise Exception("Non-unique dependency name %r" % fname)
				dependencies.append(fname)
				dependency_basenames.add(basename)

	with open(agent_title, 'wb') as f:
		f.write(b'PRAY')
		tags = {
			'Agent Type': 0,
			'Agent Description': injector_desc,
			'Agent Animation File': agent_animation_file,
			'Agent Sprite First Image': agent_sprite_first_image,
			'Agent Animation Gallery': agent_animation_gallery,
			'Dependency Count': len(dependencies),
			'Script Count': len(scripts),
			'Web URL': web_url,
			'Web Label': web_label
		}
		tags['Remove script'] = ''
		for i, script_filename in enumerate(sorted(scripts), 1):
			with open(script_filename, 'r', newline='\r\n') as script_file:
				script_contents = script_file.read()
			script_name = os.path.relpath(script_filename, current_folder)
			print(script_name)
			# this could be smarter at finding the remove scripts
			normal_script, *remove_scripts = re.split(r'(?m)^\s*rscr[\s$]', script_contents)
			tags['Script %s' % str(i)] = '* %s\r\n' % script_name + normal_script.strip() + '\r\n'
			for r in remove_scripts:
				tags['Remove script'] += '* %s\r\n' % script_name + r.strip() + '\r\n\r\n'

		for i, dep_filename in enumerate(sorted(dependencies), 1):
			print(os.path.relpath(dep_filename, current_folder))
			dep_category = None
			extname = dep_filename.lower().split('.')[-1]
			if extname in ('mng', 'wav'):
				dep_category = 1
			elif extname in ('c16', 's16'):
				dep_category = 2
			elif extname in ('blk',):
				dep_category = 6
			elif extname in ('catalogue',):
				dep_category = 7
			else:
				raise Exception("Unknown dependency category for %r" % dep_filename)

			tags['Dependency %s' % str(i)] = os.path.basename(dep_filename)
			tags['Dependency %s Category' % str(i)] = dep_category

			with open(dep_filename, 'rb') as dep_file:
				dep_data = dep_file.read()
			pray_write_binary_block(f, b'FILE', os.path.basename(dep_filename), dep_data)

		pray_write_tag_block(f, b'DSAG', injector_title, tags)
		
	print("Wrote to file %s" % agent_title)
	input("Press enter to exit")