import matplotlib.pyplot as plt
import csv

charts = []
idx = 0

def DictToArray(Dict):
	keys = []
	values = []
	for k in Dict.keys():
		if Dict[k] == 0:
			continue
		keys.append(k)
		values.append(Dict[k])
	return keys, values

def PieChart(title, labels, data):
	global idx

	if len(data) > 10:
		return

	plt.figure(idx)
	idx += 1
	fig, ax = plt.subplots(figsize = (6, 6))
	ax.set_title(title, fontsize = 18)

	ax.pie(data,
		   labels = labels,
		   autopct = '%.1f%%',
		   wedgeprops = {'linewidth': 3.0, 'edgecolor': 'white'},
		   textprops = {'size': 'x-large'})

def BarChart(title, labels, data):
	global idx

	if len(data) > 10:
		return

	x = [i + 1 for i in range(len(labels))]

	plt.figure(idx)
	idx += 1
	fig, ax = plt.subplots(figsize = (6, 6))
	ax.set_title(title, fontsize = 18)

	ax.bar(x,
		   data,
		   tick_label = labels,
		   width = 0.5)

def LineGraph(title, x, y):
	global idx

	plt.figure(idx)
	idx += 1
	fig, ax = plt.subplots(figsize = (6, 6))
	ax.set_title(title, fontsize = 18)

	ax.plot(x, y)

def SparseGraph(title, x, y):
	global idx

	plt.figure(idx)
	idx += 1
	fig, ax = plt.subplots(figsize = (6, 6))
	ax.set_title(title, fontsize = 18)

with open('data.csv', newline = '') as csvfile:
	rows = list(csv.reader(csvfile))

	labels = []
	for l in rows[0]:
		labels.append(l)

	Dict = {}
	for i in range(len(labels)):
		Dict[labels[i]] = {}

	for i in range(1, len(rows)):
		for j in range(len(labels)):
			if not(rows[i][j] in Dict[labels[j]]):
				Dict[labels[j]][rows[i][j]] = 0
			Dict[labels[j]][rows[i][j]] += 1

	# print(Dict['birth_count'])
	# PieChart('sex', Dict['sex'])
	for k in Dict.keys():
		labels, data = DictToArray(Dict[k])
		PieChart(k, labels, data)
		BarChart(k, labels, data)
		LineGraph(k, labels, data)

plt.tight_layout()
plt.show()