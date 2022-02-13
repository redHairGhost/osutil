# osutil  
now you can use linux command cd, mkdir, rm, mv, cp, ls, echo in python  
it's modified based on other repository  
it requires packages os, shutil, platform, tarfile, hashlib

does_this_exist(target)　　　　//check if the target is a diretory or a file  
　　　　　　　　　　　　　　//If it is, return True, else, return None  
　　　　　　　　　　　　　　//alias with ispath, path_s  
mkdir(target)　　　　　　　　//create target as a diretory   
mkdir(target, True)　　　　　//crete a path, same with "mkdir -P target"  
rm(target)　　　　　　　　　//same with "rm -rf target"  
mv(src, dst)　　　　　　　　//same with 'move src dst'  
cp(src, dst)　　　　　　　　//same with 'cp -r src dst'  
cd(dst)　　　　　　　　　　//cd  
ls(target, show_hidden=False,show_dirs=True, show_files=True　　//same with 'ls target'   

echo(msg)　　　　　　　　　　　　　　　　　　　　　　　　　//same with print(msg)  
echo(msg, dst='filename')　　　　　　　　　　　　　　　　　　// write msg to file 'filename'  
echo(msg, dst='filename', append = True)　　　　　　　　　　　//append msg to file 'filename'  
cat(target, aslist=False, strip=True, isurl=False)  
　　　　　　　　　　　　　　　　　　　　　　　　　　　　　 //aslist: if True, cat file contends into a string; else, a list
　　　　　　　　　　　　　　　　　　　　　　　　　　　　　//strip: strip '\n' or not  
