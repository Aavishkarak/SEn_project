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
scanner=["accept","input","scan","take from user","take from screen","intake"]
printer=["print", "output", "display"]
arithmetic = ["sum","add","difference","subtract","multiply","product","divide","mod","plus","minus","by","times"]
conditional = ["if","else","otherwise","else if"]

var_names=[]
nam_val=[]
val_exists = []

def quotes(w):
	return('\''+w+'\'')

def addoperator(d):
	return d[0]+"+"+d[1]

def suboperator(d):
	return d[0]+"-"+d[1]

def muloperator(d):
	return d[0]+"*"+d[1]

def divoperator(d):
	return d[0]+"/"+d[1]

def modoperator(d):
	return d[0]+"%"+d[1]	




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

			
def scan(di):
	for (w,t) in nam_val:
		if w in c:
			if t == "int":
				print("scanf(\"%d\",&" + w + ");")
				code_file.write("scanf(\"%d\",&" + w + ");\n")
			elif t == "float":
				print("scanf(\"%f\",&" + w + ");")
				code_file.write("scanf(\"%f\",&" + w + ");\n")
			elif t == "char":
				print("scanf(\"%c\",&" + w + ");")
				code_file.write("scanf(\"%c\",&" + w + ");\n")
			elif t == "long":
				print("scanf(\"%ld\",&" + w + ");")
				code_file.write("scanf(\"%ld\",&" + w + ");\n")
			elif t == "double":
				print("scanf(\"%lf\",&" + w + ");")
				code_file.write("scanf(\"%lf\",&" + w + ");\n")
				
				

				
def prin(di):

	str="printf (\""
	#print(str)
	vars = []

	break_pts = []
	for i in range(len(c)):
		if (c[i] == "plain" and c[i+1] == "text") or (c[i] == "special" and c[i+1] == "character") or c[i] == "variable":
			break_pts.append(i)

	#print(break_pts)
	for i in range(len(break_pts)):
		#print(i)
		#print(c[break_pts[i]])
		if c[break_pts[i]] == "plain":
		 	p = break_pts[i]+2
		 	#print(c[p])
		 	if i < len(break_pts)-1:
		 		#print(i)
		 		#str = str + "\""
		 		while p < break_pts[i+1]:
		 			str = str + c[p] + " "
		 			p = p+1
		 		#str = str + "\""
		 	else:
		 		#str = str + "\""
		 		while p < len(c):
		 			str = str + c[p] + " "
		 			p = p+1
		 		#str = str + "\""
		
		elif c[break_pts[i]] == "variable":
			
			v = c[break_pts[i]+1]

			for (w,t) in nam_val:
				if v == w:
					vars.append(v)
					if t == "int":
						str = str + "%d "
					elif t == "float":
						str = str + "%f "
					elif t == "char":
						str = str + "%c "
					elif t == "long":
						str = str + "%ld "
					elif t == "double":
						str = str + "%lf "

		else:
			p = break_pts[i] + 2
			if c[p] == "tab":
				str = str + "\\t "
			elif c[p] == "space":
				str = str + " "
			else:
				str = str + "\\n"

	str = str + "\""

	for v in vars:
		str = str + "," + v

	str = str + ");"


	print(str)
	code_file.write(str+"\n")
	
	
	
