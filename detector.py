from nltk.corpus import wordnet as wn
import nltk
import os

# Processing each metaphor one by one
inp = open( "./input.txt", "r" )    # Input file is input.txt
results_out = open( "./results.txt", "w" )  # Results are stored in results.txt
results_out.write("\n----------------------------\n")

for line in inp:
    line = line[0:-1]
    out = open( "./tempinput.tmp", "w" )    # generating temporary file
    out.write(line)
    out.close()
    os.system("./stanford-parser-full/lexparser.sh tempinput.tmp > tempoutput.tmp")
    
    # Preparing Tag Map for the words (POS tagging)
    words = nltk.word_tokenize(line)
    tags = nltk.pos_tag(words)
    tagmap = {}
    for t, tag in enumerate(tags):
        tagmap[ tag[0]+"-"+str(t+1) ] = tag[1]
    print tagmap
    # Processing output from Stanford parser line by line
    results = open( "./tempoutput.tmp", "r" )
    flag = 0
    metaphor = 0
    maxsim = 0.0	# 0 is considered not metaphor by default ( if maxsim>0 and maxsim<6, then metaphor)
    for result in results:
        result = result[0:-1]	# Removed newline character
        if flag == 0 and result == "":		# Read and empty line (parse tree is over and dependency values are about to begin)
            flag = 1
            continue
        elif flag == 0:	# Reading initial part of Stanford Parser Output (containing parse tree)
            continue
        elif result.startswith("nsubj") or result.startswith("prep_of"):	# Check if required form of Metaphor
            result = result[0:-1]
            temparray = result.split('(')
            temparray = temparray[1].split(', ')
            
            # Check if we have an N-N pair
            if not (tagmap[temparray[0]].startswith('N') and  tagmap[temparray[1]].startswith('N')):
                continue
                            
            temp1 = temparray[0].split('-')
            temp2 = temparray[1].split('-')
            xx = wn.synsets(temp1[0])
            yy = wn.synsets(temp2[0])
            
            # Calculating maximum similarity between synsets
            for x in xx:
                for y in yy:
                    similarity = x.path_similarity(y)
                    if similarity == None:
                        # print "Not similar"
                        continue
                    maxsim = max (similarity, maxsim)
            # results_out.write( temp1[0]+" "+temp2[0]+" "+str(maxsim)+"\n")
            if maxsim>0.0 and maxsim < 0.2:
                metaphor = 1
    if metaphor == 1:
        results_out.write( line+"   : YES" )
    else:
        results_out.write( line+"   : NO" )
    results_out.write("\n\n----------------------------\n\n")
    results_out.flush()
os.remove("./tempoutput.tmp")
os.remove("./tempinput.tmp")
inp.close()
results_out.close()
