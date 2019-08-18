#-*-coding:utf8-*-

"""
author:wangyue
date:201801
brief:得到所需要的q矩阵
迭代遵循如下公式
#Q(state, action) = R(state, action) + Gamma * MaxQ(next state, all actions)
"""
from scipy.sparse import *  #构造稀疏矩阵
from scipy.sparse import csr_matrix
import random
level_map = {0:(0,8),\
             1:(9,80),\
             2:(81,584),\
             3:(585,3608),\
             4:(3609,18728),\
             5:(18729,73448),\
             6:(73449,221624),\
             7:(221625,422072),\
             8:(422073,549944),\
            }
total_staus_num = 549945
total_point = ["0_0", "0_1", "0_2", "1_0", "1_1", "1_2", "2_0", "2_1", "2_2"]
def can_reach(path_one, path_two):
    if path_two.find(path_one) != -1:
        return 1
    else:
        return 0

def produce_R_mat():
    id_map = {}
    path_to_id = {}
    fp = open('../data/status.txt') 
    for line in fp:
        item = line.strip().split('\t')
        [path, id_t, score, step] = item
        id_map[int(id_t)] = (path, score, step)
        path_to_id[path] = int(id_t)
    data = []
    row = []
    col = []
    for step in range(0,9):
        print step    
        if step == 8:
           continue             
        step_next = step + 1
        step_range = range(level_map[step][0], level_map[step][1])
        step_next_range = range(level_map[step_next][0], level_map[step_next][1]) 
        for index in step_range:
            (path,score,step) = id_map[index]
            can_reach_path_list = create_reach_path(path)
            for path_next in can_reach_path_list:
                if path_next not in path_to_id:
                    continue
                index_next =  path_to_id[path_next]    
                (path_next, score_next,step_n) = id_map[index_next] 
                row.append(index) 
                col.append(index_next) 
                if score_next == "1":
                    data.append(100)
                elif score_next == "0":
                    data.append(50)   
                else:
                    data.append(1)

    rmat_csr = coo_matrix((data, (row,col)), shape=(total_staus_num, total_staus_num)).tocsr()        
    return rmat_csr, path_to_id

def qlearn_train(rmat_csr, path_to_id):
    """
    qlearn 的train
    Q(state, action) = R(state, action) + Gamma * MaxQ(next state, all actions)
    """
    q_map = {}
    gamma = 0.8
    init_qmat = coo_matrix(total_staus_num, total_staus_num)
    epoch = 2500000
    for index in range(epoch):
        initial_step = total_point[index%len(total_point)]
        path_id = path_to_id[initial_step] 
        tmp_map = {} #判断是否迭代中止
        for step in range(0, 8):
            non_zero_list = rmat_csr[path_id].nonzero()[1]
            if len(non_zero_list) == 0:
                break
            next_path_id = random.choice(non_zero_list)  
            select_list = [q_map.get(str(next_path_id) + "_" + str(column), 0) for column in rmat_csr[next_path_id].nonzero()[1]]
            if len(select_list) == 0:
                next_max = 0
            else:
                next_max = max(select_list)
            tmp_map[str(path_id)+ "_" + str(next_path_id)] = rmat_csr[path_id].getcol(next_path_id).toarray()[0][0] + gamma*next_max
            path_id = next_path_id
        same = 0
        for ele in tmp_map.items():
            if ele[0] in q_map and ele[1]==q_map[ele[0]]:
                same += 1
            else:
                q_map[ele[0]] = ele[1]
        
        if same == len(tmp_map):
            print "equal break" + str(index)
        
    fw = open('../data/mat_1.txt','w+')
    for key in q_map:
        fw.write(key + "\t" + str(q_map[key]) + "\n")           

def create_reach_path(path):
    res_list = []
    for ele in total_point:
        if path.find(ele) == -1:
            res_list.append(path + ";" + ele)
    return res_list
if __name__ == "__main__":
    rmat_csr, path_to_id = produce_R_mat()
    qlearn_train(rmat_csr, path_to_id)
