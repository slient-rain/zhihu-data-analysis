#!/usr/bin/env python
#  -*- coding: utf-8 -*-

from DAO import UserDataDAO
from Statistics import Stats
import math
from ParallelFetch import  Level3ParallelFetch


import matplotlib
matplotlib.use('Qt4Agg')
import matplotlib.pyplot as plt

def draw(dict):
   argee_num_list=[]
   user_count_list=[]
   i=0
   for (argee_num, user_count) in dict.items():
      # if i>10 :
      #    break
      # print argee_num  ,'  ', user_count
      argee_num_list.append(argee_num)
      user_count_list.append(user_count)
      i+=1
   plt.plot(argee_num_list, user_count_list, 'ro')
   plt.show()
   plt.savefig(r'e:/MyFig.jpg')
def main():
   dao=UserDataDAO()
   user_list=dao.queryAll()

   user_num_list={}
   agree_num_list = [float(agree_num[3]) for agree_num in user_list]
   for agree_num in agree_num_list:
      if(user_num_list.get(agree_num)==None):
         user_num_list[agree_num]=1
      else:
         user_num_list[agree_num]+=1
   draw(user_num_list)
   # print user_num_list
   #
   # index_list=['agree_num' , 'thanks_num' , 'follower_num' , 'followee_num' , 'answer_num']
   # print '%-16s%-16s%-16s%-16s'%('','avg','median','stdev')
   # for i in range(5):
   #    print '%-16s%-16.2f%-16.2f%-16.2f '%(index_list[i],avg_list[i],median_list[i],stdev_list[i])


def get_basic_stats_data():
   dao = UserDataDAO()
   user_list = dao.queryAll()

   avg_list = []
   median_list = []
   stdev_list = []
   for i in range(3, 8):
      num_list = [float(agree_num[i]) for agree_num in user_list]
      stats = Stats(num_list)
      avg_list.append(stats.avg())
      median_list.append(stats.median())
      stdev_list.append(stats.stdev())


   index_list=['agree_num' , 'thanks_num' , 'followee_num' , 'follower_num' , 'answer_num']
   print '%-16s%-16s%-16s%-16s'%('','avg','median','stdev')
   for i in range(5):
      print '%-16s%-16.2f%-16.2f%-16.2f '%(index_list[i],avg_list[i],median_list[i],stdev_list[i])

if __name__ == '__main__':
  # main()
  pf=Level3ParallelFetch()
  pf.multi_process_get_user_data()
