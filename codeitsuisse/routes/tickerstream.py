import numpy as np
import pandas as pd

def to_cumulative(stream: list):
  df = pd.DataFrame(stream)
  df = df.iloc[:, 0].str.split(',', expand=True)
  df[2] = df[2].astype(np.int8)
  df[3] = df[3].astype(np.float32)
  df[4] = np.round(df[2] * df[3],decimals=1)
  df.sort_values([0,1], ascending=True, inplace=True)
  df[2] = df[2].astype(str)
  df[4] = df[4].astype(str)
  pre_time = df.iloc[0,:,][0]
  result = []
  tick = ''+pre_time
  for i in df.iterrows():
      if i[1][0] != pre_time:
          result.append(tick)
          pre_time = i[1][0]
          tick = ''+pre_time
      temp = ','.join([i[1][1], i[1][2], i[1][4]])
      tick = tick +','+temp
  result.append(tick)
  return(result)


def to_cumulative_delayed(stream: list, quantity_block: int):
  stream.sort(key = lambda x: x.split(',')[0])
  df = pd.DataFrame(stream)
  df = df.iloc[:, 0].str.split(',', expand=True)
  df[2] = df[2].astype(np.int8)
  df[3] = df[3].astype(np.float32)
  labels = df[1].unique()
  quantity_block = 5
  result = []
  for i in labels:
      temp = df[df[1] == i]
      cumu_quantity, cumu_national = 0, 0
      for j in temp.iterrows():
          if cumu_quantity + j[1][2] == quantity_block:
              cumu_national +=  round((j[1][2] * j[1][3]), 1)
              cumu_quantity += j[1][2]
              result.append(','.join([j[1][0], j[1][1], str(cumu_quantity), str(cumu_national)]))
              cumu_quantity, cumu_national = 0, 0
  
          elif cumu_quantity + j[1][2] < quantity_block:
              cumu_national +=  round((j[1][2] * j[1][3]), 1)
              cumu_quantity += j[1][2]
          elif cumu_quantity + j[1][2] > quantity_block:
              cumu_national += round((quantity_block - cumu_quantity) * j[1][3],1)
              cumu_quantity = quantity_block
              result.append(','.join([j[1][0], j[1][1], str(cumu_quantity), str(cumu_national)]))
              cumu_quantity, cumu_national = 0, 0
  result.sort(key=lambda x:x.split(',')[0])
  return result
