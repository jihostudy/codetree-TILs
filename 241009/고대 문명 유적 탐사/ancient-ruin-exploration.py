from collections import deque
K, M = list(map(int, input().split()))
arr = []
for _ in range(5):
    arr.append(list(map(int, input().split())))

fill = list(map(int, input().split()))
fill_idx = 0
candidates = [(1,1),(1,2),(1,3),(2,1),(2,2),(2,3),(3,1),(3,2),(3,3)]
rotates = [90,180,270]

def print_2darr(array,len):
    for arr in array:
        print(*arr)
# len길이의 arr의 복사본 만드는 함수
def copy_arr(arr,len):
    copy_arr = [[0] * len for _ in range(len)]
    for i in range(len):
        for j in range(len):
            copy_arr[i][j] = arr[i][j]
    return copy_arr

# len 길이의 arr을 rotate도 만큼 회전한 배열 반환
def rotate_arr(arr,len, rotate):
    rotated_arr = [[0] * len for _ in range(len)]
    for i in range(len):
        for j in range(len):
            if(rotate == 90):
                rotated_arr[j][len-1-i] = arr[i][j]
            elif(rotate == 180):
                rotated_arr[len - 1 - i][len - 1 - j] = arr[i][j]
            elif(rotate == 270):
                rotated_arr[len-1-j][i] = arr[i][j]
    return rotated_arr

nr = [0,1,0,-1]
nc = [1,0,-1,0]
def BFS(arr, length, visited, row,col, accumulate):
    cnt = 0
    target_value = arr[row][col]

    accumulate_tmp = [] # 3개 이상이면 accumulate에 넣기
    queue = deque()
    queue.append((row,col))
    visited[row][col] = True
    while queue:
        trow,tcol = queue.popleft()
        accumulate_tmp.append([trow, tcol])
        cnt += 1
        for i in range(4):
            nrow, ncol = trow + nr[i], tcol + nc[i]
            if(0 <= nrow < length and 0 <= ncol < length and visited[nrow][ncol] == False and arr[nrow][ncol] == target_value):
                queue.append((nrow, ncol))
                visited[nrow][ncol] = True
    # 3개 이상이면 accumulate에 넣기
    if(len(accumulate_tmp) >= 3):
        accumulate.extend(accumulate_tmp)
        return cnt
    return 0



# 상하좌우 연속된 것의 개수를 구하기
def get_val(arr,len):
    visited = [[False for _ in range(len)] for _ in range(len)]

    val = 0
    accumulate = [] #3개 이상 연결된 경우만 저장되어 있음
    for row in range(len):
        for col in range(len):
            if(visited[row][col] == False):
                length = BFS(arr,len,visited,row,col, accumulate) # 3개 이상인 경우만 BFS의 결과로 전달됨
                val += length
    return {"val": val, "accumulate": accumulate}




# 배열을 candidate을 기준으로 rotate 회전하기
def get_rotate_arr(arr,candidate,rotate):
    row,col = candidate

    #1. 복사하기
    copied_arr = copy_arr(arr,5)

    #2. 회전시키기 (3*3 배열을 때내기 > 회전 > 집어넣기)
    # 배열 떄내기
    subarr = [[0] * 3 for _ in range(3)]
    for i in range(3):
        for j in range(3):
            subarr[i][j] = arr[row-1+i][col-1+j]
    # 회전
    subarr = rotate_arr(subarr,3, rotate)
    # 집어넣기
    for i in range(3):
        for j in range(3):
             copied_arr[row-1+i][col-1+j] = subarr[i][j]
    return copied_arr



#----------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------
# 본코드
for _ in range(K):
    #1. lookout배열 채우기
    lookout = []
    for candidate in candidates:
        centerRow, centerCol = candidate
        # print("row:{}, col:{}".format(centerRow,centerCol))
        for rotate in rotates:
            tmp_rotated_arr = get_rotate_arr(arr, candidate, rotate)
            # print_2darr(tmp_rotated_arr,5)
            tmp_get_Val = get_val(tmp_rotated_arr, 5)["val"]
            # print("{}돌렷을때 value는 {}".format(rotate,tmp_get_Val))
            lookout.append({
                "row": centerRow,
                "col" :centerCol,
                "rotate": rotate,
                "val": tmp_get_Val
            })

    # 정렬하기
    sorted_lookout = sorted(lookout,key=lambda x: (-x["val"],x["rotate"],-x["col"],x["row"]))
    # print(sorted_lookout)
    target = sorted_lookout[0]
    # print(target)
    # 유물 탐사 불가능
    if(target["val"] < 3):
        # print("유물탐사 불가")
        break

    #1. 회전하기
    arr = get_rotate_arr(arr,(target["row"], target["col"]), target["rotate"])
    # print("회전후 arr")
    # print_2darr(arr,5)
    #2. 연속이 없을때까지 값 더하기
    answer = 0
    isDone = False
    while(not isDone):
        # print("여기")
        #2. 값 더하기
        getVal= get_val(arr,5)
        cnt = getVal["val"]
        # Case: 연속된게 없는 경우 (게임끝)
        if(cnt == 0):
            isDone = True
        # Case: 연속된게 있는 경우
        else:
            #2-1. 값 더하기
            answer += cnt
            # print("{} 더합니다".format(answer))
            #2-2. 채워넣기
            accumulate = sorted(getVal["accumulate"], key=lambda x:(x[1],-x[0]))
            for trow,tcol in accumulate:
                arr[trow][tcol] = fill[fill_idx]
                fill_idx += 1
    print(answer, end=" ")