def arithmo(di):
	new_var = []
	inflag = 0
	for index in range(len(c)):
		if c[index] == 'in':
			inflag = 1
			new_index = index+1 
			break

	if inflag == 1:	
		for i in c:
			if i in var_names:
				new_var.append(i)
		new_var.remove(c[new_index])
		#print(new_var)

		if "add" in a or "sum" in a or "plus" in a:
			print(c[new_index]+ "="+ addoperator(new_var)+";")
			code_file.write(c[new_index]+ "="+ addoperator(new_var)+";\n")
		elif "subtract" in a or "difference" in a or "minus" in a:
			print(c[new_index]+ "="+ suboperator(new_var)+";")
			code_file.write(c[new_index]+ "="+ suboperator(new_var)+";\n")
		elif "multiply" in a or "product" in a or "times" in a:
			print(c[new_index]+ "="+ muloperator(new_var)+";")	
			code_file.write(c[new_index]+ "="+ muloperator(new_var)+";\n")	
		elif "divide" in a or "by" in a or "quotient" in a :
			print(c[new_index]+ "="+ divoperator(new_var)+";")	
			code_file.write(c[new_index]+ "="+ divoperator(new_var)+";\n")	
		elif "mod" in a or "modulus" in a or "remainder" in a:
			print(c[new_index]+ "="+ modoperator(new_var)+";")	
			code_file.write(c[new_index]+ "="+ modoperator(new_var)+";\n")
	elif inflag == 0:
		#print("here")
		for index in range(len(c)):
			if c[index] == 'equals' or c[index] == 'equal' :
				#print("her")
				new_index = index-1 

		new_var = var_names.copy()	
		new_var.remove(c[new_index])

		if "add" in a or "sum" in a or "plus" in a:
			print(c[new_index]+ "="+ addoperator(new_var)+";")
			code_file.write(c[new_index]+ "="+ addoperator(new_var)+";\n")
		elif "subtract" in a or "difference" in a or "minus" in a:
			print(c[new_index]+ "="+ suboperator(new_var)+";")
			code_file.write(c[new_index]+ "="+ suboperator(new_var)+";\n")
		elif "multiply" in a or "product" in a or "times" in a:
			print(c[new_index]+ "="+ muloperator(new_var)+";")	
			code_file.write(c[new_index]+ "="+ muloperator(new_var)+";\n")	
		elif "divide" in a or "by" in a or "quotient" in a :
			print(c[new_index]+ "="+ divoperator(new_var)+";")	
			code_file.write(c[new_index]+ "="+ divoperator(new_var)+";\n")	
		elif "mod" in a or "modulus" in a or "remainder" in a:
			print(c[new_index]+ "="+ modoperator(new_var)+";")	
			code_file.write(c[new_index]+ "="+ modoperator(new_var)+";\n")


def condi(di):
	#print("condi")
	for index in range(len(c)):
		if c[index] == 'than':
			first_var = index-2
			if c[index+1] == 'variable':
				second_var = index+2 
			else:
				second_var = index + 1
			break
		elif 'equal' in c[index]:
			first_var = index - 1
			if c[index+2] == 'variable':
				second_var = index+3
			elif c[index+1] == 'variable':
				second_var = index+2
			elif c[index+1] == 'to':
				second_var = index+2
			else:
				second_var = index+1

		

	#print(c)
	print(a)	
	if "greater" in c and "if" in c:
		print("if("+c[first_var] + " " + ">" + " " +c[second_var]+"){\n")
	elif "less" in c and "if" in c:
		print("if("+first_var + " " + "<" + " " +second_var+"){\n")
	elif ("else" in c or "otherwise" in c) :
		print("else{\n")
	elif ("else" in c or "otherwise" in c):
		print("else{\n")
	elif "greater than equal to" in a or "greater than or equal to" in a:
		print("hi")
	elif ("equals" in a or "equal" in a) and "if" in a:
		print("if("+c[first_var] + " " + "==" + " " +c[second_var]+"){\n")

	if "end" in c and "if" in c:
		print("}\n")

for a in lines:
	c = word_tokenize(a.lower())
	st = StanfordPOSTagger('models/english-bidirectional-distsim.tagger')
	b = st.tag(c)

	decflag=0
	iniflag=0
	scanflag=0
	pflag=0
	aflag=0
	
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

	#Printing output to screen
	
	if(decflag == 0 and iniflag == 0):
		for i in dict["NN"] or dict["VB"]:
			for p in printer:
				if p in i:
					pflag = 1
					prin(dict)
					break
			if pflag == 1:
				break

				
	#Scanning input from screen

	
	if(decflag == 0 and iniflag == 0 and pflag == 0):
		for i in dict["VB"] or dict["NN"]:
			for s in scanner:
				if s in i:
					#dict["VB"].remove(i)
					scanflag = 1
					scan(dict)
					break
			if scanflag == 1:
				break
			if scanflag == 0:
				if("take from user" in a or "take from screen" in a or "take in" in a):
					scan(dict)
					scanflag = 1

					
	#arithmetic operations
	if(decflag==0 and iniflag==0 and pflag==0 and scanflag == 0):
		for i in dict["VB"] + dict["NN"] + dict["CC"]:
			
			for a in arithmetic:	
				#print(a,i)
				if a in i:
					aflag = 1
					arithmo(dict)
					break
				if aflag==1:
					break
					
	if(flag == 0):
		
		for i in dict["IN"] + dict["JJ"] + dict["CC"] + dict["RB"]:

			for a in conditional:
				if a in i:
					flag = 1
					
					condi(dict)
					break
				if flag == 1:
					break	

				
code_file.write("\n}")
			
	
