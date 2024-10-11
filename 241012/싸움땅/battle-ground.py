def print_2d_array(array):
    for arr in array:
        print(*arr)


n,m,k = map(int,input().split())

#0. 입력받기
gun_board = []
for _ in range(n):
    array = ( list(map(int,input().split())))
    board = []
    for arr in array:
        board.append([arr])
    gun_board.append(board)

nr = [-1,0,1,0]
nc = [0,1,0,-1]

p_power = [0] * (m+1) # 능력치
p_gun = [0] * (m+1)   # 가지고 있는 총
p_row = [0] * (m+1)   # row 위치
p_col = [0] * (m+1)   # col 위치
p_dir = [0] * (m+1)   # 방향
answer =[0] * (m+1)   # 점수


for i in range(1,m+1):
    x,y,d,s = map(int,input().split())
    p_power[i] = s
    p_row[i] = x-1
    p_col[i] = y-1
    p_dir[i] = d

# print("초기 row:",p_row)
# print("초기 col:", p_col)
# print("초기 dir:", p_dir)
# print("초기 gun:",p_gun)
# 이동하려는 자리에 사람이 있는지 확인하는 함수
def check_player_exist(nrow, ncol):
    for i in range(1,m+1):
        if(p_row[i] == nrow and p_col[i] == ncol):
            return i
    return False

#본코드 한번 Loop
for loop in range(k):
    for player in range(1,m+1):
        # print("이동하는 player: {}".format(player))
        #1. 이동
        trow, tcol = p_row[player] + nr[p_dir[player]], p_col[player] + nc[p_dir[player]]
        #1.1: 격자 벗어난 경우
        if (trow < 0 or trow >= n or tcol < 0 or tcol >= n):
            p_dir[player] = (p_dir[player] + 2) % 4 #반대 방향
        nrow, ncol = p_row[player] + nr[p_dir[player]], p_col[player] + nc[p_dir[player]]


        #2. 결투
        #2-1: 다른 플레이어 X
        against = check_player_exist(nrow, ncol)

        # 1.2. 이동하기
        p_row[player], p_col[player] = nrow, ncol
        # print("nrow: {},ncol: {}".format(nrow, ncol))
        # print("against: {}".format(against))
        if(against == False):
            # print("다른 플레이어 없음")
            # 2-1-1: 칸에 총 O
            if (len(gun_board[nrow][ncol]) != 0):
                # 총 교체
                # 2-1-1-1: 나 총 X
                if(p_gun[player] == 0):
                    p_gun[player] = max(gun_board[nrow][ncol])  # TODO" 제일쏀거 집는건지 확인 필요
                    gun_board[nrow][ncol].remove(p_gun[player]) # 집은거 뺴기

                # 2-1-1-2: 나 총 O
                else:
                    new_gun_board = [p_gun[player],*gun_board[nrow][ncol]]
                    p_gun[player] = max(new_gun_board)  # 내것 포함 제일 쏀거
                    new_gun_board.remove(p_gun[player]) # 집은거 뺴기
                    gun_board[nrow][ncol] = new_gun_board
        #2-2: 다른 플레이어 O
        else:
            # 다른 플레이어
            against_strength =  p_power[against] + p_gun[against] # 상대방 힘 0번
            p_strength = p_power[player] + p_gun[player]          # 내 힘 1번
            winner = -1 # winner의 number를 저장
            loser = -1  # loser의 number를 저장
            # 2-2-1. 비김
            if(against_strength == p_strength):
                if(p_power[against] > p_power[player]):
                    winner = against
                    loser = player
                else:
                    winner = player
                    loser = against
            # 2-2-2. 승부남
            else:
                if(against_strength > p_strength):
                    winner = against
                    loser = player
                else:
                    winner = player
                    loser = against
            # print("winner: {}, loser: {}".format(winner,loser))
            # 2-2-2.winner 정해짐
            # Case1: loser 이동
            # 1. 격자에 총 내려놓기
            gun_board[nrow][ncol].append(p_gun[loser])
            p_gun[loser] = 0

            #2. 진 플레이어 이동
            #2.1. 가능할때까지 회전
            row_loser,col_loser, dir_loser = p_row[loser], p_col[loser], p_dir[loser]
            nrow_loser = row_loser + nr[dir_loser]
            ncol_loser = col_loser + nc[dir_loser]
            # print("loser의 현재 위치: row: {} col: {}".format(row_loser, col_loser))
            while(nrow_loser < 0 or nrow_loser >= n or ncol_loser < 0 or ncol_loser >= n or check_player_exist(nrow_loser,ncol_loser) != False):
                # print("돌립니다")
                p_dir[loser] = (p_dir[loser] + 1) % 4 # 회전
                dir_loser = p_dir[loser]
                nrow_loser = row_loser + nr[dir_loser]
                ncol_loser = col_loser + nc[dir_loser]
            #2.2. 이동
            p_row[loser] = nrow_loser
            p_col[loser] = ncol_loser
            # print("진사람을  row: {}, col: {}로 이동시킴".format(nrow_loser,ncol_loser))
            #2.3. 총 있으면 집기
            if(len(gun_board[nrow_loser][ncol_loser]) != 0):
                p_gun[loser] = max(gun_board[nrow_loser][ncol_loser])
                gun_board[nrow_loser][ncol_loser].remove(p_gun[loser])  # 집은거 뺴기

            #3. 이긴 플레이어
            #3.1. 점수 획득
            answer[winner] += abs(against_strength - p_strength)

            #3.2. 총 최신화
            new_gun_board = [p_gun[winner], *gun_board[nrow][ncol]]
            p_gun[winner] = max(new_gun_board)  # 내것 포함 제일 쏀거
            new_gun_board.remove(p_gun[winner])  # 집은거 뺴기
            gun_board[nrow][ncol] = new_gun_board
        # print("이동후 row:",p_row)
        # print("이동후 col:", p_col)
        # print("이동후 dir:", p_dir)
        # print("이동후 gun:",p_gun)

#결과 출력
for i in range(1,m+1):
    print(answer[i],end=" ")