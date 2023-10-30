# repo_pmt_bomb

### thuật toán sử dụng:
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
### di chuyển 
    chia map làm 4 zone (theo kim đồng hồ) đê chọn các hướng di chuyển khác nhau

#### save zone: cách enemy >=4
    

***
### chọn action
    tại vị trí có điểm (cạnh trứng, bulk) => minimax 
        if in_save_zone : minimax no e
        else : minimax_ab (cắt cụt alpha beta) : hơi lâu nên tạm cmt
    tại vị trí ko có điểm => bfs
    bfs => [] => tìm egg

### chạy bot:
    vì python ko  edit đc global var từ package khác nên phải gom hết vào 1 file all_pro
    edit  GAME_ID ,PLAYER_ID, ENEMY_ID 


    