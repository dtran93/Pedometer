import csv

def openCSV(file, array):
	with open(file, 'rb') as f:
	    reader = csv.reader(f)
	    for row in reader:
	        array.append(row);

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

def mean(data):
	return sum(data) / len(data)

def std(data, mean):
	sum_var = 0
	for item in data:
		sum_var += (item - mean)**2
	return (sum_var / (len(data) - 1)) ** .5

sitting_array = []
walking_array = []
running_array = []
openCSV('sitting.csv', sitting_array)
openCSV('walking.csv', walking_array)
openCSV('running.csv', running_array)
trim_feature_sitting = getFeatureArray(sitting_array)
trim_feature_walking = getFeatureArray(walking_array)
trim_feature_running = getFeatureArray(running_array)

mean_sitting = mean(trim_feature_sitting)
mean_walking =  mean(trim_feature_walking)
mean_running = mean(trim_feature_running)

print mean_sitting
print mean_walking
print mean_running

print std(trim_feature_sitting, mean_sitting)
print std(trim_feature_walking, mean_walking)
print std(trim_feature_running, mean_running)

# assume percent sitting = 65% walking = 25% running = 10%
# posterior(sit) = P(sit)P(feature|sit) / evidence
# posterior(walk) = P(sit)P(feature|walk) / evidence
# posterior(run) = P(sit)P(feature|run) / evidence
# evidence = P(sit)P(feature|sit) + P(walk)P(feature|walk) + P(run)P(feauture|run)

