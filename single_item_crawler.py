from icrawler.builtin import BaiduImageCrawler, BingImageCrawler, GoogleImageCrawler
import argparse
import os
import time

date = [(2017, 1, 1), (2018, 1, 1), (2019, 1, 1), (2019, 8, 31)]


google_crawler = None

def crawl_item(keyword, rootdir, max_num=500, language='vi'):
    '''
        max_num is used at every crawl at different time,
        so number of crawled image is max_num * len(data-1)
    '''
    global google_crawler
    storage = {'root_dir': rootdir}
    print('Starting to crawl {}'.format(keyword))
    # change the storage dir
    google_crawler = GoogleImageCrawler(
                        feeder_threads=1,
                        parser_threads=1,
                        downloader_threads=4,
                        storage=storage)
    for i in range(len(date)-1):
        try:
            google_crawler.crawl(
                keyword=keyword,
                filters={'date': (date[i], date[i+1])},
                max_num=max_num,
                file_idx_offset='auto',
                language='vi')
        except Exception as err:
            print(err)
        time.sleep(0.5)
    return

def main(keyword, rootdir, imageslimit, max_num, lang):
    global google_crawler

    item_num = len(os.listdir(rootdir))
    if item_num < imageslimit:
        crawl_item(keyword, rootdir, max_num=max_num, language=lang)
    else:
        print('Skipping {} with {} of images'.format(keyword, item_num))
    return

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-kw", "--keyword", type=str, required=True, help="Keyword to crawl")
    parser.add_argument("-rd", "--rootdir", type=str, required=True, help="Path to the save directory")
    parser.add_argument("-il", "--imageslimit", type=int, default=1000, help="Limit the data image in each folder, when you recrawl")
    parser.add_argument("-mn", "--max_num", type=int, default=300, help="Number of images to crawl each time (not the real number will be crawled)")
    parser.add_argument("-la", "--language", type=str,default = 'vi', choices=['vi', 'en', 'ja'], help="Language to crawl")
    args = parser.parse_args()
    main(args.keyword, args.rootdir, args.imageslimit, args.max_num, args.language)
    # print(crawl_list)
    # crawl_item('twice', 'test', max_num=10)
