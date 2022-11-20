
import sys

all_input = []
while True:
    input_str = sys.stdin.readline().strip()
    if not input_str:
        break
    all_input.append(input_str)


for j in range(len(all_input)):
    out_put = ""
    input_str = all_input[j]
    fenzi = int(input_str.split("/")[0])
    fenmu = int(input_str.split("/")[1])
    # out_put = "{}/{}=".format(fenzi, fenmu)
    for i in range(10000):
        if fenzi == 1:
            out_put+="1/{}".format(fenmu)
            break
        elif fenmu % fenzi == 0:
            out_put+="1/{}".format(int(fenmu / fenzi))
            break
        elif fenmu % 2 == 0 and fenzi == 3:
            out_put+="1/{} + 1/{} + ".format(int(fenmu / 2), fenmu)
            break
        else:
            value = int(fenmu / fenzi) + 1
            fenzi = fenzi * value - fenmu  # 产生新的分子
            fenmu = value * fenmu  # 产生新的分母

            out_put+="1/{}+ ".format(value)

        i -= 1
    out_put = out_put.replace(" ", "")
    if out_put.endswith("+"):
        out_put = out_put[:-1]
    print(out_put)

