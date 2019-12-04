# generate an input file containing the structure of a two-level graph
# first line is the number of domains
# next n lines are the number of webpages in each domain
# other lines are links represented in "A B C D" form where A is source's domain, B is source's name, C is destination's domain, and D is destination's name
# for every four intra-domain link generated, one inter-domain link is also generated

from random import randint
import sys

with open("input.txt", "w") as f:
	n = int(sys.argv[1])
	f.write(str(n) + "\n")
	# number of webpages in each domain
	pages = []
	for i in range(n):
		pages.append(randint(n // 2, n // 2 * 3))
		f.write(str(pages[i]) + "\n")
	# generate intra-domain links
	for i in range(n):
		for j in range(2 * pages[i]):
			f.write(str(i) + " " + str(randint(0, pages[i] - 1)) + " ")
			f.write(str(i) + " " + str(randint(0, pages[i] - 1)) + "\n")
	# generate inter-domain links
	for i in range(n * n // 2):
		s = randint(0, n - 1)
		f.write(str(s) + " " + str(randint(0, pages[s] - 1)) + " ")
		d = randint(0, n - 1)
		f.write(str(d) + " " + str(randint(0, pages[d] - 1)) + "\n")