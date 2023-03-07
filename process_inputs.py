import sys

outfile = sys.argv[1].split(".")

inputfile = open(sys.argv[1],"r")
outfile = open(outfile[0] + "_output.csv","w+")
outfile.write("sgRNAs\n")

checkduplicates = []
forward = 0
reverse = 0
dups = 0

for line in inputfile:
	if line != ">":
		seq = line.strip("\n")
		revstr = ""
		
		for i in range(1,len(seq)+1):
			if seq[len(seq)-i] == "A": revstr = revstr + "T"
			if seq[len(seq)-i] == "C": revstr = revstr + "G"
			if seq[len(seq)-i] == "G": revstr = revstr + "C"
			if seq[len(seq)-i] == "T": revstr = revstr + "A"
		
		seq = seq + seq[0:27]
		revstr = revstr + revstr[0:27]
		
		for i in range(22,len(seq)-5):
			if seq[i] == "G" and seq[i-1] == "G":
				forward += 1
				if seq[i-22:i+1] not in checkduplicates:
					outfile.write(seq[i-22:i+6] + "\n")
				else:
					print("DUPLICATE: " + seq[i-22:i+1])
					dups += 1
				checkduplicates.append(seq[i-22:i+1])
		for i in range(22,len(revstr)-5):
			if revstr[i] == "G" and revstr[i-1] == "G":
				reverse += 1
				if revstr[i-22:i+1] not in checkduplicates:
					outfile.write(revstr[i-22:i+6] + "\n")
				else:
					print("DUPLICATE: " + revstr[i-22:i+1])
					dups += 1
				checkduplicates.append(revstr[i-22:i+1])

print("Forward strand sgRNAs found: " + str(forward))
print("Reverse strand sgRNAs found: " + str(reverse))
print("Total sgRNAs found: " + str(forward+reverse))
print("Total duplicate sites found: " + str(dups))
print("Total unique sgRNAs found: " + str(forward+reverse-dups))

outfile.close()
