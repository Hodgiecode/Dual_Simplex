import math

class Simplex:
    def __init__(self, m, n, table, mode):
        self.N = 20
        self.M = 20
        self.epsilon = 1e-8
        self.table = table

        self.n = n
        self.m = m

        self.n_init = n
        self.m_init = m
       
        self.counter = 0
        self.mode = mode
        
    def add_slack_variable(self):
        self.n += self.m - 1
        tmp = []
        for i in range(self.m): tmp.append([1 if i == j else 0 for j in range(1, self.n - 1)])

        tmp=[[0, 0, 0], [1, 0, 0], [0, 1, 0],[0,0,1]]
        for i in range(len(self.table)): self.table[i] += tmp[i]


    def print_table(self, msg):
        self.counter = self.counter + 1
        print("\n%s Table %s:\n" % (self.counter, msg) , end = "")
        print("col:", "b[i]", end = "")

        for j in range(self.n): print(" x%s" % j, end = "")
        print()

        for i in range(self.m):
            if i == 0: print(self.mode + " ", end = "")
            if i != 0: print("b%d: " % i, end = "")

            for j in range(self.n):
                if abs(int(self.table[i][j]) - self.table[i][j]) < self.epsilon:
                    print(int(self.table[i][j]), end = "")
                else:
                    print(self.table[i][j], end = "")

                print(" ", end = "")

            print()

    def print_optimal_vector(self, msg):
        print("%s at " % msg, end = "")
        for j in range(1, self.n):
            xi = self.find_basis_variable(j)
            if xi != -1:
                print("x%s = %s, " % (j, self.table[xi][0]), end = "")
            else:
                print("x%s = 0, " % j, end = "")

        print()
    

    def check_b_positive(self):
        for i in range(self.m): assert self.table[i][0] >= 0
        
    def pivot_on(self, row, col):
        pivot = self.table[row][col]
        assert pivot > 0

        for j in range(self.n): self.table[row][j] /= pivot

        assert (abs(self.table[row][col] - 1) < self.epsilon)

        for i in range(self.m):
            multiplier = self.table[i][col]
            
            if i == row: continue

            for j in range(self.n):
                self.table[i][j] -= multiplier * self.table[row][j]
                
    def find_pivot_column(self):
        pivot_col = 1
        lowest = self.table[0][pivot_col]
        for j in range(self.n):
            if self.table[0][j] < lowest:
                lowest = self.table[0][j]
                pivot_col = j

        print("Most negative column in row[0] is col %s = %s." % (pivot_col, lowest))
        if lowest >= 0: return -1

        return pivot_col

    def find_pivot_row(self, pivot_col):
        pivot_row = 0
        min_ratio = -1

        #print("Ratios A[row_i,0]/A[row_i,%s] = [" % pivot_col, end = "")
        
        for i in range(1, self.m):
            #print(self.table[i][0],self.table[i][pivot_col])
            if abs(self.table[i][pivot_col])<self.epsilon:
                continue
            
            ratio = self.table[i][0] / float(self.table[i][pivot_col])
            #print("%s, " % ratio, end="")
            if ((ratio > 0 and ratio < min_ratio) or min_ratio < 0):
                min_ratio = ratio
                pivot_row = i

        #print("].")
        if min_ratio == -1: return -1
        print("Found pivot A[%s,%s], min positive ratio = %s in row = %s." % (pivot_row, pivot_col, min_ratio, pivot_row), end = "")

        return pivot_row


    def find_basis_variable(self, col):
        xi = -1
        for i in range(1, self.m):
            if abs(self.table[i][col] - 1) < self.epsilon:
                if xi == -1: xi = i
                else: return -1

            else:
                if not (abs(self.table[i][col]) < self.epsilon): return -1

        return xi

    def simplex(self):
        loop = 0
        self.add_slack_variable()

        self.print_table("Padded with slack varibales")

        while True:
            pivot_col = self.find_pivot_column()
            
            if pivot_col < 0:
                if self.mode == "max":
                    print("Found optimal value=A[0,0]=%s (no negatives in row 0)." % self.table[0][0])
                    self.print_optimal_vector("Optimal vector")
                else:
                    print("Optimal_vector",self.table[0][self.n_init+1:][:-1])
                break


            print("Entering variable x%s to be made basic, so pivot_col=%s." % (pivot_col, pivot_col))
            pivot_row = self.find_pivot_row(pivot_col)
            
            
            if pivot_row < 0:
                print("unbounded (no pivot_row)");
                break

            print("Leaving variable x%s, so pivot_row=%s" % (pivot_row, pivot_row))
            self.pivot_on(pivot_row, pivot_col)

            self.print_table("After pivoting");
            self.print_optimal_vector("Basic feasible solution");

            if loop > 20:
                print("Too many iterations > %s." % loop);
                break
            
            loop += 1


    def main(self):
        if self.mode == "min":
            self.table[0].append(0)
            self.table = [list(i) for i in zip(*self.table)]
            self.table = [self.table[-1]] + self.table[:-1]
            self.table[0] = [0]+[-1 * elem for elem in self.table[0]][1:]
        else:
            self.table[0] = [0] + [-1*x for x in self.table[0]]
            for i in range(1, len(self.table)): self.table[i] = [self.table[i][-1]] + self.table[i][:-1]

        self.m = len(self.table)
        self.n = len(self.table[0])

        self.simplex()


def run_solution(m,n,arr,mode):
    #arr=[[0.5,3,1,4],[1,1,1,1,40],[-2,-1,1,1,10],[0,1,0,-1,10]]
    A=Simplex(m,n,arr,mode)

    #arr=[[12,10],[2,12,20],[4,6,32],[3,0,14],[0,18,42]]
    #A=Simplex(3,4,arr,"min")

    #arr=[[20, 32, 14, 42], [ 2, 4, 3, 0, 12], [12, 6, 0, 18, 10]]
    #A=Simplex(2,4,arr,"max")

    A.main()

