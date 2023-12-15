# Facility location problem 
A hybrid approach using "BRKGA", exact methods and fitness aproximation whith machine learning to solve facility location problem (TSCFLP)

# The TSCFLP problem

In a classic facility location problem, management decision makers have to decide which sites should be chosen to establish new facilities from a set of available candidate sites, while constraints are met in order to minimize the total cost and to guarantee that the demands of all customers have to be met, the capacity limits of the suppliers and facilities must be respected, etc. The cost includes fixed costs to open facilities and variable costs associated with transportation. The two-stage capacitated facility location problem (TSCFLP) is a variant of classic facility location problem and can be defined as follows: a single product manufactured in plants is delivered to depots, both having limited capacities. Then the products storage in depots are delivered to customers to satisfy their demands. The use of the plants and depots apply a fixed cost, while transportation from the plants to the customers through the depots results in a variable cost, depending on the quantity transported. The objective is identify what plants and depots to use, as well as the product flows from the plants to the depots and then to the customers such that the demands are met at a minimum cost.

# BRKGA 

A biased random-key genetic algorithm (BRKGA) is a general search metaheuristic proposed in Gonçalves and Resende (2011) and based on random-key genetic algorithm (RKGA), which was first introduced by Bean (1994) for solving combinatorial optimization problems involving sequencing. The chromosomes of a RKGA are represented as vectors of randomly generated real numbers in the interval [0, 1]. A deterministic algorithm, called decoder, transforms a solution vector in a solution of the combinatorial optimization problem for which an objective value or fitness can be computed.

# Encoding and Decoding a solution to a vector of random keys

A solution is encoded as a vector v=(v1,...,vn) of size n= ( |I| + |J| + |K|) where |I| is the number of plants |J| is the number of deposits and |K| is the number of customers and vx is a random number between 0 and 1.

The chromosome decoding process is done in 2 steps. The first step is to identify which plants and deposits will be opened. We order the factories based on the value of their random key and then select the factories that have the highest values until demand is satisfied. The same process is done for the deposits, we select those with the largest random keys until the selected deposits are able to support the production of the selected factories. With the factories and warehouses resolved, we add the fixed costs of each one to the total cost of the solution.

The second step is to establish the transport flow between factories, warehouses and customers.

For each factory we create a list of warehouses sorted by transportation cost in ascending order. Then the first warehouse is selected, the maximum possible quantity is transported and the next warehouse is selected until the factory's stock is exhausted, this is repeated for all factories until all production has been transported. The same goes for warehouses and customers, for each warehouse a list of customers is created ordered by transportation cost, the first warehouse sends as much as it can to the first customer and selects the next one until the warehouse's stock is exhausted. This is repeated for all warehouses until all customer demand is satisfied.

# Fitness aproximation 

The idea of using a fitness approach for complex continuous optimization problems has been proven efficient and effective (Jin, Olhofer & Sendhoff, 2002; Hacioglu, 2007; Zheng, Chen, Liu & Huang,
2016). The use of an ELM as an approximate fitness function in the TSCFLP problem was proposed in the article Peng Guo, Wenming Cheng, Yi Wang,2016.

# The algorithm 

The implementation of the BRKGA solution with fitness approximation used as a basis the algorithm proposed in the article C.E. Andrade. R.F. Toso, J.F. Gonçalves, M.G.C. Resende.

To implement the ELM, the open source skit-elm library was used, which provides an implementation based on the original article proposing the model.

The changes were:

1-During the algorithm initialization process, the chromosomes of the initial population and their respective fitness are passed as training data to the ELM.

2-During the evolution phase, the approximate fitness of all non-elite individuals are calculated. From these, the best individuals are selected as elite candidates. The actual fitness of the candidates is calculated and the actual chromosomes and fitness of these candidates are used to re-train the ELM. Then a comparison is made between the current elite and the candidates and the best individuals are added to the elite.




# References

[1] C.E. Andrade. R.F. Toso, J.F. Gonçalves, M.G.C. Resende. 
The Multi-Parent Biased Random-key Genetic Algorithm with Implicit Path Relinking.
European Journal of Operational Research, volume 289, number 1, pages 17–30, 2021. DOI https://doi.org/10.1016/j.ejor.2019.11.037

[2].José Fernando Gonçalves & Mauricio G. C. Resende. Biased random-key genetic algorithms for combinatorial optimization.

[3] G.-B. Huang, Q.-Y. Zhu and C.-K. Siew, "Extreme Learning Machine:
          Theory and Applications", Neurocomputing, vol. 70, pp. 489-501,
          2006.
          
