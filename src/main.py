from alpha import Alpha


def read_logs(path):
    logs = []
    for line in open(path):
        logs.append(tuple(line.split()))
    return logs


logs = read_logs("../logs/log2.txt")
alpha = Alpha(logs)
alpha.create_graph('graph2')


