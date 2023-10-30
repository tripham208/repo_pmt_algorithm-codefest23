# repo_pmt_bomb

### 1. thuật toán sử dụng:
    minimax
    bfs
    a star
#### minimax
    handle đặt bomb và di chuyển sau đặt bom

#### bfs
    tìm vị trí có cạnh trứng/ tường phá đc
#### a star
    tìm gst egg
***
### 2. di chuyển 
    chia map làm 4 zone (theo kim đồng hồ) đê chọn các hướng di chuyển khác nhau

#### save zone: cách enemy >=4
    

***
### 3. chọn action
    tại vị trí có điểm (cạnh trứng, bulk) => minimax 
        if in_save_zone : minimax no e
        else : minimax_ab (cắt cụt alpha beta) : hơi lâu nên tạm cmt
    tại vị trí ko có điểm => bfs
    bfs => [] => tìm egg

### 4. chạy bot:
    vì python ko  edit đc global var từ package khác nên phải gom hết vào 1 file all_pro
    edit  GAME_ID ,PLAYER_ID, ENEMY_ID 

## !!! issue
    1:  do emit các event thi mà action trc đó chưa kết thúc sẽ bị ghi đè action khác => dễ đi vào bomb
        => check lại các điều kiện di chuyển , delay frame 
    2:  set time < x thì lock nhưng khi bomb nổ => unlock => tia lửa chưa end đã di chuyển qua