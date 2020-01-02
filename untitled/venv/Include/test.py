import os
import shutil
import requests
import json
from lxml import html
import time
import re
import urllib.request

headers = {
    # 'Cookies':'SUB=_2A25xgwvUDeRhGeBN7FoU9SzJyzmIHXVSj5WcrDV6PUJbkdAKLWrukW1NRArvY5Bm433yk8F2VI-rnvIJU6E9sZpJ; SUHB=010GCPyqzcv2w4; SCF=AmxfXClfex8bJruLjpDGuj_HkiQ0ruLZt7O5LBUqsqttQtoskRiPxXPI-zaCehtuzjU-YbhbLWBIwQIvvcmN1VE.; SSOLoginState=1552382852; _T_WM=6ca499957ef4fe628d21dbf0971e2a27; MLOGIN=1; WEIBOCN_FROM=1110006030; XSRF-TOKEN=863cd5; M_WEIBOCN_PARAMS=luicode%3D10000011%26lfid%3D100103type%253D1%2526q%253D%25E6%25A0%25A1%25E8%258D%2589%26fid%3D10080818b3ed999cd7b9b893ddf2ee3414346f%26uicode%3D10000011',
    'Cookies': 'SUB=_2A25xgwvUDeRhGeBN7FoU9SzJyzmIHXVSj5WcrDV6PUJbkdAKLWrukW1NRArvY5Bm433yk8F2VI-rnvIJU6E9sZpJ; SUHB=010GCPyqzcv2w4; SCF=AmxfXClfex8bJruLjpDGuj_HkiQ0ruLZt7O5LBUqsqttQtoskRiPxXPI-zaCehtuzjU-YbhbLWBIwQIvvcmN1VE.; SSOLoginState=1552382852; _T_WM=6ca499957ef4fe628d21dbf0971e2a27; MLOGIN=1; WEIBOCN_FROM=1110006030; XSRF-TOKEN=09566d; M_WEIBOCN_PARAMS=luicode%3D10000011%26lfid%3D10080818b3ed999cd7b9b893ddf2ee3414346f_-_feed%26fid%3D1005052914737397%26uicode%3D10000011',
    'Host': 'm.weibo.cn',
    # 'Referer':'https://m.weibo.cn/p/index?containerid=10080818b3ed999cd7b9b893ddf2ee3414346f&luicode=10000011&lfid=100103type%3D1%26q%3D%E6%A0%A1%E8%8D%89',
    'Referer': 'https://m.weibo.cn/sw.js',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
}

# user_url ='https://m.weibo.cn/api/container/getIndex?containerid=10080818b3ed999cd7b9b893ddf2ee3414346f_-_main&luicode=10000011&lfid=100103type%3D1%26q%3D%E6%A0%A1%E8%8D%89'

#user_url = 'https://m.weibo.cn/api/container/getIndex?type=uid&value=2914737397&containerid=1076032914737397'
user_url='https://m.weibo.cn/api/container/getIndex?type=uid&value=2607803303&containerid=1076032607803303'

tmp_folder_name = 'WeiboData_'
tmp_folder_time = '2019_'
user_name = '章'

txt_file_name = '_Weibo_DataRecords.txt'

num_page = 2

path = tmp_folder_name + tmp_folder_time + user_name + '/'
if os.path.exists(path) is True:
    shutil.rmtree(path)
os.mkdir(path)

print('\n' + 40 * '=' + '\n' + 'Crawling Weibo data of user - ' + user_name + '.\n' + 40 * '=')

print('\n' + 40 * '=' + '\n' + 'The number of crawling pages is: ' + str(num_page) + '.' + '\n' + 40 * '=' + '\n')

ii = 0
list_cards = []

while ii < num_page:
    ii += 1
    print('Start crawling "cards" on page %d/%d.' % (ii, num_page))

    url = user_url + '&page=' + str(ii)
    print(url)
    response = requests.get(url, headers=headers)
    ob_json = json.loads(response.text)
    list_cards.append(ob_json['data']['cards'])
    time.sleep(5)
    print('Complete!')
# print('list_cards:',list_cards)

print(
    '\n' + 40 * '=' + '\n' + 'The number of crawling pages is: ' + str(len(list_cards)) + '.' + '\n' + 40 * '=' + '\n')

count_weibo = 0
page_weibo = 0


