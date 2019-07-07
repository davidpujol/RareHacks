#the drug used to treat intraocular melanoma is Aldesleukin

import pandas as pd

text_final = ""

for i in range(1,8):
    print("NUM: ",str(i))
    file = pd.read_csv('csv/drugs_labs_biobanks_dataset -'+str(i)+'.csv').values


    names= ['Uveal melanoma','Primary melanoma of the central nervous system', 'Melanoma of soft tissue', 'Diffuse leptomeningeal melanocytosis', 'Melanoma and neural system tumor syndrome', 'Familial atypical multiple mole melanoma syndrome', 'Familial melanoma', 'Malignant melanoma of the mucosa']

    size = len(file[0,:])

    dataset = []
    for j in range(size):
        l = list(filter(lambda x: not pd.isnull(x), file[:,j]))
        dataset.append(l)

    llista=[]

    melanoma = str(names[i-1])

    def medical_name(list):
        slist = []
        if len(list)>0:
            for l in list:
                s1 = "The drug used to treat "+melanoma+" is "+l+"."
                slist.append(s1)
                s2 = "Medicine prescribed for "+melanoma+" is "+l+"."
                slist.append(s2)
        else:
            slist.append("No medical treatment known")
        return slist

    llista.append(medical_name(dataset[0]))

    def brand_name(list):
        slist = []
        if len(list) > 0:
            for l in dataset[0]:
                s1= "The  brand name for " +l+" is "+ list[0]+"."
                s2 = "The drug "+l+" is sold as "+list[0]+"."
                slist.append(s1)
                slist.append(s2)
        else:
            slist.append("There is no consensuate for treating this illness, go to your medical center")
        return slist

    llista.append(brand_name(dataset[1]))

    def drug_side_effects(list):
        slist=[]
        if len(list)>0:
            l = ", ".join(list)
            s1 = "The side effects of the treatment are: "+l+"."
            s2 = "This treatment can cause: "+ l +"."
            slist.append(s1)
            slist.append(s2)
        return slist

    llista.append(drug_side_effects(dataset[2]))
    def dangerous_side_effects(list):
        slist=[]
        if len(list)>0:
            l = ", ".join(list)
            s1 = "If you have one of these side effects, you must go to your medical center: " + l + "."
            s2 = "The following side effects are dangerous, please contact with your doctor: " + l + "."
            slist.append(s1)
            slist.append(s2)
        return slist
    llista.append(dangerous_side_effects(dataset[3]))
    def diagnostic_test(list):
        slist=[]
        l = ", ".join(list)
        s1="The genetic tests for this illness are: "+l+"."
        s2=l+" can be used for doing diagnose."
        slist.append(s1)
        slist.append(s2)
        return slist

    llista.append(diagnostic_test(dataset[14]))
    def patient_organisation(list):
        slist=[]
        l= ",".join(list)
        s1= "You can put in contact with other patients in the following organisations: "+l+"."
        s2 = "The following networks are people like you: "+l+"."
        slist.append(s1)
        slist.append(s2)
        return slist

    llista.append(patient_organisation(dataset[15]))

    def po_link():
        slist=[]
        l = zip(dataset[15],dataset[16])
        for l1,l2 in l:
            s = "This link "+l2+" corresponds to this organization: "+l1+"."
            slist.append(s)
        return slist

    llista.append(po_link())

    def age_onset(list):
        slist=[]
        if len(list) > 0:
            l = ", ".join(list)
            s1 ="The most common age of onset could be: "+l+"."
            s2 = "The first signs appear in "+l+" age."
            slist.append(s1)
            slist.append(s2)
        return slist

    llista.append(age_onset(dataset[17]))

    def prevalence_eu(list):
        slist=[]
        if len(list)>0:
            s="The prevalence of "+melanoma+" in Europe is "+list[0]+"."
            slist.append(s)
        return slist

    llista.append(prevalence_eu(dataset[18]))

    def genes(list):
        slist=[]
        link="https://www.uniprot.org/"
        for g,u in list:
            s="The illness can be caused by a mutation in "+g[0]+" ("+g[1]+"), you can find more information visiting "+link+" using this reference: "+u+"."
            slist.append(s)
        return slist
    if len(dataset[19])>0 and len(dataset[20])>0:
        ls = zip(dataset[19], dataset[20])
        ls = list(zip(ls, dataset[21]))

    llista.append(genes(ls))

    def symptoms(dic):
        #list = [veryfrequent,[l]]
        slist = []
        for (k,v) in dic.items():
            s = k+" symptoms for "+ melanoma +" are: "+", ".join(v)+"."
            slist.append(s)
        return slist

    def symptoms2(l):
        #list = [veryfrequent,[l]]
        slist = []
        s = " symptoms for "+ melanoma +" are: "+", ".join(l)+"."
        slist.append(s)
        return slist

    if size > 24 and len(dataset[24])>0:
        l =list(zip(dataset[23],dataset[24]))

        dic ={}
        for v,k in l:
            if k in dic:
                dic[k].append(v)
            else:
                dic[k]=[v]
        llista.append(symptoms(dic))
    else:
        l = dataset[23]
        llista.append(symptoms2(l))

    ss=""
    for sub in llista:
        for s in sub:
            ss += s + "\n"
    text_final +=ss

f = open("sentences.txt","w")
f.write(text_final)
f.close()

