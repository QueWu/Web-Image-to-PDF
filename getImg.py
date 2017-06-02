import subprocess
import sys

def get(call, test, fileName):
	link = "http://images.dmzj.com/b/%E5%BF%85%E7%84%B6%E6%80%A7%E6%8C%87%E5%8D%97%EF%BD%9E%E7%A5%9E%E6%98%8E%E4%BB%AC%E7%9A%84%E6%81%8B%E7%88%B1%E4%BB%A3%E7%90%86%EF%BD%9E/%E7%AC%AC03%E8%AF%9D/image"
	command1 = "curl -L -H 'Referer: "
	command2 = "nohup wget --referer='"
	suffix = ".jpg"
	pages = 17
	startingPage = 185
	compilePDF = "convert *"+suffix+" "+fileName+".pdf"
	imgStat = False
	for i in range(pages):
		numFormat = "%05d" % (i+startingPage,)
		finalLink = link + numFormat + suffix
		if(call == "curl"):
			line = command1+finalLink+"' "+finalLink+" > "+numFormat+suffix
		elif(call == "wget"):
			line = command2+finalLink+"' "+finalLink+" > "+numFormat+suffix
		elif(call != "curl" and call != "wget"):
			print("Incorrect command argument.")

		if(test == ""):
			subprocess.call(line,shell=True)
			imgStat = True
		elif(test == "test"):
			print(line)
			if(i==227):
				print(compilePDF)
		elif(test != "" and test != "test"):
			print("Incorrect test argument.")
			break
		
	if(imgStat == True):
			subprocess.call(compilePDF,shell=True)
			subprocess.call("rm *"+suffix,shell=True)
	return line

if __name__=="__main__":
	if(len(sys.argv) == 4):
		get(sys.argv[1], sys.argv[2], sys.argv[3])
	elif(len(sys.argv)<3 or len(sys.argv)>4):
		print("Incorrect number of arguments, takes 2.")
	else:
		get(sys.argv[1], "", sys.argv[2])

