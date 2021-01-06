import pymysql


# db 접속하기
def get_connection():
    conn = pymysql.connect(host='127.0.0.1', user='root',
                           password='', db='url', charset='utf8')
    if conn:
        print('디비 접속 완료')
    return conn


def process_input(input_url):
    check = check_url(input_url)
    if check != None:
        update_visit_number(check[0])
        return check[0]

    # db에 저장된 original_url이 없는 경우 new_url 생성

    new_url = shorten_url()

    # db에 new_url 저장
    insert_url(input_url, new_url)

    return new_url


# db에 이미 있는 url인지 확인
def check_url(original_url):
    conn = get_connection()
    cursor = conn.cursor()
    sql = ''' SELECT url_short FROM url_list WHERE url_long = %s  '''
    cursor.execute(sql, original_url)
    result = cursor.fetchone()
    conn.commit()
    conn.close()

    return result


def update_visit_number(url_existing):
    conn = get_connection()
    cursor = conn.cursor()

    sql = ''' SELECT submitted_num FROM url_list WHERE url_short = %s ''' #0
    cursor.execute(sql, url_existing)
    result = cursor.fetchone()
    conn.commit()
    conn.close()


    num = result[0] + 1
    plus_num(url_existing, num)


def plus_num(url_existing, num):
    conn = get_connection()
    cursor = conn.cursor()

    sql = ''' UPDATE url_list SET submitted_num = %s WHERE url_short = %s '''
    cursor.execute(sql, (num, url_existing))

    conn.commit()
    conn.close()

def insert_url(original_url, new_url):
    conn = get_connection()
    cursor = conn.cursor()
    sql = '''
            INSERT INTO url_list
                (url_long, url_short)
                values (%s, %s)
            '''
    cursor.execute(sql, (original_url, new_url))
    conn.commit()
    conn.close()


def shorten_url():
    url_characters = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    temp_url_short = []

    conn = get_connection()
    cursor = conn.cursor()
    sql = ''' SELECT COUNT(*) FROM url_list  '''
    cursor.execute(sql)
    url_info = cursor.fetchone()
    conn.commit()
    conn.close()

    index_id = url_info[0] + 1000000000

    while index_id > 0:
        val = index_id % len(url_characters)
        temp_url_short.append(url_characters[val])
        index_id = index_id // len(url_characters)

    return "".join(temp_url_short[::-1])


def take_url(url_short):
    conn = get_connection()
    cursor = conn.cursor()
    #
    #url_short = url_short[14:]
    sql = ''' SELECT url_long FROM url_list WHERE url_short = %s '''
    cursor.execute(sql, url_short)
    url_long = cursor.fetchone()
    conn.commit()
    conn.close()
    return url_long[0]


# 메인페이지에 URL 조회 랭크 탑5 보여주기
def get_url_rank():
    conn = get_connection()
    cursor = conn.cursor()

    sql = 'select url_long, submitted_num from url_list order by submitted_num DESC limit 5'
    cursor.execute(sql)
    #결과를 가져온다 => 이중 튜플로 되어 있음
    result = cursor.fetchall() #fectchone() fectchmany()

    temp_list=[]
    for row in result:
        temp_dic={}
        temp_dic['url'] = row[0] #튜플안의 index 0 값
        temp_dic['num'] = row[1]
        temp_list.append(temp_dic)

    conn.close()
    return temp_list