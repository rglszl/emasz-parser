import json

import requests
from bs4 import BeautifulSoup
from datetime import datetime

USERNAME = ""
PASSWORD = ""
MEROORA_AZONOSITO = ""

def get_data_from_url(date, session, sap_contextid, sap_appcontext):
    date_formatted = date.strftime("%Y-%m-%d")
    date_formatted = "2022-12-27"
    cookies = {
        'sap-contextid': session.cookies.get_dict()["sap-contextid"],
        'sap-appcontext': session.cookies.get_dict()["sap-appcontext"],
        'cookiePanelAccepted': '1',
        'cookieMarketingAccepted': '1',
        'cookieSocialAccepted': '1',
        'sap-usercontext': 'sap-language=HU&sap-client=100',
    }

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'hu,en-US;q=0.9,en;q=0.8,es;q=0.7',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'DNT': '1',
        'Origin': 'https://eloszto.mvmemaszhalozat.hu',
        'Referer': 'https://eloszto.mvmemaszhalozat.hu/SMMU(bD1odSZjPTEwMA==)/Oldal_3.htm',
        'Sec-Fetch-Dest': 'frame',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
    }

    data = {
        'azonosito': MEROORA_AZONOSITO,
        'tipus': 'Fogyasztás',
        'idoszak_tol_mero': date_formatted,
        'idoszak_ig_mero': date_formatted,
        'mertekegyseg': 'kWh',
        'profil': 'KIS_LAKOSSAG',
        'OnInputProcessing(elkuld)': 'Adatok frissítése',
    }

    response = session.post(
        'https://eloszto.mvmemaszhalozat.hu/SMMU(bD1odSZjPTEwMA==)/Oldal_3.htm',
        cookies=cookies,
        headers=headers,
        data=data,
    )

    return response.text


