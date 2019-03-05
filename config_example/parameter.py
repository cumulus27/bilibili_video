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
merge_fragment_path = "config/merge_fragment_list.txt"
merge_fragment_files_path = "config/merge_fragment_files_list.txt"
use_ffmpeg_to_merge_fragments = True  # Recommend
use_ffmpeg_to_merge_audio = True  # Only chpice

# File type
file_types = [""]

# Max retry time
max_retry = 3

# Report type
save_in_database = True
txt_report = True

# merge
merge_fragment_delete = False
merge_audio_delete = False

# MySQL config
mysql_host = "localhost"
# mysql_user = "root"
# mysql_pass = ""
# mysql_user = "web"
# mysql_pass = "Scan123456)"
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
                         PRIMARY KEY (aid)
                         """

item_table1_list = "scid, apk_name, app_name, package_name, version, method, detected, scan_data," \
                   " detail_result, exitcode, try_times"

item_table1_value = "'{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}'"

item_table2 = """        cid CHAR(50) NOT NULL,
                         aid CHAR(50),
                         quality CHAR(20),
                         title TEXT(200) character set utf8,
                         path TEXT(200) character set utf8,
                         quality_des TEXT(50) character set utf8,
                         format CHAR(255),
                         download_time CHAR(255),
                         merge_time CHAR(255),
                         audio_merge CHAR(20),
                         piece_merge CHAR(20),
                         piece_delete CHAR(20),
                         exitcode CHAR(20),
                         PRIMARY KEY (cid)
                         """

