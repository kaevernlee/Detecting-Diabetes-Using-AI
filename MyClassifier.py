import csv
import math
import sys

class Person:
	
	def __init__(self, preg_count, glu_con, blood_press, fold, insulin, mass, d_func, age, is_diabetic = None):
		self.preg_count = preg_count
		self.glu_con = glu_con
		self.blood_press = blood_press
		self.fold = fold
		self.insulin = insulin
		self.mass = mass
		self.d_func = d_func
		self.age = age
		self.is_diabetic = is_diabetic
		self.distance = 0
		self.array = [self.preg_count,self.glu_con,self.blood_press,self.fold,self.insulin,self.mass,self.d_func,self.age]
		
	def set_distance(self, newattribute_array):
		distance = 0
		for i in range(0,len(newattribute_array)):
			distance += (self.array[i] - newattribute_array[i])**2
		distance = math.sqrt(distance)
		self.distance = distance


def knn(base_list,new_list, k):
	for person in new_list:
		update_base(base_list, person.array)
		base_list.sort(key=lambda x: x.distance)
		update_classifier(base_list,new_list,person,k)
	
	for i in range(0, len(new_list)):
		print(new_list[i].is_diabetic)
		
def update_base(base_list,newattribute_array):
	'''Set the distance of each person in the base_list by using the set_distance method each time there is a new input person'''
	
	for person in base_list:
		person.set_distance(newattribute_array)

def update_classifier(base_list,new_list,person,k):
	yes_counter = 0
	no_counter = 0
	
	for i in range(0,k):
		if base_list[i].is_diabetic == 'yes':
			yes_counter+=1
		else:
			no_counter+=1
			
	if yes_counter >= no_counter:
		person.is_diabetic = 'yes'
	else:
		person.is_diabetic = 'no'

def attribute_sd(yes_mean,no_mean,yes_list,no_list):
	
	yes_sd, no_sd = [],[]
	for i in range(0,8):
		sd,sd2 = 0,0
		for person in yes_list:
			sd += (person.array[i]-yes_mean[i])**2
		sd = math.sqrt(sd/float((len(yes_list)-1)))
		yes_sd.append(sd)
		for pers in no_list:
			sd2 += (pers.array[i]-no_mean[i])**2
		sd2 = math.sqrt(sd2/float((len(no_list)-1)))
		no_sd.append(sd2)
	return yes_sd, no_sd
	
def attribute_mean(yes_list,no_list):
	yes_mean, no_mean = [],[]
	for i in range(0,8):
		mean = 0
		mean2 = 0
		for j in range(0, len(yes_list)):
			mean += yes_list[j].array[i]
		yes_mean.append(mean/float(len(yes_list)))
		for z in range(0, len(no_list)):
			mean2 += no_list[z].array[i]
		no_mean.append(mean2/float(len(no_list)))
	return yes_mean, no_mean
		
	
def sort_naive(base_list):
	yes_list = []
	no_list = []
	for person in base_list:
		if person.is_diabetic == 'yes':
			yes_list.append(person)
		else:
			no_list.append(person)
	return yes_list, no_list


def class_prob(mean, std, value):
	second_term = math.exp(-(math.pow(value-mean,2)/(2*math.pow(std,2))))
	first_term = (1/(math.sqrt(2*math.pi)*std))
	final = first_term * second_term
	return final

def nb(base_list, new_list):
	
	yes_list, no_list = sort_naive(base_list)
	yes_mean, no_mean = attribute_mean(yes_list, no_list)
	yes_sd, no_sd = attribute_sd(yes_mean,no_mean,yes_list,no_list)
		
	
	for person in new_list:
		class_prob_yes = 1.0
		class_prob_no = 1.0
		for i in range(0,8):

			class_prob_yes *= class_prob(yes_mean[i],yes_sd[i],person.array[i])
			class_prob_no *= class_prob(no_mean[i],no_sd[i],person.array[i])
		
		class_prob_yes = class_prob_yes * (len(yes_list)/len(base_list))
		class_prob_no = class_prob_no * (len(no_list)/len(base_list))
		
		if class_prob_yes > class_prob_no:
			print("yes")
		else:
			print("no")

def write_10fold(base_list):
	list0,list1,list2,list3,list4,list5,list6,list7,list8,list9 = [],[],[],[],[],[],[],[],[],[]
	big_list = [list0,list1,list2,list3,list4,list5,list6,list7,list8,list9]
	yes_list, no_list = sort_naive(base_list)
	for i in range(0, len(yes_list)):
			mod = i% 10
			big_list[mod].append(yes_list[i])
	for j in range(0,len(no_list)):
		mod2 = (mod +j) %10
		big_list[mod2].append(no_list[j])

		
	with open("pima-folds.csv",'a')as out:
		writer = csv.writer(out)
		for i in range(0,len(big_list)):
			writer.writerow(["fold{}".format(i+1)])
			for person in big_list[i]:
				writer.writerow([person.array[0],person.array[1],person.array[2],person.array[3],person.array[4],person.array[5],person.array[6],person.array[7],person.is_diabetic])
				
			writer.writerow('')


def main():

	base_list = []
	new_list = []


	with open(sys.argv[1]) as csvfile:
		base = csv.reader(csvfile, delimiter = ',')
		for row in base:
			base_list.append(Person(float(row[0]),float(row[1]),float(row[2]),float(row[3]),float(row[4]),float(row[5]),float(row[6]),float(row[7]),row[8]))
	with open(sys.argv[2]) as p:
		new = csv.reader(p, delimiter = ',')
		for row in new:
			new_list.append(Person(float(row[0]),float(row[1]),float(row[2]),float(row[3]),float(row[4]),float(row[5]),float(row[6]),float(row[7])))

	if sys.argv[3][0].upper() == "N":
		nb(base_list, new_list)
	else:
		knn(base_list, new_list, int(sys.argv[3][0]))
	




if __name__ == "__main__":
    main()
