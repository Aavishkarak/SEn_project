import nltk
from nltk.tokenize import *
from nltk.corpus import *
#from nltk.tag.stanford import *
from nltk.tag.stanford import StanfordPOSTagger


file = open('dummy.txt', 'r')
dummy= file.read()


lines = dummy.split('\n')

code_file = open('sag.c','a')

code_file.write("#include<stdio.h>\n\n")

code_file.write("main(){\n")

declarations=["declar","creat","tak","mak","consider","new"]
datatypes=["int","char","long","float","double"]
initialize=["giv","initializ","assign"]

var_names=[]
nam_val=[]
val_exists = []

def quotes(w):
	return('\''+w+'\'')

def declare(di):

	dt = ''
	for j in di["NN"] or di["JJ"]:
		
		#comparing to find the datatype
		for d in datatypes:
			if d in j:
				dt = d
				if j in di["NN"]:
					di["NN"].remove(j)
				else:
					di["JJ"].remove(j)
				
				break
		if dt!='':
			break
	if(dt == ''):
		dt = input("Please enter a valid datatype for the variable")
		
	#Variable or array?
	if 'variable' in di["NN"]:
		di["NN"].remove('variable')
	elif 'variable' in di["JJ"]:
		di["JJ"].remove('variable')
	#di["NN"].remove('array')
	
	#print(di)
	#Obtaining the names
	if len(di["NN"]) == 1:
		w = di["NN"][0]
		var_names.append(w)
	
		nam_val.append((w,dt))   
		print(dt+ " " + w+ ";\n")
		code_file.write(dt+ " " + w+ ";\n")
	else:
		w = input("Please give a name for the variable")
		var_names.append(w)
		nam_val.append((w,dt))
		print(dt+ " " + w+ ";")
		code_file.write(dt+ " " + w+ ";\n")
		
		
		
def init(di):
	charflag = 0
	x= '1'
	y= '1'
	for i in c:
		if (i,'char') in nam_val:
			if x=='1':
				charflag = 1
				x = i
			else:
				y = i
				break

		elif i in var_names:
			if x=='1':
				x = i
			else:
				y=i
				break
	for index in range(len(c)):
		if c[index] == 'ascii':
			char_index = index+2 

	if charflag == 1:
		if 'ascii' in a:
		
			print(x + "=" +quotes((c[char_index]))+";" )
			code_file.write(x + "=" +quotes((c[char_index]))+";\n" )

		else:
			if 'to' in c and di["VB"][0] == "assign":
				print(y +" = " + x + ";")
				code_file.write(y +" = " + x + ";\n")
			else:
				print(x +" = " + y + ";")
				code_file.write(x +" = " + y + ";\n")

	elif x == '1' and len(di["CD"]) == 0:
		print ("please first declare this variable")

	elif y == '1':
		
		print(x +" = " + di["CD"][0] + ";")
		code_file.write(x +" = " + di["CD"][0] + ";\n")
	else:
		if 'to' in c and di["VB"][0] == "assign":
			print(y +" = " + x + ";")
			code_file.write(y +" = " + x + ";\n")
		else:
			print(x +" = " + y + ";")
			code_file.write(x +" = " + y + ";\n")		

		

for a in lines:
	c = word_tokenize(a.lower())
	st = StanfordPOSTagger('models/english-bidirectional-distsim.tagger')
	b = st.tag(c)

	decflag=0
	iniflag=0
	
	dict = {"VB": [], "NN": [], "JJ": [], "DT": [], "CC": [], "PR": [], "CD": []}

	for (w,t) in b:
		if (t[:2] in dict):
			dict[t[:2]].append(w)


	#print(dict)


	#checking if the statement is a declaration
	
	for i in dict["VB"]:
		for d in declarations:
			if d in i:
				dict["VB"].remove(i)
				decflag = 1
				declare(dict)
				break
		if decflag == 1:
			break

	#checking if the statement is an initialization
		
	if(decflag == 0):
		for i in dict["VB"]:
			for ini in initialize:
				if ini in i:
					iniflag = 1
					init(dict)
					break
			if iniflag == 1:
				break


				
code_file.write("\n}")
			
	
