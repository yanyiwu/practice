#!/usr/bin/python
#-*-coding:utf8-*-
"""
author:wangyue
date:201801
brief:q训练 训练电脑先走的矩阵 
outputfile: path \t 路径序号\t电脑输赢状态(赢1输-1其余0)\t第几步走的棋
"""
import operator

WIN_MAP = {
            "0_0;0_1;0_2":1,\
            "1_0;1_1;1_2":1,\
            "2_0;2_1;2_2":1,\
            "0_0;1_0;2_0":1,\
            "0_1;1_1;2_1":1,\
            "0_2;1_2;2_2":1,\
            "0_0;1_1;2_2":1,\
            "0_2;1_1;2_0":1 \
                }
TOTAL_POINT = [(0,0),(0,1),(0,2),(1,0),(1,1),(1,2),(2,0),(2,1),(2,2)]

def find_status():
    """
    产出所有状态的对应表
    """
    status_map = {}
    total_index = 0
    layer_vec_odd = [] #奇数cache
    layer_vec_even = [] #偶数cache
    for index in range(len(TOTAL_POINT)):
        if index%2 == 0:#此时需要利用奇数cache 所以清零偶数cache
            layer_vec_even = []
            cache_vec = layer_vec_odd
        else:
            layer_vec_odd = []
            cache_vec = layer_vec_even
        print "index:" + str(index) + "lenjishu:" + str(len(layer_vec_odd)) + "lenoushu:" + str(len(layer_vec_even)) +\
                 "lencache:" + str(len(cache_vec)) + "totalindex:" + str(total_index)
        if index == 0:
            for ele in TOTAL_POINT:
                k = point_str(ele)
                status_map[k] = (total_index, 0, index)
                layer_vec_even.append(k)   
                total_index+=1
        else:
            new_cache_vec = []
            for point_path in cache_vec:
                if status_map[point_path][1] != 0:
                    continue
                
                for point in TOTAL_POINT:
                    str_ele = point_str(point)
                    if point_path.find(str_ele) == -1:
                        new_path = point_path + ";" + str_ele
                        status=decide_which_win(new_path)
                        status_map[new_path] = (total_index, status, index)
                        total_index+=1
                        new_cache_vec.append(new_path)
            if index %2 == 1: 
                layer_vec_odd = new_cache_vec  
            else:
                layer_vec_even = new_cache_vec
    print "total" + str(total_index)
    fw = open("../data/status.txt","w+")
    for zuhe in  sorted(status_map.iteritems(), key = lambda line:line[1][0], reverse= False):
        fw.write(zuhe[0] + "\t" + str(zuhe[1][0]) + "\t" + str(zuhe[1][1]) + "\t" + str(zuhe[1][2])+ "\n")           

def decide_which_win(new_path):
    """
    棋手一二形成的路径
    """
    path_total_list = new_path.split(';')
    path_one_list = [ele  for index, ele in enumerate(path_total_list) if index%2==0]
    path_two_list = [ele  for index, ele in enumerate(path_total_list) if index%2==1]
    if(decide_win_core(path_one_list)): return 1
    if(decide_win_core(path_two_list)): return -1
    return 0

def cmp_func(ele_one, ele_two):
    """
    排序函数
    """
    
    [ele_one_x, ele_one_y] = ele_one.split("_")
    [ele_two_x, ele_two_y] = ele_two.split("_")
    if ele_one_x < ele_two_x:
        return -1
    elif ele_one_x==ele_two_x and ele_one_y<=ele_two_y:
        return -1
    else:
        return 1

def decide_win_core(path_in):
    """
    true 就是赢了
    false 就是没赢
    """
    new_path_in = sorted(path_in, cmp_func)
    path_size = len(new_path_in)
    if path_size < 3:
        return False
    for index_one in range(path_size):
        for index_two in range(index_one+1, path_size):
            for index_three in range(index_two + 1, path_size):
                total_path = new_path_in[index_one] + ";" + new_path_in[index_two] + ";" + new_path_in[index_three]
                if total_path in WIN_MAP:
                    return True
    return False 


def point_str(point_in):
    """
    point变str
    """
    return str(point_in[0]) + "_" + str(point_in[1])

if __name__ == "__main__":
    find_status()
