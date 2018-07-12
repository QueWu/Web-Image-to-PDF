import subprocess
import sys
import threading

def get(link, startPage, endPage): 
	#link = "https://images.asmhentai.com/002/45068/"
	command1 = "curl -L -H 'Referer: "
	command2 = "nohup wget --referer='"
	suffix = ".jpg"
	#numFormat = "%05d" % (i+startingPage,)
	print("link-->"+link)
	id = link[link.index("0"):-2].replace("/","_")
	print(id)
	subprocess.call("mkdir "+id,shell=True) 
	#subprocess.call("cd "+id,shell=True)
	pages = endPage-startPage+1
	for i in range(pages):
		#finalLink = command2+link+"' "+link+str(startPage)+suffix+" > "+id+"/"+str(i+1)+suffix
		finalLink = command1+link+"1.jpg' "+link+str(startPage)+suffix+" > "+id+"/"+str('%03d' % (i+1))+suffix
		startPage+=1
		print(finalLink)
		subprocess.call(finalLink,shell=True)
	print("finished job: " + id + " with " + str(endPage) + " pages.")

#get(1,30)

queue = ["URL here...", \
		 "URL here...", \
		 "URL here...", \
		 "URL here...", \
		 "URL here..."
		 ] 
pages = [17, 19, 19, 11, 133]

threads = []

if(len(queue)!=len(pages)):
	print("Inconsistent array number")
else:
	#print("in main")
	for i in range(len(queue)):
		main = threading.Thread(target=get, args=(queue[i],1,pages[i]))
		threads.append(main)
		main.start()
