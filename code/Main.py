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

var_names=[]

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

