import csv
import math

# open teh CSV file make an array
def openCSV(file, array):
	with open(file, 'rb') as f:
	    reader = csv.reader(f)
	    for row in reader:
	        array.append(row);

# calculate the feature the sum of abs distance between x's, y's, z's per second, trim ends given array of x,y,z,time
def getFeatureArray(data):
	time_start = int(data[0][3])
	sum_feature = 0
	prev_x = float(data[0][0])
	prev_y = float(data[0][1])
	prev_z = float(data[0][2])
	featue_comp_array = []
	for x,y,z,time in data[1:]:
			sum_feature += abs(float(x) - prev_x) + abs(float(y) - prev_y) + abs(float(z) - prev_z)
			prev_x = float(x)
			prev_y = float(y)
			prev_z = float(z)
			if int(time) > time_start + 1000:
				featue_comp_array.append(sum_feature)
				time_start = int(time)
				sum_feature = 0
	for i in range(5):
		featue_comp_array.pop(0)
	for i in range(5):
		featue_comp_array.pop(len(featue_comp_array) - 1)
	return featue_comp_array

# calculate the mean given array
def mean(data):
	return sum(data) / len(data)

# calculate std given array and mean
def std(data, mean):
	sum_var = 0
	for item in data:
		sum_var += (item - mean)**2
	return (sum_var / (len(data) - 1)) ** .5

# calculate the probability of a mode (running, walking, sitting) given a feature 
def feature_give(mean, std, num):
	return (1.0 / (2.0 * math.pi * std**2) ** 0.5) * math.e**(-(num - mean)**2 / (2.0 * std ** 2))

sitting_array = []
walking_array = []
running_array = []

openCSV('sitting2.csv', sitting_array)
openCSV('walking.csv', walking_array)
openCSV('running.csv', running_array)

trim_feature_sitting = getFeatureArray(sitting_array)
trim_feature_walking = getFeatureArray(walking_array)
trim_feature_running = getFeatureArray(running_array)

mean_sitting = mean(trim_feature_sitting)
mean_walking =  mean(trim_feature_walking)
mean_running = mean(trim_feature_running)

std_sitting = std(trim_feature_sitting, mean_sitting)
std_walking = std(trim_feature_walking, mean_walking)
std_running = std(trim_feature_running, mean_running)

print "mean sit, walk, run"
print mean_sitting
print mean_walking
print mean_running

print "std sit, walk, run"
print std_sitting
print std_walking
print std_running

# mean and std
# mean sitting = 38.4684210526
# mean walking = 268.910131579
# mean running = 810.752207792
# std sitting = 18.0655037057
# std walking = 58.2738178943
# std running = 202.214244784

# assume percent sitting = 65% walking = 25% running = 10%
# posterior(sit) = P(sit)P(feature|sit) / evidence
# posterior(walk) = P(sit)P(feature|walk) / evidence
# posterior(run) = P(sit)P(feature|run) / evidence
# evidence = P(sit)P(feature|sit) + P(walk)P(feature|walk) + P(run)P(feauture|run)
# evidence constant not needed

# testing code
# for item in trim_feature_walking:
# 	walk_num_test = item
# 	feature_given_sit = feature_give(mean_sitting, std_sitting, walk_num_test)
# 	feature_given_walk = feature_give(mean_walking, std_walking, walk_num_test)
# 	feature_given_run = feature_give(mean_running, std_running, walk_num_test)
# 	print feature_given_sit,
# 	print " ",
# 	print feature_given_walk,
# 	print " ",
# 	print feature_given_run