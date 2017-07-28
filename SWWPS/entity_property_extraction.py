from operator import itemgetter

def find_compound(idx):
  result = tokens[idx-1]["word"]
  compound = []
  for item in enhancedDependencies:
    if item["dep"] == "compound" and item["governor"] == idx:
      compound.append(item["dependent"])
  for item in sorted(compound, reverse=True):
    result = tokens[idx-1]["word"] + " " + result
  return result

data = {"docDate":"2017-07-28T14:12:28","sentences":[{"index":0,"parse":"(ROOT\r\n  (NP\r\n    (NP (DT the) (NN name))\r\n    (PP (IN of)\r\n      (NP\r\n        (NP (NNP Albert) (NNP Einstein) (POS 's))\r\n        (NN wife)))))","basicDependencies":[{"dep":"ROOT","governor":0,"governorGloss":"ROOT","dependent":2,"dependentGloss":"name"},{"dep":"det","governor":2,"governorGloss":"name","dependent":1,"dependentGloss":"the"},{"dep":"case","governor":7,"governorGloss":"wife","dependent":3,"dependentGloss":"of"},{"dep":"compound","governor":5,"governorGloss":"Einstein","dependent":4,"dependentGloss":"Albert"},{"dep":"nmod:poss","governor":7,"governorGloss":"wife","dependent":5,"dependentGloss":"Einstein"},{"dep":"case","governor":5,"governorGloss":"Einstein","dependent":6,"dependentGloss":"'s"},{"dep":"nmod","governor":2,"governorGloss":"name","dependent":7,"dependentGloss":"wife"}],"enhancedDependencies":[{"dep":"ROOT","governor":0,"governorGloss":"ROOT","dependent":2,"dependentGloss":"name"},{"dep":"det","governor":2,"governorGloss":"name","dependent":1,"dependentGloss":"the"},{"dep":"case","governor":7,"governorGloss":"wife","dependent":3,"dependentGloss":"of"},{"dep":"compound","governor":5,"governorGloss":"Einstein","dependent":4,"dependentGloss":"Albert"},{"dep":"nmod:poss","governor":7,"governorGloss":"wife","dependent":5,"dependentGloss":"Einstein"},{"dep":"case","governor":5,"governorGloss":"Einstein","dependent":6,"dependentGloss":"'s"},{"dep":"nmod:of","governor":2,"governorGloss":"name","dependent":7,"dependentGloss":"wife"}],"enhancedPlusPlusDependencies":[{"dep":"ROOT","governor":0,"governorGloss":"ROOT","dependent":2,"dependentGloss":"name"},{"dep":"det","governor":2,"governorGloss":"name","dependent":1,"dependentGloss":"the"},{"dep":"case","governor":7,"governorGloss":"wife","dependent":3,"dependentGloss":"of"},{"dep":"compound","governor":5,"governorGloss":"Einstein","dependent":4,"dependentGloss":"Albert"},{"dep":"nmod:poss","governor":7,"governorGloss":"wife","dependent":5,"dependentGloss":"Einstein"},{"dep":"case","governor":5,"governorGloss":"Einstein","dependent":6,"dependentGloss":"'s"},{"dep":"nmod:of","governor":2,"governorGloss":"name","dependent":7,"dependentGloss":"wife"}],"tokens":[{"index":1,"word":"the","originalText":"the","characterOffsetBegin":0,"characterOffsetEnd":3,"pos":"DT","before":"","after":" "},{"index":2,"word":"name","originalText":"name","characterOffsetBegin":4,"characterOffsetEnd":8,"pos":"NN","before":" ","after":" "},{"index":3,"word":"of","originalText":"of","characterOffsetBegin":9,"characterOffsetEnd":11,"pos":"IN","before":" ","after":" "},{"index":4,"word":"Albert","originalText":"Albert","characterOffsetBegin":12,"characterOffsetEnd":18,"pos":"NNP","before":" ","after":" "},{"index":5,"word":"Einstein","originalText":"Einstein","characterOffsetBegin":19,"characterOffsetEnd":27,"pos":"NNP","before":" ","after":""},{"index":6,"word":"'s","originalText":"'s","characterOffsetBegin":27,"characterOffsetEnd":29,"pos":"POS","before":"","after":" "},{"index":7,"word":"wife","originalText":"wife","characterOffsetBegin":30,"characterOffsetEnd":34,"pos":"NN","before":" ","after":""}]}]}
sent = "the name of Albert Einstein 's wife"
nmod_of_list = []
nmod_poss_list = []
amod_list = []
ent = []
prop = []

enhancedDependencies = data["sentences"][0]["enhancedDependencies"]
tokens = data["sentences"][0]["tokens"]

for item in enhancedDependencies:
  dep = item["dep"]
  if dep == "nmod:of":
    nmod_of_list.append(item)
    continue
  if dep == "nmod:poss":
    nmod_poss_list.append(item)
    continue
  if dep == "amod":
    amod_list.append(item)

if len(nmod_of_list) > 0:
  nmod_of = sorted(nmod_of_list, key=itemgetter("governor"))[0]
  ent.append(sent[tokens[nmod_of["governor"]-1]["characterOffsetEnd"]+4:])
  prop.append(find_compound(nmod_of["governor"]))
if len(nmod_poss_list) > 0:
  nmod_poss = sorted(nmod_poss_list, key=itemgetter("governor"))[-1]
  ent.append(sent[:tokens[nmod_poss["governor"]-1]["characterOffsetBegin"]-3])
  prop.append(find_compound(nmod_poss["governor"]))
if len(nmod_of_list) == 0 and len(nmod_poss_list) == 0 and len(amod_list) > 0:
  amod = amod_list[0]
  ent.append(sent)
  prop.append(find_compound(amod["governor"]))


print "----------Result----------"
print "Entity(s):"
print ent
print "Property(s):"
print prop