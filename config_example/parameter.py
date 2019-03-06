# Some config
cookies = ""

# MySQL
mysql_user = ""
mysql_pass = ""

# path = "Download"
path = "Test"

# Config txt files
list_file_path = "config/list.txt"
merge_audio_path = "config/merge_audio_list.txt"
merge_piece_path = "config/merge_piece_list.txt"
merge_piece_files_path = "config/merge_piece_files_list.txt"
use_ffmpeg_to_merge_pieces = True  # Recommend
use_ffmpeg_to_merge_audio = True  # Only choice

# File type
file_types = [""]

# Max retry time
max_retry = 3

# Report type
save_in_database = True
txt_report = True

# merge
merge_piece_delete = False
merge_audio_delete = False
auto_merge = True

# MySQL config
mysql_host = "localhost"
# mysql_user = "root"
# mysql_pass = ""
mysql_charset = 'utf8'
mysql_database = "bilibili"
mysql_table1 = "video_info"
mysql_table2 = "download_info"

item_table1 = """        aid CHAR(50) NOT NULL,                        
                         title TEXT(200) character set utf8,
                         videos CHAR(20),
                         owner TEXT(50) character set utf8,
                         tname TEXT(50) character set utf8,
                         dynamic TEXT(100) character set utf8,
                         detail TEXT(200) character set utf8,
                         ctime CHAR(20),
                         insert_time CHAR(255),
                         download CHAR(20),
                         exit_code CHAR(20),
                         PRIMARY KEY (aid)
                         """

item_table2 = """        cid CHAR(50) NOT NULL,
                         aid CHAR(50),
                         quality CHAR(20),
                         title TEXT(200) character set utf8,
                         length CHAR(255),
                         path TEXT(200) character set utf8,
                         quality_des TEXT(50) character set utf8,
                         format CHAR(255),
                         download_time CHAR(255),
                         merge_time CHAR(255),
                         audio_merge CHAR(20),
                         piece_merge CHAR(20),
                         piece_delete CHAR(20),
                         exit_code CHAR(20),
                         PRIMARY KEY (cid)
                         """

