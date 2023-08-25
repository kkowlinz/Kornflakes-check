import os, requests, bs4
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem
os.system("taskkill /F /IM chrome.exe /T")
import util.UndetectDriver as UDriver

def getHeaders():
    software_names = [SoftwareName.CHROME.value]
    operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value]   
    user_agent_rotator = UserAgent(software_names=software_names, operating_systems=operating_systems, limit=10)
    user_agents = user_agent_rotator.get_user_agents()
    user_agent = user_agent_rotator.get_random_user_agent()
    return {"User-Agent" : user_agent}

NAME_PROFILE = "@supernixxx"

os.makedirs((NAME_PROFILE + "/Video"),exist_ok=True)
UDriver.get_page(f"https://www.tiktok.com/{NAME_PROFILE}")
UDriver.scroll_page_to_the_end()
soup = UDriver.get_soup()
all_image_soup = soup.find_all("a")
all_video_link = []
for element in all_image_soup:
    try:
        PRE_LINK = str(element.get("href"))
        if ( NAME_PROFILE in PRE_LINK and "video" in PRE_LINK ):
            all_video_link.append(element.get("href"))
    except: pass
print("Video find", len(all_video_link))

def download_video_2(url):

    ID_VIDEO = str(url).split("/")[-1]
    session = requests.Session()
    server_url = 'https://musicaldown.com/'
    headers = {
        'authority': 'musicaldown.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7',
        'dnt': '1',
        'sec-ch-ua': '"Not?A_Brand";v="99", "Opera";v="97", "Chromium";v="111"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': getHeaders()["User-Agent"]
    }
    session.headers.update(headers)
    request = session.get(server_url)
    data = {}
    parse = bs4.BeautifulSoup(request.text, 'html.parser')
    get_all_input = parse.findAll('input')
    for i in get_all_input:
        if i.get("id") == "link_url":
            data[i.get("name")] = url
        else:
            data[i.get("name")] = i.get("value")
    post_url = server_url + "id/download"
    req_post = session.post(post_url, data=data, allow_redirects=True)
    print(req_post.url)
    print("Post response = ", str(req_post.status_code))
    get_all_blank = bs4.BeautifulSoup(req_post.text, 'html.parser').findAll('a', attrs={'target': '_blank'})
    download_link = get_all_blank[0].get('href')
    get_content = requests.get(download_link, headers = getHeaders(), allow_redirects = True)
    print("Download response = ", str(get_content.status_code))
    open(NAME_PROFILE + "/Video/" + ID_VIDEO + ".mp4", 'wb').write(get_content.content)
    print("\n")

for i in range(len(all_video_link)):
    print("GET", str(all_video_link[i]).split("\\")[-1], "N.", str(i), "of", str(len(all_video_link)))
    download_video_2(all_video_link[i])

print("END")
UDriver.close_driver()