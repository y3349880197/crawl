import csv
import re

from lxml import html
from curl_cffi import requests as crequests

TMDB_BASE_URL = "https://www.themoviedb.org"
TMDB_TOP_URL = "https://www.themoviedb.org/movie/top-rated"
TMDB_TOP_URL_1 = "https://www.themoviedb.org/discover/movie/items"

def get_films_info(films_list):
    films_info = []
    for film in films_list:
        print(f"正在获取{film}信息")
        film_resp = crequests.get(film,params={"language": "zh-CN"})
        film_doc = html.fromstring(film_resp.text)

        #"电影名", "年份", "上映时间", "类型", "时长", "评分", "语言", "主演", "简介"
        film_name = film_doc.xpath('//*[@id="original_header"]/div[2]/section/div[1]/h2/a/text()')
        film_name = film_name[0].strip() if film_name else ""
        year_raw = film_doc.xpath('//*[@id="original_header"]/div[2]/section/div[1]/h2/span/text()')
        year_match = re.search(r"\d{4}", year_raw[0].strip()) if year_raw else None
        year = year_match.group() if year_match else ""

        date_raw = film_doc.xpath('//*[@id="original_header"]/div[2]/section/div[1]/div/span[2]/text()')
        date_match = re.search(r"\d{4}-\d{2}-\d{2}", date_raw[0].strip()) if date_raw else None
        date = date_match.group() if date_match else ""
        a_list = film_doc.xpath('//*[@id="original_header"]/div[2]/section/div[1]/div/span[3]/a')
        genres = []
        for a in a_list:
            text = a.xpath("./text()")
            if text:
                genres.append(text[0])
        genres_str = " / ".join(genres)
        runtime = film_doc.xpath('//*[@id="original_header"]/div[2]/section/div[1]/div/span[4]/text()')
        runtime = runtime[0].strip() if runtime else ""
        percent = film_doc.xpath('//*[@id="consensus_pill"]/div/div[1]/div/div/@data-percent')
        percent = percent[0].strip() if percent else ""
        language = film_doc.xpath('//*[@id="media_v4"]/div/div/div[2]/div/section/div[1]/div/section[1]/p[3]/text()')
        language = language[0].strip() if language else ""
        profiles_list = film_doc.xpath('//*[@id="original_header"]/div[2]/section/div[3]/ol/li')
        characters_list = []
        for profile in profiles_list:
            names = profile.xpath("./p[1]/a/text()")
            if names:
                characters_list.append(names[0])
        characters_str = " / ".join(characters_list)
        overview = film_doc.xpath('//*[@id="original_header"]/div[2]/section/div[3]/div/p/text()')
        overview = overview[0].strip() if overview else ""
        films = {"电影名": film_name, "年份": year, "上映时间": date, "类型": genres_str, "时长": runtime,
                 "评分": percent, "语言": language, "主演": characters_str,
                 "简介": overview}
        films_info.append(films)
    return films_info



def save_films(films):
    with open("csv_data/films.csv", "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["电影名", "年份", "上映时间", "类型", "时长", "评分", "语言",
                                               "主演", "简介"])
        writer.writeheader()
        writer.writerows(films)

def main():
    films_src = []
    for page_num in range(1, 6):
        if page_num == 1:
            response = crequests.get(TMDB_TOP_URL, timeout=60)
        else:
            response = crequests.post(TMDB_TOP_URL_1,
                                     data = f"air_date.gte=&air_date.lte=&certification=&certification_country=SG&debug=&first_air_date.gte=&first_air_date.lte=&include_adult=false&include_softcore=false&latest_ceremony.gte=&latest_ceremony.lte=&page={page_num}&primary_release_date.gte=&primary_release_date.lte=&region=&release_date.gte=&release_date.lte=&show_me=everything&sort_by=vote_average.desc&vote_average.gte=0&vote_average.lte=10&vote_count.gte=300&vote_count.lte=&watch_region=SG&with_genres=&with_keywords=&with_networks=&with_origin_country=&with_original_language=&with_watch_monetization_types=&with_watch_providers=&with_release_type=&with_runtime.gte=0&with_runtime.lte=400&view=&discover_preset=top-rated".encode("utf-8")
                                     , timeout=60)

        document = html.fromstring(response.text)


        srcs = document.xpath("//a[@class='flex w-full']")
        for src in srcs:
            films_src.append(TMDB_BASE_URL+src.get("href"))

    films_info = get_films_info(films_src)
    print(films_info)
    save_films(films_info)



if __name__ == '__main__':
    main()