import re
import os
import sys
import argparse
import configparser
#import paramiko
import ftplib
from datetime import datetime

parser = argparse.ArgumentParser(
                    prog='MoveIt',
                    description='moves completed borrows to NAS'
                    )
parser.add_argument('-contentPath')
parser.add_argument('-contentType')
parser.add_argument('-contentName')
args = parser.parse_args()

scriptLoc = os.path.dirname(os.path.realpath(__file__))

config = configparser.ConfigParser()

config.read(os.path.join(scriptLoc, "config.ini"))


def get_formatted_time():
        return datetime.now().strftime("%Y-%m-%d\t%H:%M:%S")

def write_log(message):
        funcName = sys._getframe(1).f_code.co_name
        with open(os.path.join(scriptLoc, (get_formatted_time().split("\t")[0]) + "MoveLog.log"), "a+")as logfile:
                logfile.write("\t".join([get_formatted_time(), funcName, message]) + "\n")

if args.contentType is None:
	try:
		pattern = re.compile(r"^(?P<title>[-\w'\"]+(?P<separator>[ .])(?:[-\w'\"]+\2)*?)(?:(?:(?!\d+\2)(?:s(?:eason\2?)?)?(?P<season>\d\d?)(?:e\d\d?(?:e?\d\d?)?|x\d\d?)?|(?P<year>[(\]]?\d{4}[)\]]? ))(?=\2) | (?= BOXSET | XVID | DIVX | LIMITED  | UNRATED | PROPER | DTS  | AC3 | AAC | BLU[ -]?RAY | HD(?:TV|DVD) | (?:DVD|B[DR]|WEB)RIP | \d+p |Â [hx]\.?264))", flags= re.I | re.M | re.X)
		regReturn = pattern.search(args.contentName)
		write_log(f"regReturn: {regReturn}")
		write_log(regReturn.groupdict())
		if regReturn is not None:
			if regReturn.groupdict().get('season'):
				contentType = "tv"
			elif regReturn.groupdict().get('year'):
				contentType = "movie"
			else:
				write_log("Not movie or tv, setting ct other")
				contentType = "other"
				write_log(regReturn)
		else:
			write_log("regreturn none, ct to other")
			contentType = "other"
	except Exception as e:
		write_log(f"hit exception {e}\nct to other")
		contentType = "other"
else:
	contentType = args.contentType
filesList = []
if os.path.isfile(args.contentPath):
	filesList.append[args.ContentPath]
else:
	with os.scandir(args.contentPath) as targets:
		for entry in targets:
			filesList.append(entry.path)

write_log(f"Processing type {contentType}")
for file in filesList:
	write_log(file)


def ftp_upload_dir(ftp, source, target):
    if not os.path.isdir(source):
        write_log(f"Source {source} is not a directory")
        raise ValueError(f"Source {source} is not a directory")
    
    def make_dirs(path):
	if dirs.contains('/'):
		sepp = '/'
	elif dirs.contains('\'):
		sepp = '\'
	dirs = path.split(sepp)
        path_to_create = ''
        for dir in dirs:
                write_log(f"Working directory {dir}")
                if dir:
                        path_to_create = f"{path_to_create}{sepp}{dir}" if path_to_create else dir
                        write_log(f"Path to create: {path_to_create}")
                        try:
                            ftp.mkd(path_to_create)
                        except ftplib.error_perm as e:
                            if not e.args[0].startswith('550'):
                                raise
                        try:
                            ftp.cwd(path_to_create)
                            ftp.cwd(sepp)
                        except ftplib.error_perm as e:
                            write_log(f"Failed to change directory to {path_to_create}: {e}")
                            raise
    
    make_dirs(target)

    for item in os.listdir(source):
        write_log(item)
        local_path = os.path.join(source, item)
        remote_path = f"{target}/{item}".replace(os.sep, '/')
        write_log(f"Remote path: {remote_path}")
        if os.path.isfile(local_path):
            with open(local_path, 'rb') as file:
                ftp.storbinary(f'STOR {remote_path}', file)
        elif os.path.isdir(local_path):
            ftp_upload_dir(ftp, local_path, remote_path)

def connect_and_upload_ftp(server, port, username, password, source_dir, target_dir):
    ftp = ftplib.FTP()
    ftp.connect(server, port)
    ftp.login(username, password)
    
    try:
        ftp_upload_dir(ftp, source_dir, target_dir)
    except ftplib.all_errors as e:
        write_log(f"error uploading: {e}")
    finally:
        ftp.quit()

server = config['db']['server']
port = int(config['db']['port'])
username = config['auth']['user']
password = config['auth']['pass']
source_dir = args.contentPath

if contentType == 'movie':
	target_path = config['db']['movie']
elif contentType == 'tv':
	target_path = config['db']['tv']
else:
	target_path = config['db']['other']
target_dir = f"{target_path}{args.contentName}"

connect_and_upload_ftp(server, port, username, password, source_dir, target_dir)






















#sftp.mkdir(target_path, ignore_existing=True)
#sftp.put_dir(contentPath, target_path)
#sftp.close()












#with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "torrentoutput.txt"), "w+") as newfile:
#	newfile.write(f"Path: {args.contentPath}\nType: {args.contentType}")
