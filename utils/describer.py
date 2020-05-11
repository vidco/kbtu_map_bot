actions = ["left", "right", "up_5", "up_4", "up_3", "up_2", "up_1", "up_0", 
			"down_5", "down_4", "down_3", "down_2", "down_1", "down_0"]

def floor_ending(floor):
	if floor == '0':
		return ""
	elif floor == 1:
		return "st"
	elif floor == 2:
		return "nd"
	elif floor == 3:
		return "rd"
	else:
		return "th"

def describe(path):
	last = ""
	path_description = ""
	counter = 1;

	for i in range(len(path)):
		p = path[i];
		if p not in actions:
			if i == 0:
				path_description += "{}. Leave the {} room\n".format(counter, p)
				counter += 1
			elif i == len(path) - 1:
				path_description += "{}. Enter the {} room\n".format(counter, p)
				counter += 1
			else:
				last = p
		else:
			if last != "":
				path_description += "{}. Go through the hall till {} room\n".format(counter, last)
				counter += 1
			
			if p in actions[:2]:
				path_description += "{}. Turn {}\n".format(counter, p)
			else:
				direction, floor = p.split('_')
				path_description += "{}. Go {}stairs to the {}{} floor\n".format(counter, direction, floor, floor_ending(floor))

			counter += 1
			last = ""

	return path_description
