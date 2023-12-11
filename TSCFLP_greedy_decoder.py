import numpy as np

class greedy_decoder:
    def __init__(self,instance):
        self.instance = instance


    def decode(self,chromosome,rewrite):  
        
        I = self.instance.parameters[0]
        J = self.instance.parameters[1]
        K = self.instance.parameters[2]
        
        cromossomo_fabrica = chromosome[:I]
        cromossomo_deposito = chromosome[I:]
        
        
        #Escolhe as fabricas que serzão abertas com base no cormossomo
        fabricas = {}
        for index, f in enumerate(cromossomo_fabrica):
            fabricas[index]  = f
        fabricas_ordenado = sorted(fabricas,key =fabricas.get )
     
        sum_fab= 0 
        fabricas_escolhidas= []
        for item in fabricas_ordenado:
            
            if sum_fab < self.instance.demanda_total:
                fabricas_escolhidas.append(item)
                sum_fab += self.instance.plant_capacity[item]
            else:
                break
 
        
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


        CUSTO_TOTAL = 0
        
        fluxo_fabricas = {}
        for fabrica in fabricas_escolhidas:
            fluxo_fabricas[fabrica] = self.instance.plant_capacity[fabrica]
            CUSTO_TOTAL += self.instance.plant_fxcost[fabrica]

        fluxo_depositos = {}
        for deposito in depositos_escolhidos:
            fluxo_depositos[deposito] = 0
            CUSTO_TOTAL += self.instance.stelite_fxcost[deposito]

        fluxo_cliente = {}
        for i in np.arange(len(self.instance.demanda_clientes)):
            fluxo_cliente[i] = 0



        #Fabricas para depositos
        for fabrica in fluxo_fabricas.keys():
            ordem_custo_depo = sorted(depositos_escolhidos,key=lambda depositos: self.instance.cost_plant_satelite[fabrica][depositos])
            for depo in ordem_custo_depo:
                if fluxo_depositos[depo] < self.instance.stelite_capacity[depo]:
                    quantidade_faltante = self.instance.stelite_capacity[depo] - fluxo_depositos[depo]
                    if fluxo_fabricas[fabrica] >= quantidade_faltante:
                        quantidade_enviada = quantidade_faltante
                        fluxo_fabricas[fabrica] -= quantidade_enviada
                        fluxo_depositos[depo] += quantidade_enviada
                        CUSTO_TOTAL += quantidade_enviada*self.instance.cost_plant_satelite[fabrica][depo]
                    else:
                        quantidade_enviada = fluxo_fabricas[fabrica] 
                        fluxo_fabricas[fabrica] -= quantidade_enviada
                        fluxo_depositos[depo] += quantidade_enviada
                        CUSTO_TOTAL +=quantidade_enviada*self.instance.cost_plant_satelite[fabrica][depo]
                else:
                    continue
        #Depósitos para clientes
        for deposito in fluxo_depositos.keys():
            ordem_depo_cliente = sorted(np.arange(K),key=lambda cli: self.instance.cost_satelite_custumer[deposito][cli])
            for cliente in ordem_depo_cliente:
                if fluxo_cliente[cliente] < self.instance.demanda_clientes[cliente]:
                    quantidade_faltante = self.instance.demanda_clientes[cliente] - fluxo_cliente[cliente]
                    if fluxo_depositos[deposito] >= quantidade_faltante:
                        quantidade_enviada = quantidade_faltante
                        fluxo_depositos[deposito] -= quantidade_enviada
                        fluxo_cliente[cliente] += quantidade_enviada
                        CUSTO_TOTAL += quantidade_enviada*self.instance.cost_satelite_custumer[deposito][cliente]
                    else:
                        quantidade_enviada = fluxo_depositos[deposito]
                        fluxo_depositos[deposito] -=quantidade_enviada
                        fluxo_cliente[cliente] +=quantidade_enviada
                        CUSTO_TOTAL += quantidade_enviada*self.instance.cost_satelite_custumer[deposito][cliente]
                else:
                    continue
        return CUSTO_TOTAL

