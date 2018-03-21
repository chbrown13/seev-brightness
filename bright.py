from PIL import Image
import csv
import math
import numpy
import os

PATCH = 20
DIR = "./"
R = 0.2126
G = 0.7152
B = 0.0722

def write(pid, frame, file, array): 
	output = csv.writer(open(file + "_{n}.csv".replace("{n}", str(PATCH)), 'w'))
	output.writerow(['pptID', 'FrameNum', 'FileName', 'Location', 'Brightness'])
	for x in range(len(array)):
		for y in range(len(array[x])):
			output.writerow([pid, frame, file, '{x},{y}'.replace("{x}", str(x + 1)).replace("{y}", str(y + 1)), array[x][y]])

def main():
	for f in os.listdir(DIR):
		if f.endswith(".jpg"):
			filename = f.replace(".jpg", "")
			frame = filename.split("_")[-1]
			ppt_id = filename.split("_")[-3]
			img = Image.open(f)
			img = img.convert('RGB')
			width, height = img.size #1280, 720
			pixels = list(img.getdata())
			pixs = numpy.array(pixels).reshape((width, height, 3));
			x, y = 0, 0
			brights = [[0 for w in range(width/PATCH)] for h in range(height/PATCH)]
			for i in range(width):
				y = 0
				if (i) % PATCH == 0 and i > 0:
					x += 1
				for j in range(height):
					if (j) % PATCH == 0 and j > 0:
						y += 1
					r, g, b = pixs[i][j]
					brights[y][x] += (r * R + g * G + b * B)/(PATCH*PATCH)
			write(ppt_id, frame, filename, brights)
	

if __name__=="__main__":
	main()
