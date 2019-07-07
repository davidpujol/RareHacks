#the drug used to treat intraocular melanoma is Aldesleukin

import pandas as pd
file = pd.read_csv('drugs_labs_biobanks_dataset.csv').values

names = file[:,0]
dataset = []
for i in range(23):
    l = list(filter(lambda x: not pd.isnull(x), file[:,i]))
    dataset.append(l)



melanoma = "intraocular melanoma"

def medical_name(list):
    slist = []
    for l in list:
        s1 = "The drug used to treat "+melanoma+" is "+l+"."
        slist.append(s1)
        s2 = "Medicine prescribed for "+melanoma+" is "+l+"."
        slist.append(s2)
    return slist

print(medical_name(dataset[0]))

def brand_name(list):
    slist = []
    for l in dataset[0]:
        s1= "The  brand name for " +l+" is "+ list[0]+"."
        s2 = "The drug "+l+" is sold as "+list[0]+"."
        slist.append(s1)
        slist.append(s2)
    return slist

print(1,brand_name(dataset[1]))

def drug_side_effects(list):
    slist=[]
    l = ", ".join(list)
    s1 = "The side effects of the treatment are: "+l+"."
    s2 = "This treatment can cause: "+ l +"."
    slist.append(s1)
    slist.append(s2)
    return slist

print(2,drug_side_effects(dataset[2]))
def dangerous_side_effects(list):
    slist=[]
    l = ", ".join(list)
    s1 = "If you have one of these side effects, you must go to your medical center: " + l + "."
    s2 = "The following side effects are dangerous, please contact with your doctor: " + l + "."
    slist.append(s1)
    slist.append(s2)
    return slist
print(3,dangerous_side_effects(dataset[3]))
def diagnostic_test(list):
    slist=[]
    l = ", ".join(list)
    s1="The genetic tests for this illness are: "+l+"."
    s2=l+" can be used for doing diagnose."
    slist.append(s1)
    slist.append(s2)
    return slist

print(4,diagnostic_test(dataset[14]))
def patient_organisation(list):
    slist=[]
    l= ",".join(list)
    s1= "You can put in contact with other patients in the following organisations: "+l+"."
    s2 = "The following networks are people like you: "+l+"."
    slist.append(s1)
    slist.append(s2)
    return slist

print(5,patient_organisation(dataset[15]))

def po_link(list):
    slist=[]
    l = zip(dataset[15],dataset[16])
    for l1,l2 in l:
        s = "This link "+l2+" corresponds to this organization: "+l1+"."
        slist.append(s)
    return slist

print(6,po_link(dataset[16]))

def age_onset(list):
    slist=[]
    if len(list) > 0:
        l = ", ".join(list)
        s1 ="The most common age of onset could be: "+l+"."
        s2 = "The first signs appear in "+l+" age."
        slist.append(s1)
        slist.append(s2)
    return slist

print(7,age_onset(dataset[17]))

def prevalence_eu(list):
    slist=[]
    if len(list)>0:
        s="The prevalence of "+melanoma+" in Europe is "+list[0]+"."
        slist.append(s)
    return slist

print(8,prevalence_eu(dataset[18]))

def genes(list):
    slist=[]
    link="https://www.uniprot.org/"
    for g,s,u in list:
        s="The illness can be caused by a mutation in "+g+" ("+s+"), you find more information visiting "+link+" using this reference: "+u+"."
        slist.append(s)
    return slist

ls = zip(dataset[19],dataset[20])

ls = list(zip(ls,dataset[21]))

print(ls)
print(9,genes(ls))

def symptoms(list):
    #list = [veryfrequent,[l]]
    slist = []
    for sy,f in list:
        s = f+"symptoms are: " +", ".join(sy)+"."
        slist.append(s)
    return slist

print(10,symptoms(dataset[23:24]))