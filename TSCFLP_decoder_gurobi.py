
import gurobipy as gb
import numpy as np

class solver_decoder:
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
                
            
        
        
        m = gb.Model("TSCFLP")
        m.Params.OutputFlag = 0
        #variáveis de decisão
        yi = m.addVars(fabricas_escolhidas,vtype= gb.GRB.BINARY)

        zj = m.addVars(depositos_escolhidos,vtype= gb.GRB.BINARY)

        xij = m.addVars(fabricas_escolhidas,depositos_escolhidos,vtype = gb.GRB.INTEGER)

        sjk = m.addVars(depositos_escolhidos, np.arange(K),vtype = gb.GRB.INTEGER)

        #função objetivo

        m.setObjective(
            gb.quicksum(self.instance.plant_fxcost[i]*yi[i] for i in fabricas_escolhidas)

            + gb.quicksum(self.instance.stelite_fxcost[j]*zj[j] for j in depositos_escolhidos)

            + gb.quicksum(self.instance.cost_plant_satelite[i][j]*xij[i,j]for i in fabricas_escolhidas for j in depositos_escolhidos)

            + gb.quicksum(self.instance.cost_satelite_custumer[j][k]*sjk[j,k] for j in depositos_escolhidos for k in np.arange(K)),
        sense= gb.GRB.MINIMIZE)

        #Constrains


        #Restrição de demanda sendo atendida
        c1 = m.addConstrs((gb.quicksum(sjk[j,k] for j in depositos_escolhidos)>= self.instance.demanda_clientes[k]) for k in np.arange(K))

        #Restrição de flow

        c2 = m.addConstrs((gb.quicksum(xij[i,j] for i in fabricas_escolhidas) >= gb.quicksum(sjk[j,k] for k in np.arange(K))) for j in depositos_escolhidos)

        #Restrição capacidade das plantas 
        c3 = m.addConstrs((gb.quicksum(xij[i,j] for j in depositos_escolhidos)<= self.instance.plant_capacity[i]* yi[i]) for i in fabricas_escolhidas)

        #Restrição capacidade dos depositos
        c4 = m.addConstrs((gb.quicksum(sjk[j,k] for k in np.arange(K))<= self. instance.stelite_capacity[j] * zj[j]) for j in depositos_escolhidos)

        m.optimize()
        if m.SolCount >= 1:
            ret = m.ObjVal
        else:
            ret = 10e8
        return ret