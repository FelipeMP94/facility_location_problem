
from skelm import ELMRegressor
from sklearn.model_selection import train_test_split
import sklearn
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor


class Fitness_aproximation:
    def __init__(self,instance):
        self.instance = instance
        self.train_data = 0
        self.test_data = 0
        self.trained = False

    
    def prepare_data(self,fit,initial_population):
        X = []#Cromossomo com valores binarios 
        X_not_transformed = [] #Cromossomo nao binario
        Y = []#Fit do cromossomo
        for element in fit:
            Y.append(element[0])
            X_not_transformed.append(initial_population[element[1]])

        for x in X_not_transformed:
            cromossomo_fabrica = x[:self.instance.parameters[0]]
            cromossomo_deposito = x[self.instance.parameters[0]:]


            fabricas = {}
            for index, f in enumerate(cromossomo_fabrica):
                fabricas[index]  = f
            fabricas_ordenado = sorted(fabricas,key =fabricas.get )

            fabricas_escolhidas = []
            sum_fab= 0 
            for item in fabricas_ordenado:      
                if sum_fab < self.instance.demanda_total:
                    fabricas_escolhidas.append(item)
                    sum_fab += self.instance.plant_capacity[item]
                else:
                    break

            X_fabricas = []
            for i in np.arange(len(cromossomo_fabrica)):
                if i not in fabricas_escolhidas:
                    X_fabricas.append(0) 
                else:
                    X_fabricas.append(1)


            #Escolhe os depositos que serão abertos com base no cromossomo
            depositos = {}
            for index,d in enumerate(cromossomo_deposito):
                depositos[index] = d
            depositos_ordenados = sorted(depositos,key=depositos.get)


            sum_dep = 0 
            depositos_escolhidos = []
            for item in depositos_ordenados:
                if sum_dep < sum_fab:
                    depositos_escolhidos.append(item)
                    sum_dep += self.instance.stelite_capacity[item]
                else:
                    break

            X_depositos = []
            for i in np.arange(len(cromossomo_deposito)):
                if i not in depositos_escolhidos:
                    X_depositos.append(0)
                else:
                    X_depositos.append(1)

            result = X_fabricas + X_depositos
            X.append(result)
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.3, random_state=42)
        self.train_data = [X_train,Y_train]
        self.test_data = [X_test,Y_test]




class ELM_decoder(Fitness_aproximation):
    def __init__(self,instance):
        super().__init__(instance)
        self.ELM = ELMRegressor(n_neurons=800,
                     ufunc='relu',
                     density=0.7,
                      pairwise_metric= 'euclidean',
                     alpha= 10e-4)
        self.MAE = 0

    def train_model(self):
        self.ELM.fit(self.train_data[0],self.train_data[1])
        self.trained = True
        pred = self.ELM.predict(self.test_data[0])
        self.MAE = sklearn.metrics.mean_absolute_error(self.test_data[1],pred)
        
        
    def decode(self,chromosome,rewrite = True):
        re_crom = np.reshape(chromosome,(1,-1))
        x = self.ELM.predict(re_crom)
        return x



class Gradient_Boosting_decoder(Fitness_aproximation):
    def __init__(self,instance):
        super().__init__(instance)
        self.GB = GradientBoostingRegressor(n_estimators=5000,loss='absolute_error')
        self.MAE = 0
    
    def train_model(self):
        self.GB.fit(self.train_data[0],self.train_data[1])
        self.trained = True
        pred = self.GB.predict(self.test_data[0])
        self.MAE = sklearn.metrics.mean_absolute_error(self.test_data[1],pred)
        
        
    def decode(self,chromosome,rewrite = True):
        x = self.GB.predict(chromosome)
        return x  
        