def get_token():
    session = requests.Session()

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'hu,en-US;q=0.9,en;q=0.8,es;q=0.7',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'DNT': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
    }

    response = session.get('https://eloszto.mvmemaszhalozat.hu/usz(bD1odSZjPTExMg==)/dso/mvm/index.html',
                            headers=headers)
    sap_appcontext = response.cookies.get_dict()["sap-appcontext"]

    cookies = {
        'sap-usercontext': 'sap-language=HU&sap-client=112',
    }

    headers = {
        'Accept': 'application/json',
        'Accept-Language': 'hu,en-US;q=0.9,en;q=0.8,es;q=0.7',
        'Connection': 'keep-alive',
        # 'Cookie': 'sap-usercontext=sap-language=HU&sap-client=112',
        'DNT': '1',
        'Referer': 'https://eloszto.mvmemaszhalozat.hu/usz(bD1odSZjPTExMg==)/dso/mvm/index.html',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
    }

    params = {
        'sap-client': '112',
        'sap-language': 'HU',
    }

    response = session.get(
        'https://eloszto.mvmemaszhalozat.hu/sap/opu/odata/sap/ZGW_UGYFELSZLG_CMS_NO_AUTH_SRV/CookieTokenek',
        params=params,
        cookies=cookies,
        headers=headers,
    )

    ga_token = json.loads(response.text)["d"]["results"][0]["GAToken"]

    cookies = {
        'cookiePanelAccepted': '1',
        'cookieMarketingAccepted': '1',
        'cookieSocialAccepted': '1',
        'sap-usercontext': 'sap-language=HU&sap-client=112',
    }

    headers = {
        'Accept': 'application/json',
        'Accept-Language': 'hu,en-US;q=0.9,en;q=0.8,es;q=0.7',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',        'DNT': '1',
        'Origin': 'https://eloszto.mvmemaszhalozat.hu',
        'Referer': 'https://eloszto.mvmemaszhalozat.hu/usz(bD1odSZjPTExMg==)/dso/mvm/index.html',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'X-Requested-With': 'X',
        'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
    }

    params = {
        'sap-client': '112',
        'sap-language': 'HU',
    }

    json_data = {
        'Username': USERNAME,
        'Password': PASSWORD,
    }

    response = session.post(
        'https://eloszto.mvmemaszhalozat.hu/sap/opu/odata/sap/ZGW_UGYFELSZOLGALAT_LOGIN_SRV/Login',
        params=params,
        cookies=cookies,
        headers=headers,
        json=json_data,
    )
    auth_code = json.loads(response.text)["d"]["AuthCode"]

    cookies = {
        'cookiePanelAccepted': '1',
        'cookieMarketingAccepted': '1',
        'cookieSocialAccepted': '1',
        'sap-usercontext': 'sap-language=HU&sap-client=112',
    }

    headers = {
        'Accept': 'application/json',
        'Accept-Language': 'hu,en-US;q=0.9,en;q=0.8,es;q=0.7',
        'Connection': 'keep-alive',
        'DNT': '1',
        'Referer': 'https://eloszto.mvmemaszhalozat.hu/usz(bD1odSZjPTExMg==)/dso/mvm/index.html',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
    }

    params = {
        'Code': f"'{auth_code}'",
        'sap-client': '112',
        'sap-language': 'HU',
    }

    response = session.get(
        'https://eloszto.mvmemaszhalozat.hu/sap/opu/odata/sap/ZGW_OAUTH_SRV/GetToken',
        params=params,
        cookies=cookies,
        headers=headers,
    )

    token_code = json.loads(response.text)["d"]["GetToken"]["TokenCode"]
    renew_token = json.loads(response.text)["d"]["GetToken"]["RenewToken"]

    cookies = {
        'cookiePanelAccepted': '1',
        'cookieMarketingAccepted': '1',
        'cookieSocialAccepted': '1',
        'sap-usercontext': 'sap-language=HU&sap-client=112',
    }

    headers = {
        'Accept': 'application/json',
        'Accept-Language': 'hu,en-US;q=0.9,en;q=0.8,es;q=0.7',
        'Authorization': 'Bearer ' + token_code,
        'Connection': 'keep-alive',
        'DNT': '1',
        'Referer': 'https://eloszto.mvmemaszhalozat.hu/usz(bD1odSZjPTExMg==)/dso/mvm/index.html',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
    }

    params = {
        'sap-client': '112',
        'sap-language': 'HU',
    }

    response = session.get(
        'https://eloszto.mvmemaszhalozat.hu/sap/opu/odata/sap/ZGW_UGYFELSZOLGALAT_SRV/Felhelyek(Vevo%3D%274501026937%27%2CId%3D%2720481319%27)/Okosmero',
        params=params,
        cookies=cookies,
        headers=headers,
    )
    url=""
    guid = ""
    sap_client=""
    for item in json.loads(response.text)["d"]["results"]:
        if MEROORA_AZONOSITO in item["FogyMeroAzon"]:
            url = item["URL"]
            guid_start = url.find("guid")+5
            guid_end = url[guid_start:].find("&")
            guid = url[guid_start:guid_start+guid_end]

            sap_client_start = url.find("sap-client")+11
            sap_client = url[sap_client_start:]

    cookies = {
        'sap-usercontext': 'sap-language=HU&sap-client=112',
        'cookiePanelAccepted': '1',
        'cookieMarketingAccepted': '1',
        'cookieSocialAccepted': '1',
    }

    headers = {
        'Accept': 'application/json',
        'Accept-Language': 'hu,en-US;q=0.9,en;q=0.8,es;q=0.7',
        'Authorization': 'Bearer ' + token_code,
        'Connection': 'keep-alive',
        # 'Cookie': 'sap-usercontext=sap-language=HU&sap-client=112; cookiePanelAccepted=1; cookieMarketingAccepted=1; cookieSocialAccepted=1',
        'DNT': '1',
        'Referer': 'https://eloszto.mvmemaszhalozat.hu/usz(bD1odSZjPTExMg==)/dso/mvm/index.html',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
    }

    params = {
        'Funkcio': 'OKOSMERO',
        'sap-client': '112',
        'sap-language': 'HU',
    }

    response = requests.get(
        'https://eloszto.mvmemaszhalozat.hu/sap/opu/odata/sap/ZGW_UGYFELSZOLGALAT_SRV/Vevok(%274501026937%27)/Felhelyek',
        params=params,
        cookies=cookies,
        headers=headers,
    )



    cookies = {
        'sap-usercontext': 'sap-language=HU&sap-client='+sap_client,
        'cookiePanelAccepted': '1',
        'cookieMarketingAccepted': '1',
        'cookieSocialAccepted': '1',
    }

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'hu,en-US;q=0.9,en;q=0.8,es;q=0.7',
        'Connection': 'keep-alive',
        # 'Cookie': 'sap-usercontext=sap-language=HU&sap-client=112; cookiePanelAccepted=1; cookieMarketingAccepted=1; cookieSocialAccepted=1',
        'DNT': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
    }

    params = {
        'guid': guid,
        'sap-client': sap_client,
    }


    response = session.get('https://eloszto.mvmemaszhalozat.hu/SMMU', params=params, cookies=cookies, headers=headers)

    cookies = {
        'cookiePanelAccepted': '1',
        'cookieMarketingAccepted': '1',
        'cookieSocialAccepted': '1',
        'sap-usercontext': 'sap-language=HU&sap-client='+sap_client,
    }

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'hu,en-US;q=0.9,en;q=0.8,es;q=0.7',
        'Connection': 'keep-alive',
        # 'Cookie': 'cookiePanelAccepted=1; cookieMarketingAccepted=1; cookieSocialAccepted=1; sap-usercontext=sap-language=HU&sap-client=100',
        'DNT': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
    }

    params = {
        'guid': guid,
    }

    response = session.get(
        'https://eloszto.mvmemaszhalozat.hu/SMMU(bD1odSZjPTEwMA==)/belepes.htm',
        params=params,
        cookies=cookies,
        headers=headers,
    )

    sap_contextid = session.cookies.get_dict()["sap-contextid"]
    #sap_appcontext = session.cookies.get_dict()["sap-appcontext"]

    cookies = {
        'sap-contextid': sap_contextid,
        'sap-appcontext': sap_appcontext,
        'cookiePanelAccepted': '1',
        'cookieMarketingAccepted': '1',
        'cookieSocialAccepted': '1',
        'sap-usercontext': 'sap-language=HU&sap-client='+sap_client,
    }

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'hu,en-US;q=0.9,en;q=0.8,es;q=0.7',
        'Connection': 'keep-alive',
        # 'Cookie': 'sap-contextid=SID%3aANON%3aneppasascs_NEP_01%3anU1BTfviN_AQoSOdULwPvqEN1GJ3mKTKuPJIgjeG-NEW; sap-appcontext=c2FwLXNlc3Npb25pZD1TSUQlM2FBTk9OJTNhbmVwcGFzYXNjc19ORVBfMDElM2FuVTFCVGZ2aU5fQVFvU09kVUx3UHZxRU4xR0ozbUtUS3VQSklnamVHLUFUVA%3d%3d; cookiePanelAccepted=1; cookieMarketingAccepted=1; cookieSocialAccepted=1; sap-usercontext=sap-language=HU&sap-client=100',
        'DNT': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
    }

    params = {
        'guid': guid,
        'sap-sessioncmd': 'open',
    }

    response = session.get(
        'https://eloszto.mvmemaszhalozat.hu/SMMU(bD1odSZjPTEwMA==)/belepes.htm',
        params=params,
        cookies=cookies,
        headers=headers,
    )




    cookies = {
        'cookiePanelAccepted': '1',
        'cookieMarketingAccepted': '1',
        'cookieSocialAccepted': '1',
        'sap-usercontext': 'sap-language=HU&sap-client='+sap_client,
    }

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'hu,en-US;q=0.9,en;q=0.8,es;q=0.7',
        'Connection': 'keep-alive',
        # 'Cookie': 'cookiePanelAccepted=1; cookieMarketingAccepted=1; cookieSocialAccepted=1; sap-usercontext=sap-language=HU&sap-client=100',
        'DNT': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
    }

    params = {
        'guid': guid,
    }

    response = session.get(
        'https://eloszto.mvmemaszhalozat.hu/SMMU(bD1odSZjPTEwMA==)/belepes.htm',
        params=params,
        cookies=cookies,
        headers=headers,
    )

    #sap_contextid = session.cookies.get_dict()["sap-contextid"]
    #sap_appcontext = session.cookies.get_dict()["sap-appcontext"]

    cookies = {
        'sap-contextid': sap_contextid,
        'sap-appcontext': sap_appcontext,
        'cookiePanelAccepted': '1',
        'cookieMarketingAccepted': '1',
        'cookieSocialAccepted': '1',
        'sap-usercontext': 'sap-language=HU&sap-client='+sap_client,
    }

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'hu,en-US;q=0.9,en;q=0.8,es;q=0.7',
        'Connection': 'keep-alive',
        # 'Cookie': 'sap-contextid=SID%3aANON%3aneppasascs_NEP_01%3anU1BcXAcfx9rmR0s0WeAWrSD10t2mKS37PIqiN34-NEW; sap-appcontext=c2FwLXNlc3Npb25pZD1TSUQlM2FBTk9OJTNhbmVwcGFzYXNjc19ORVBfMDElM2FuVTFCY1hBY2Z4OXJtUjBzMFdlQVdyU0QxMHQybUtTMzdQSXFpTjM0LUFUVA%3d%3d; cookiePanelAccepted=1; cookieMarketingAccepted=1; cookieSocialAccepted=1; sap-usercontext=sap-language=HU&sap-client=100',
        'DNT': '1',
        'Referer': 'https://eloszto.mvmemaszhalozat.hu/SMMU(bD1odSZjPTEwMA==)/belepes.htm?guid=' + guid,
        'Sec-Fetch-Dest': 'frame',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
    }

    response = session.get(
        'https://eloszto.mvmemaszhalozat.hu/SMMU(bD1odSZjPTEwMA==)/oldal_1.htm',
        cookies=cookies,
        headers=headers,
    )

    #sap_contextid = session.cookies.get_dict()["sap-contextid"]
    #sap_appcontext = session.cookies.get_dict()["sap-appcontext"]

    cookies = {
        'sap-contextid': sap_contextid,
        'sap-appcontext': sap_appcontext,
        'cookiePanelAccepted': '1',
        'cookieMarketingAccepted': '1',
        'cookieSocialAccepted': '1',
        'sap-usercontext': 'sap-language=HU&sap-client='+sap_client,
    }

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'hu,en-US;q=0.9,en;q=0.8,es;q=0.7',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        # 'Cookie': 'sap-contextid=SID%3aANON%3aneppasascs_NEP_01%3anU1BcXAcfx9rmR0s0WeAWrSD10t2mKS37PIqiN34-NEW; sap-appcontext=c2FwLXNlc3Npb25pZD1TSUQlM2FBTk9OJTNhbmVwcGFzYXNjc19ORVBfMDElM2FuVTFCY1hBY2Z4OXJtUjBzMFdlQVdyU0QxMHQybUtTMzdQSXFpTjM0LUFUVA%3d%3d; cookiePanelAccepted=1; cookieMarketingAccepted=1; cookieSocialAccepted=1; sap-usercontext=sap-language=HU&sap-client=100',
        'DNT': '1',
        'Origin': 'https://eloszto.mvmemaszhalozat.hu',
        'Referer': 'https://eloszto.mvmemaszhalozat.hu/SMMU(bD1odSZjPTEwMA==)/oldal_1.htm',
        'Sec-Fetch-Dest': 'frame',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
    }

    data = {
        'accept': 'on',
        'OnInputProcessing(tovabb)': '',
    }

    response = session.post(
        'https://eloszto.mvmemaszhalozat.hu/SMMU(bD1odSZjPTEwMA==)/oldal_1.htm',
        cookies=cookies,
        headers=headers,
        data=data,
    )



    """_________________________"""
    #sap_contextid = session.cookies.get_dict()["sap-contextid"]
    #sap_appcontext = session.cookies.get_dict()["sap-appcontext"]

    cookies = {
        'sap-contextid': sap_contextid,
        'sap-appcontext': sap_appcontext,
        'cookiePanelAccepted': '1',
        'cookieMarketingAccepted': '1',
        'cookieSocialAccepted': '1',
        'sap-usercontext': 'sap-language=HU&sap-client='+sap_client,
    }

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'hu,en-US;q=0.9,en;q=0.8,es;q=0.7',
        'Connection': 'keep-alive',
        # 'Cookie': 'sap-contextid=SID%3aANON%3aneppasascs_NEP_01%3anU1BLzE7oWqc11gVVlCwFXN2ZCl3mKQQlfIboshO-NEW; sap-appcontext=c2FwLXNlc3Npb25pZD1TSUQlM2FBTk9OJTNhbmVwcGFzYXNjc19ORVBfMDElM2FuVTFCTHpFN29XcWMxMWdWVmxDd0ZYTjJaQ2wzbUtRUWxmSWJvc2hPLUFUVA%3d%3d; cookiePanelAccepted=1; cookieMarketingAccepted=1; cookieSocialAccepted=1; sap-usercontext=sap-language=HU&sap-client=100',
        'DNT': '1',
        'Referer': 'https://eloszto.mvmemaszhalozat.hu/SMMU(bD1odSZjPTEwMA==)/Oldal_2.htm',
        'Sec-Fetch-Dest': 'frame',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
    }

    response = session.get(
        'https://eloszto.mvmemaszhalozat.hu/SMMU(bD1odSZjPTEwMA==)/Oldal_2.htm?OnInputProcessing(ToTerhGor1)',
        cookies=cookies,
        headers=headers,
    )

    #sap_contextid = session.cookies.get_dict()["sap-contextid"]
    #sap_appcontext = session.cookies.get_dict()["sap-appcontext"]

    cookies = {
        'sap-contextid': sap_contextid,
        'sap-appcontext': sap_appcontext,
        'cookiePanelAccepted': '1',
        'cookieMarketingAccepted': '1',
        'cookieSocialAccepted': '1',
        'sap-usercontext': 'sap-language=HU&sap-client='+sap_client,
    }

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'hu,en-US;q=0.9,en;q=0.8,es;q=0.7',
        'Connection': 'keep-alive',
        # 'Cookie': 'sap-contextid=SID%3aANON%3aneppasascs_NEP_01%3anU1BTcShbhuY1pbVoPDQ7woeEC53mKQ8_fJyifSB-NEW; sap-appcontext=c2FwLXNlc3Npb25pZD1TSUQlM2FBTk9OJTNhbmVwcGFzYXNjc19ORVBfMDElM2FuVTFCVGNTaGJodVkxcGJWb1BEUTd3b2VFQzUzbUtROF9mSnlpZlNCLUFUVA%3d%3d; cookiePanelAccepted=1; cookieMarketingAccepted=1; cookieSocialAccepted=1; sap-usercontext=sap-language=HU&sap-client=100',
        'DNT': '1',
        'Referer': 'https://eloszto.mvmemaszhalozat.hu/SMMU(bD1odSZjPTEwMA==)/Oldal_2.htm',
        'Sec-Fetch-Dest': 'frame',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
    }

    response = session.get(
        'https://eloszto.mvmemaszhalozat.hu/SMMU(bD1odSZjPTEwMA==)/Oldal_3.htm',
        cookies=cookies,
        headers=headers,
    )

    return session, sap_contextid, sap_appcontext



if __name__ == '__main__':
    session, sap_contextid, sap_appcontext = get_token()
    page = get_data_from_url(datetime.now(), session, sap_contextid, sap_appcontext)
    soup = BeautifulSoup(page, "html.parser")
    script = soup.findAll("script")[-1]
    data_index = 0
    start_timestamp = 0
    for index, row in enumerate(script.text.split('\r\n')):
        if "Hálózatból vételezett" in row:
            data_index = index+1
        if "pointStart" in row:
            start_timestamp = int(row.replace("pointStart: ", "").replace(",", "").strip())
    data = json.loads(script.text.split('\r\n')[data_index].replace("data: ", "").strip()[:-1])
    data_with_timestamp = []
    for index, item in enumerate(data):
        data_with_timestamp.append({
            "value": item["y"],
            "timestamp": datetime.fromtimestamp(int(start_timestamp/1000 + index * 900))
        })

    print(data_with_timestamp)

    sum = 0
    for item in data_with_timestamp:
        print(item)
        sum = sum + item["value"]

    print(sum)
