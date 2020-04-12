#osutile for python3

"""A wrapper for various shell based functions found in the os & shutil modules."""

import os
import shutil
import platform
import tarfile
import hashlib
import sys

__author__ = 'RINNE'
__version__ = '0.0.1'
###path  delimite issue
#hostname = _getenv_hostname
#user = _getenv_user
#home = _getenv_home
#PWD = _get_cwd
#dir_s = isdir = os.path.isdir
#file_s = isfile = os.path.isfile
#link_s = islink = os.path.islink
#path_s = ispath = does_this_exist
#ln = os.symlink
#rm mv cp cd ls echo cat targz


def system():
	kernel = platform.system()
	if kernel == 'Linux':
		return 'Linux'
	elif kernel == 'Darwin':
		return 'Mac'
	elif kernel == 'Windows':
		return 'Windows'
	elif kernel.rpartition('-')[0] == 'CYGWIN_NT':
		return 'Cygwin'
	else:
		return 'UNKNOWN'
    
    
def _getenv_hostname():
	return os.getenv('HOSTNAME')


def _getenv_user():
	if system() == 'Windows':
		return os.getenv('USERNAME')
	else:
		return os.getenv('USER')


def _getenv_home():
	if system() == 'Windows':
		return str(os.getenv('HOMEDRIVE') + os.getenv('HOMEPATH')).replace('\\', '/')
	else:
		return os.getenv('HOME')


def _get_cwd():
	# os.getenv('PWD') does not funtion the same as getcwd(). It doesnt seem to respect the cd's.
	return os.getcwd()


def get_hash(target, hashtype='sha1'):

	# Calls hashlib.[md5, sha1, sha224, sha256, sha384, sha512]
	method_to_call = getattr(hashlib, hashtype)
	h = method_to_call(target)
	return h.hexdigest()

hostname = _getenv_hostname
user = _getenv_user
home = _getenv_home
PWD = _get_cwd
dir_s = isdir = os.path.isdir
file_s = isfile = os.path.isfile
link_s = islink = os.path.islink

def does_this_exist(target):
	# Check if the target is a directory
	if isdir(target):
		return True
	else:
		# Check if the target is a file
		if isfile(target):
			return True
		else:
			return False
path_s = ispath = does_this_exist
ln = os.symlink

def mkdir(target, path=True, verbose=False, msg=None):
	if verbose:
		if not type(msg) == str:
			msg = 'Creating: ' + target
		print(msg)

	if path:
		os.makedirs(target)
	else:
		os.mkdir(target)


def rm(target, verbose=False, msg=None):
	if verbose:
		if not type(msg) == str:
			msg = 'Removing: "' + target + '"'
		print(msg)

	if isdir(target):
		shutil.rmtree(target)

	if isfile(target):
		os.remove(target)


def mv(src, dst, verbose=False, msg=None):
	if verbose:
		if not type(msg) == str:
			msg = 'Moving: "' + src + '" to: "' + dst + '"'
		print(msg)

	shutil.move(src, dst)


def cp(src, dst, verbose=False, msg=None):
	if verbose:
		if not type(msg) == str:
			msg = 'Copying: "' + src + '" to: "' + dst + '"'
		print(msg)

	if isdir(src):
		shutil.copytree(src, dst)

	if isfile(src):
		shutil.copy(src, dst)


def cd(dst):
	os.chdir(dst)


def ls(target, show_hidden=False,show_dirs=True, show_files=True):
    
	if not isdir(target):
		raise Exception('target path is not directory')
        
    # Fix path issue
	if not str(target).endswith('/'):
		target += '/'

	# Gets the contents of the specified path
	target_listing = os.listdir(target)

	dirs = []
	files = []
	hdirs = []
	hfiles = []

	# The sorting mechanism
   
	for x in target_listing:
		if isdir(target + x):
			if x.startswith('.'):
				hdirs.append(x)
			else:
				dirs.append(x)
		elif isfile(target + x):
			if x.startswith('.'):
				hfiles.append(x)
			else:
				files.append(x)

	listing = []
	if (show_hidden is False) or show_hidden == 'a':
		pass
	else:
		raise Exception("keyvalue 'show_hidden' should be False or 'a' ")
	if show_dirs and show_hidden == 'a':
		listing += hdirs
	if show_dirs:
		listing += dirs
	if show_files and show_hidden == 'a':
		listing += hfiles
	if show_files:
		listing += files

	return listing


def echo(msg, dst='', append=False):

	if dst == '':
		print(msg)
	else:
		if append:
			mode = 'a'
		else:
			mode = 'w'

		tmp = open(dst, mode)
		tmp.write(msg)
		tmp.close()


def cat(target, aslist=False, strip=True, isurl=False):

	if isurl:
		if sys.version_info.major == 2:
			from urllib import urlopen
		else:
			from urllib.request import urlopen
		f = urlopen(target)
	else:
		f = open(target, 'r')

	s = f.read()

	# if sys.version_info.major == 3:
	# 	s = s.decode()

	if aslist:
		s = s.splitlines()

		if strip:
			for x in s[:]:
				if x == '':
					s.remove(x)
	else:

		if strip:
			s = s.rstrip('\n')
	f.close()

	return s


def targz(target, dst='', extract=False, into=False, verbose=False):

	cwd = _get_cwd() + '/'

	target_fullpath = os.path.abspath(target)
	target_dir = str(target_fullpath.rpartition('/')[2])
	parent_path = str(target_fullpath.rpartition('/')[0]) + '/'

	if dst == '':
		dst = parent_path
	if not dst.endswith('/'):
		dst += '/'

	# TODO: Raise Errors
	# TODO: Loop through to find exact dir that does not exist
	if not does_this_exist(target):
		echo('"' + target_fullpath + '" does not exist!')
		exit()

	if not does_this_exist(dst):
		echo('"' + dst + '" does not exist!')
		exit()

	if not extract:
		# ARCHIVE
		cd(parent_path)
		if verbose:
			echo('Archiving: "' + target_fullpath + '" to "' + dst + target_dir + '.tar.gz"')
		tar = tarfile.open(dst + target_dir + '.tar.gz', 'w:gz')
		tar.add(target_dir)
		tar.close()
	else:
		# EXTRACT
		cd(dst)
		if verbose:
			echo('Extracting: "' + target_fullpath + '" to "' + dst + '"')
		tar = tarfile.open(target_fullpath)

		if not into:
			tar.extractall()
		else:
			for member in tar.getmembers():
				if not member.name == target_dir:  # example.tar.gz is somehow being read as example
					member.name = './' + str(member.name).partition('/')[2]
					tar.extract(member)
		tar.close()
	cd(cwd)