# generate an input file containing the structure of a two-level graph
# first line is the number of domains
# second line is the number of webpages in each domain
# other lines are links represented in "A B C D" form where A is source's domain, B is source's name, C is destination's domain, and D is destination's name
# for every four intra-domain link generated, one inter-domain link is also generated

from random import randint
import sys

with open("input.txt", "w") as f:
	n = int(sys.argv[1])
	nDomains = n
	pagesPerDomain = n
	linksPerDomain = 2 * n
	f.write(str(nDomains) + "\n")
	f.write(str(pagesPerDomain) + "\n")
	for i in range(nDomains):
		for j in range(linksPerDomain):
			f.write(str(i) + " " + str(randint(0, pagesPerDomain - 1)) + " ")
			f.write(str(i) + " " + str(randint(0, pagesPerDomain - 1)) + "\n")
			if j % 4 == 0:
				f.write(str(randint(0, nDomains - 1)) + " " + str(randint(0, pagesPerDomain - 1)) + " ")
				f.write(str(randint(0, nDomains - 1)) + " " + str(randint(0, pagesPerDomain - 1)) + "\n")