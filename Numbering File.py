import os
enterdir = input ("Please enter your dir: ")
#enterdir = "C:\\Users\\HiFan\\Desktop\\新建文件夹\\ATK\\there"
enterdir = enterdir.replace ("\\", "\\\\")
targetdir = enterdir + "\\\\"
dirlist = os.listdir(targetdir)
#find already numbered files
maxN = 0
for eachfile in dirlist:
    fileAddress = targetdir + eachfile
    index = eachfile.find("._")
    if index != -1:
        try:
            num = int(eachfile[0:index])
        except:
            print("Numbering Err: ", eachfile," ignored.")
            break
        if num > maxN:
            maxN = num
#number rest files
i = maxN + 1
for eachfile in dirlist:
    fileAddress = targetdir + eachfile
    index = eachfile.find("._")
    if index != -1:
        try:
            int(eachfile[0:index])
            continue
        except:
            break
    fileAddressNo = targetdir + str(i)+"._" + eachfile
    os.rename(fileAddress, fileAddressNo)
    i = i+1
print("Complated")    

