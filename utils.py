import numpy as np
import os
import json

class Instance:
    def __init__(self, m, n, l, s, D):
        self.m = m
        self.n = n
        self.l = l
        self.s = s
        self.D = np.array(D)
        self.ratio_courier_loads = np.max(l)//np.min(l)
        self.courier_dist_lb = self.set_d_low_bound()
        self.courier_dist_ub = self.set_d_up_bound()
        self.rho_low_bound = self.set_rho_lower_bound()
        self.courier_min_load, self. courier_max_load = self.set_min_max_loads()
        self.correspondences = None
        self.corr_inverse = None
        self.courier_sort_dict = None

    def set_rho_lower_bound(self):  
        last_row = self.D[-1]
        last_column = self.D[:,-1]
        value1 = last_column[np.argmax(last_row)] + max(last_row)
        value2 = last_row[np.argmax(last_column)] + max(last_column)
        lb = max(value1, value2)
        return lb  
    
    def set_d_low_bound(self):  
        last_row = self.D[-1]
        last_column = self.D[:,-1]
        last_column = last_column[last_column != 0]
        last_row = last_row[last_row !=0]
        value1 = last_column[np.argmin(last_row)] + min(last_row)
        value2 = last_row[np.argmin(last_column)] + min(last_column)
        d_low_bound = max(value1, value2)
        #print("Distance low bound: ", d_low_bound)
        return d_low_bound
    
    def set_d_up_bound(self):
       up_bound = np.max(self.D)*self.n //self.m + np.max(np.array(self.D)[:,-1])
       return up_bound
    
    def set_min_max_loads(self):
      min_l = np.min(self.s)
      max_l = np.max(self.l)
      return min_l, max_l
    
        
    def sort_l(self, reverse=False):
        arr = np.array(self.l)
        if reverse:
            sorted_indices = np.argsort(-arr)  # Use negative values for reverse sorting
        else:
            sorted_indices = np.argsort(arr)
        sorted_list = arr[sorted_indices]
        ordered_dict = {}
        for i in range(len(arr)):
            ordered_dict[i] = sorted_indices[i]
        return list(sorted_list), ordered_dict
    


    def preprocess_instance(self):
        self.correspondences = np.argsort(self.l)[::-1]
        transformation_function = sorted(zip(self.correspondences, np.arange(self.m)))
        self.corr_inverse = np.fromiter((x for _, x in transformation_function), dtype= int)

        self.l, self.courier_sort_dict = self.sort_l(reverse=True)

      
      
    def post_process_instance(self,  distances = [], solution = [[]]):
    
        true_order_distaces = list(distances)
        true_order_solution = list(solution)
        for start, end in self.courier_sort_dict.items():
              true_order_solution[end] = solution[start]
              true_order_distaces[end] = distances[start]
 
        return true_order_distaces, true_order_solution


    def unpack(self):
      return self.m, self.n, self.s, self.l, self.D
        
def load_instance(path: str, num: int, preprocessing: bool = True):
  if num < 10:
    num = "0"+str(num)
  else:
    num = str(num)
  path += f"/inst{num}.dat"
  file = open(path, 'r')
  
  m = int(file.readline())
  n = int(file.readline())
  l = [int(x) for x in file.readline().split(" ") if x!= ""]
  s = [int(x) for x in file.readline().split(" ") if x!= ""]
  D = []
  for i in range(n+1):
      D.append([int(x) for x in file.readline().split(" ") if x!= "\n" if x!= ""])
  
  instance = Instance(m, n, l, s, D)
  if preprocessing:
    instance.preprocess_instance()
  return instance

def load_data(path: str, num):
  if type(num) == int:
    if 0 < num <= 21:
      return {str(num): load_instance(path, num)}
    elif num == 0:
      return {str(x): load_instance(path, x) for x in range(1, 22)}
    else:
      raise ValueError("The specified instance ID is wrong: expected between 1 and 21")
  
  elif type(num) == list:
    return {str(x): load_instance(path, x) for x in num}
  
  else:
    raise TypeError("The number of instance should be either an integer or a list of integers")
  
def save_file(path, filename, json_dict):
  if not os.path.exists(path):
      os.makedirs(path)
      
  with open(path + filename, 'w') as file:
      json.dump(json_dict, file)
      os.makedirs(path)
      
  with open(path + filename, 'w') as file:
      json.dump(json_dict, file)