for cards in list_cards:
    page_weibo += 1

    for card in cards:
        count_weibo += 1
        print('Start crawling the ' + str(count_weibo) + '-th post on ' + str(page_weibo) + '-th page.')
        if card['card_type'] == 9:
            mid = card['mblog']['id']
            created_at = card['mblog']['created_at']  # The posted time.

            # 1/3 Crawl text.
            if card['mblog']['isLongText'] == 'False':  # Note: 'False' != 'false'.
                text = card['mblog']['text']
            else:
                try:
                    tmp_url = 'https://m.weibo.cn/statuses/extend?id=' + mid
                    print(mid)
                    tmp_response = requests.get(tmp_url, headers=headers)
                    ob_json = json.loads(tmp_response.text)  # ob_json (dict)
                    text = ob_json['data']['longTextContent']
                    tree = html.fromstring(text)
                    text = tree.xpath('string(.)')
                except:
                    text = "No short text extracted!"

                    # Save text.
            with open(path + user_name + txt_file_name, 'a', encoding='utf-8') as ff:
                ff.write('\n' + 'The ' + str(
                    count_weibo) + '-th weibo\n' + '***  Published on  ' + created_at + '  ***' + '\n')
                ff.write(text + '\n')

                # 2/3 Crawl JPG/GIF images.
            if 'bmiddle_pic' in card['mblog']:
                tag_post = 1  # 1 - original post.
            else:
                tag_post = 2  # 2 - re-tweeted post.

            if (tag_post == 1) or (tag_post == 2):  # Save all post.
                # Create a child folder for saving images.
                image_path = path + str(count_weibo)
                os.mkdir(image_path)

                url_extend = 'https://m.weibo.cn/status/' + mid  # URL of one Weibo.
                res = requests.get(url_extend, headers=headers).text  # <'string'>

                imgjpg_url_weibo = re.findall('https://.*large.*.jpg', res)  # Match URL of JPG images <'string'>.
                imggif_url_weibo = re.findall('https://.*large.*.gif', res)  # Match URL of GIF images <'string'>.

                # 2-1/3 Crawl JPG images.
                x_jpg = 0  # The serial number of JPG image.

                for i in range(len(imgjpg_url_weibo)):
                    x_jpg += 1

                    # Add JPG image URL to .txt file.
                    temp = image_path + '/' + str(x_jpg) + '.jpg'
                    with open(path + user_name + txt_file_name, 'a', encoding='utf-8') as ff:
                        ff.write('The link of the image is：' + imgjpg_url_weibo[i] + '\n')
                    print('Download the %s-th image.' % x_jpg)

                    # Download JPG image.
                    try:
                        urllib.request.urlretrieve(urllib.request.urlopen(imgjpg_url_weibo[i]).geturl(), temp)
                    except:
                        print("Failed to download the image: %s" % imgjpg_url_weibo[i])

                        # 2-2/3 Crawl GIF images.
                x_gif = 0  # The serial number of GIF image.

                for i in range(len(imggif_url_weibo)):
                    x_gif += 1

                    # Add GIF image URL to .txt file.
                    temp = image_path + '/' + str(x_gif) + '.gif'
                    with open(path + user_name + txt_file_name, 'a', encoding='utf-8') as ff:
                        ff.write('The link of the image is：' + imggif_url_weibo[i] + '\n')
                    print('Download the %s-th image.' % x_gif)

                    # Download GIF image.
                    try:
                        urllib.request.urlretrieve(urllib.request.urlopen(imggif_url_weibo[i]).geturl(), temp)
                    except:
                        print("Failed to download the image: %s" % imggif_url_weibo[i])

                        # 3/3 Crawl videos.
            if 'page_info' in card['mblog']:
                if 'media_info' in card['mblog'][ 'page_info']:  # Filter Weibo posts with video that has 'page_info' index.

                    # Create a child folder for saving video.
                    video_path = path + str(count_weibo) + '_video'
                    os.mkdir(video_path)
                    print(card)
                    if   card['mblog']['page_info']['media_info'].get('mp4_sd_url')!= None:
                       videourl_weibo = card['mblog']['page_info']['media_info']['mp4_sd_url']  # <'string'>
                       print(videourl_weibo)
                    # Note:
                    #     This code obtains the URL of video.
                    #     The index is manually parsed from DevTools.

                       temp = video_path + '/' + str(1) + '.mp4'
                       print('Download the video.')  # Each Weibo post only has one video.

                    # Download video.
                    try:
                        urllib.request.urlretrieve(urllib.request.urlopen(videourl_weibo).geturl(), temp)
                    except:
                        print("Failed to download the video.")

        time.sleep(6)  # Suspend * seconds after crawling data from one Weibo post.
        print('Complete!\n')

    print('Complete crawling Weibo data on ' + str(page_weibo) + '-th page!' + '\n\n' + 40 * '-' + '\n')
