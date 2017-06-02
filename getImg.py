import subprocess
import sys

def get(call, test, fileName):
	# Preview the resource link and know its naming format e.g img001,img002 etc
	link = "http://images/whatever/F%9D/image"
	# add or adjust different commands as you see fit.
	command1 = "curl -L -H 'Referer: "
	command2 = "nohup wget --referer='"
	suffix = ".jpg"
	pages = 17
	startingPage = 185 # starting page depends on your resource naming format
	# Choose your prefered conversion method.
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

