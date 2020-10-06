import sys, json, numpy as np



#Read data from stdin
def read_in():
    lines = sys.stdin.readlines() #paramter를 읽음
    return json.loads(lines[0])  #이 예제에서는 첫 줄만 사용

def main():
    lines = read_in()
    np_lines = np.array(lines)       # String -> Array 변환
    lines_sum = np.sum(np_lines) #Array 총 합 계산
    print(lines_sum)                      #총합 반환   
#    return lines_sum

if __name__ == '__main__': # Python 특성상, 독자적으로 불리면 main인데, 여기서는 독립적으로 실행되는 형태라 맞기 때문에 main
    main()