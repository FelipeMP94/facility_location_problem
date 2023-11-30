import numpy as np
import nltk


class TSCFLPinstance():
    def __init__(self,path):
        
        #Extraindo parâmetros
        self.path = path
        self.parameters = np.array([],dtype= int)
        arq = open(self.path)
        self.data = arq.readlines()
        extracted_param =nltk.word_tokenize(self.data.pop(0))
        for e in extracted_param:
            self.parameters = np.append(self.parameters,int(e))
        
        
        #Dados da instância
        self.demanda_clientes = np.array([],dtype= int)
        self.demanda_total = 0
        self.plant_capacity = np.array([],dtype= int)
        self.plant_fxcost =  np.array([],dtype= int)
        self.cost_plant_satelite =  np.zeros((self.parameters[0],self.parameters[1]),dtype= int)
        self.stelite_capacity = np.array([],dtype = int)
        self.stelite_fxcost = np.array([],dtype = int)
        self.cost_satelite_custumer = np.zeros((self.parameters[1],self.parameters[2]),dtype= int)
          
        j = 0
        k = 0
        for i in np.arange(len(self.data)):
            if i < self.parameters[2]:
                self.demanda_clientes =  np.append(self.demanda_clientes,int(self.data[i]))  
                self.demanda_total += int(self.data[i])

            if i >= self.parameters[2] and i< self.parameters[2]+self.parameters[0]:
                tokenized_fxcos_capacity = nltk.word_tokenize(self.data[i])
                self.plant_capacity = np.append(self.plant_capacity,int(tokenized_fxcos_capacity[0]))
                self.plant_fxcost = np.append(self.plant_fxcost,int(tokenized_fxcos_capacity[1]))

            if i >= self.parameters[2]+self.parameters[0] and i < self.parameters[2]+self.parameters[0]+ self.parameters[0]:
                tokenized_cos_plant_satelite = nltk.word_tokenize(self.data[i])
                tokens_to_int = np.array([int(val) for val in tokenized_cos_plant_satelite])
                self.cost_plant_satelite[j] = self.cost_plant_satelite[j] + tokens_to_int
                j+=1

            if i>=self.parameters[2]+self.parameters[0]+ self.parameters[0] and i<self.parameters[2]+self.parameters[0]+ self.parameters[0]+self.parameters[1]:
                tokenized_fxcos_capacity = nltk.word_tokenize(self.data[i])
                self.stelite_capacity = np.append(self.stelite_capacity,int(tokenized_fxcos_capacity[0]))
                self.stelite_fxcost = np.append(self.stelite_fxcost,int(tokenized_fxcos_capacity[1]))


            if i>=self.parameters[2]+self.parameters[0]+ self.parameters[0]+self.parameters[1] and i<self.parameters[2]+self.parameters[0]+ self.parameters[0]+self.parameters[1]+self.parameters[1]:
                tokenized_cos_satelite_custumer = nltk.word_tokenize(self.data[i])
                tokens_to_int = np.array([int(val) for val in tokenized_cos_satelite_custumer])
                self.cost_satelite_custumer[k] = self.cost_satelite_custumer[k] + tokens_to_int
                k+=1
            