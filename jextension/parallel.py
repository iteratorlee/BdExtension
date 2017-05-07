from pyspark import SparkConf, SparkContext
import os

APP_NAME = "Notebook Extension"
conf = SparkConf().setAppName(APP_NAME)
conf = conf.setMaster("local[*]")
sc = SparkContext(conf=conf)

def sort_by_col(filename, col):
    if not os.path.exists(filename):
        print("File not exist")
        return
    lines = sc.textFile(filename).flatMap(lambda x : x.split('\n'))
    lines = lines.map(lambda x : (float(x.split(',')[col]), x))
    lines = lines.sortByKey().map(lambda (x, y) : y).collect()
    lines = lines[0:1000]

    return lines

def get_col_sum(filename, col):
    if not os.path.exists(filename):
        print("File not exist")
        return

    lines = sc.textFile(filename).flatMap(lambda x : x.split('\n'))
    lines = lines.map(lambda x : float(x.split(',')[col]))
    ret = lines.reduce(lambda x, y : x + y)

    return ret

def get_col_ave(filename, col):
    if not os.path.exists(filename):
        print("File not exist")
        return

    lines = sc.textFile(filename).flatMap(lambda x : x.split('\n'))
    lines = lines.map(lambda x : float(x.split(',')[col]))
    ret = lines.reduce(lambda x, y : x + y)
    line_num = lines.count()

    return ret / float(line_num)
