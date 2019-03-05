# Some config
cookies = ""

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
mysql_user = "web"
mysql_pass = "Scan123456)"
mysql_charset = 'utf8'
mysql_database = "bilibili"
mysql_table1 = "video_info"
mysql_table2 = "download_info"

item_table1 = """        av CHAR(50) NOT NULL,                        
                         title TEXT(200) character set utf8,
                         cv CHAR(50),
                         videos CHAR(20),
                         dynamic CHAR(255),
                         tname CHAR(20), 
                         video_data CHAR(255),
                         PRIMARY KEY (av)
                         """

item_table1_list = "scid, apk_name, app_name, package_name, version, method, detected, scan_data," \
                   " detail_result, exitcode, try_times"

item_table1_value = "'{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}'"

item_table2 = """        av CHAR(50) NOT NULL,                        
                         videos CHAR(20),
                         quality CHAR(20),
                         title TEXT(200) character set utf8,
                         path TEXT(200) character set utf8,
                         quality_des TEXT(50) character set utf8,
                         dynamic CHAR(255),
                         format CHAR(255),
                         insert_time CHAR(255),
                         download_time CHAR(255),
                         merge_time CHAR(255),
                         audio_merge CHAR(20),
                         piece_merge CHAR(20),
                         piece_delete CHAR(20),
                         download CHAR(20),
                         exitcode CHAR(20),
                         PRIMARY KEY (av)
                         """
