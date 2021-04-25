import requests
import datetime

oauth_token = 'AQAAAAAFnpusAADLWxGxdPX1ykzrktKbb53gOEM'
superhero_list = ['Hulk', 'Captain America', 'Thanos']


def yandex_disc_put(file, fname_disc):
    upload_url_request = \
        'https://cloud-api.yandex.net/v1/disk/resources/upload'
    headers = {
        'Content-type': 'application/json',
        'Authorization': f'OAuth {oauth_token}'
    }
    params = {'path': fname_disc, 'overwrite': 'true'}
    answer_data = requests.get(upload_url_request,
                               headers=headers, params=params)
    link = answer_data.json().get('href')
    response = requests.put(link, data=open(file, 'rb'))
    response.raise_for_status()
    if response.status_code == 201:
        answer = 'Файл был успешно загружен'
    else:
        answer = 'Файл не был загружен'
    return answer


def get_smartest_sh(superhero_list):
    intelligence_list = []
    urlbase = "https://superheroapi.com/api/2619421814940190/search/"
    for superhero in superhero_list:
        url = urlbase + superhero
        resp = requests.get(url)
        intelligence = int(resp.json()['results'][0]['powerstats']['intelligence'])
        intelligence_list += [[intelligence, superhero]]
    smartest_sh = max(intelligence_list)
    return smartest_sh


def get_stackoverflow_questions():
    date_str = datetime.datetime.utcnow().strftime('%Y-%m-%d')
    date_timestamp_str = \
        datetime.datetime.strptime(date_str, '%Y-%m-%d').strftime("%s")
    date_deep2 = datetime.datetime.utcnow().date() - datetime.timedelta(2)
    date_deep2_str = date_deep2.strftime('%Y-%m-%d')
    date_deep2_timestamp = \
        datetime.datetime.strptime(date_deep2_str, '%Y-%m-%d').strftime("%s")
    params_base = {
        'site': 'stackoverflow', 'fromdate': date_deep2_timestamp,
        'todate': date_timestamp_str, 'tagged': 'Python', 'order': 'desc',
        'sort': 'creation'
    }
    url = 'https://api.stackexchange.com/2.2/questions/'
    work = True
    page = 1
    with open('question_base.txt', 'w') as f:
        f.write('')
    while work is True:
        params_base.update({'page': page})
        resp = requests.get(url, params=params_base)
        with open('question_base.txt', 'a') as f:
            f.write(str(resp.json()['items']))
        page += 1
        if resp.json()['has_more'] == False:
            work = False

smartest_sh = get_smartest_sh(superhero_list)
print(f'Самый умный сепергерой - {smartest_sh[1]}: {smartest_sh[0]}\n')

file = 'Python_logo.svg'
file_name_at_ydisc = 'logo_Python'
print(yandex_disc_put(file, file_name_at_ydisc))

get_stackoverflow_questions()