"""
Network requests for full week's economic calendar filtered by USA events, 2 and 3 star events
"""

"""
curl 'https://www.investing.com/economic-calendar/Service/getCalendarFilteredData' \
  -H 'accept: */*' \
  -H 'accept-language: en-US,en;q=0.9' \
  -H 'content-type: application/x-www-form-urlencoded' \
  -b 'mm-src-01jhj5jstc9w0gwx=https://mp.mmvideocdn.com/mini-player/prod/voltax_mp.js; udid=9b1a4c3c7c65fd0b8a3ddb2e8b1cc46d; inudid=9b1a4c3c7c65fd0b8a3ddb2e8b1cc46d; adBlockerNewUserDomains=1752541883; r_p_s_n=1; __eventn_id=9b1a4c3c7c65fd0b8a3ddb2e8b1cc46d; PHPSESSID=qqtvifc8fcj6e76pa5cfn723u7; page_equity_viewed=0; browser-session-counted=true; user-browser-sessions=1; reg_trk_ep=google%20one%20tap; top_strip_variant=%7B%22user_type%22%3A%22guest%22%2C%22variant_id%22%3A2%2C%22variant_name%22%3A%22Free%20users%202%2C%20SummerSale25%2C%20pricing%20page%22%7D; invab=chlngsa_2|mwebe_1|noadnews_0|noleftad_1|nostrip_0|ovlayouta_-1|regwallb_0|videoalloc_1; ses_num=4; last_smd=9b1a4c3c7c65fd0b8a3ddb2e8b1cc46d-1752766026; g_state={"i_p":1753370833706,"i_l":3}; invpc=5; __cflb=0H28vY1WcQgbwwJpSw5YiDRSJhpofbwaKURzD4HnCEY; _imntz_error=1; lifetime_page_view_count=6; geoC=US; gtmFired=OK; adsFreeSalePopUp=3; nyxDorf=MTVhMmMxPnxkMGBsbz9keDdnYjkwKTEyPTpuaA%3D%3D; smd=9b1a4c3c7c65fd0b8a3ddb2e8b1cc46d-1752894749; __cf_bm=4ZtnodzyeqomtiX1_TGWwAgR3MF.zuOVrdxkupwAxKw-1752894749-1.0.1.1-1CbxF.JNt7U_sPa.L0SWWD3aoHpGNRr_.eiv4MuDHGZA715le1wNdYv2IRFcEIQZMH5saETr7kMpBej4S6cD.RUFb6OxIfSvBpH6_Hx.7AQjMzkRGjM3aH2nj_IAaOdS; page_view_count=88; cf_clearance=dW3StZEqSlNMCJK5Nj3tn06YUpch5WFabkCfjrQnicQ-1752894750-1.2.1.1-MXG1Uo_MEAIs6KOugxRHVZl61W8t6NSqXGbxufB2C5HKx1X.Uk3KCEypCHTcYi5.X3n7p4Kd.G8s15Mg5715HLP9Q.JWVIIUDqYIGPkDBwQDYZBSXtWGqNOGKCFSwR3nd_eEKHtEigSXHhWPtMswzdfNP.FLgqmBPY2hUatWoqzdMLgAhiZ1faa9gLZS5TlPamLO1I1wY_hSXDdxHYcvzTS70WNFiz_aqvx.3naJrRo' \
  -H 'dnt: 1' \
  -H 'origin: https://www.investing.com' \
  -H 'priority: u=1, i' \
  -H 'referer: https://www.investing.com/economic-calendar/' \
  -H 'sec-ch-ua: "Not)A;Brand";v="8", "Chromium";v="138"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "macOS"' \
  -H 'sec-fetch-dest: empty' \
  -H 'sec-fetch-mode: cors' \
  -H 'sec-fetch-site: same-origin' \
  -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36' \
  -H 'x-requested-with: XMLHttpRequest' \
  --data-raw 'country%5B%5D=5&category%5B%5D=_employment&category%5B%5D=_economicActivity&category%5B%5D=_inflation&category%5B%5D=_credit&category%5B%5D=_centralBanks&category%5B%5D=_confidenceIndex&category%5B%5D=_balance&category%5B%5D=_Bonds&importance%5B%5D=2&importance%5B%5D=3&timeZone=8&timeFilter=timeRemain&currentTab=thisWeek&submitFilters=1&limit_from=0'
"""

cookies = {
    'mm-src-01jhj5jstc9w0gwx': 'https://mp.mmvideocdn.com/mini-player/prod/voltax_mp.js',
    'udid': '9b1a4c3c7c65fd0b8a3ddb2e8b1cc46d',
    'inudid': '9b1a4c3c7c65fd0b8a3ddb2e8b1cc46d',
    'adBlockerNewUserDomains': '1752541883',
    'r_p_s_n': '1',
    '__eventn_id': '9b1a4c3c7c65fd0b8a3ddb2e8b1cc46d',
    'PHPSESSID': 'qqtvifc8fcj6e76pa5cfn723u7',
    'page_equity_viewed': '0',
    'browser-session-counted': 'true',
    'user-browser-sessions': '1',
    'reg_trk_ep': 'google%20one%20tap',
    'top_strip_variant': '%7B%22user_type%22%3A%22guest%22%2C%22variant_id%22%3A2%2C%22variant_name%22%3A%22Free%20users%202%2C%20SummerSale25%2C%20pricing%20page%22%7D',
    'invab': 'chlngsa_2|mwebe_1|noadnews_0|noleftad_1|nostrip_0|ovlayouta_-1|regwallb_0|videoalloc_1',
    'ses_num': '4',
    'last_smd': '9b1a4c3c7c65fd0b8a3ddb2e8b1cc46d-1752766026',
    'g_state': '{"i_p":1753370833706,"i_l":3}',
    'invpc': '5',
    '__cflb': '0H28vY1WcQgbwwJpSw5YiDRSJhpofbwaKURzD4HnCEY',
    '_imntz_error': '1',
    'lifetime_page_view_count': '6',
    'geoC': 'US',
    'gtmFired': 'OK',
    'adsFreeSalePopUp': '3',
    'nyxDorf': 'MTVhMmMxPnxkMGBsbz9keDdnYjkwKTEyPTpuaA%3D%3D',
    'smd': '9b1a4c3c7c65fd0b8a3ddb2e8b1cc46d-1752894749',
    '__cf_bm': '4ZtnodzyeqomtiX1_TGWwAgR3MF.zuOVrdxkupwAxKw-1752894749-1.0.1.1-1CbxF.JNt7U_sPa.L0SWWD3aoHpGNRr_.eiv4MuDHGZA715le1wNdYv2IRFcEIQZMH5saETr7kMpBej4S6cD.RUFb6OxIfSvBpH6_Hx.7AQjMzkRGjM3aH2nj_IAaOdS',
    'page_view_count': '88',
    'cf_clearance': 'dW3StZEqSlNMCJK5Nj3tn06YUpch5WFabkCfjrQnicQ-1752894750-1.2.1.1-MXG1Uo_MEAIs6KOugxRHVZl61W8t6NSqXGbxufB2C5HKx1X.Uk3KCEypCHTcYi5.X3n7p4Kd.G8s15Mg5715HLP9Q.JWVIIUDqYIGPkDBwQDYZBSXtWGqNOGKCFSwR3nd_eEKHtEigSXHhWPtMswzdfNP.FLgqmBPY2hUatWoqzdMLgAhiZ1faa9gLZS5TlPamLO1I1wY_hSXDdxHYcvzTS70WNFiz_aqvx.3naJrRo',
}

headers = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'content-type': 'application/x-www-form-urlencoded',
    'dnt': '1',
    'origin': 'https://www.investing.com',
    'priority': 'u=1, i',
    'referer': 'https://www.investing.com/economic-calendar/',
    'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
    # 'cookie': 'mm-src-01jhj5jstc9w0gwx=https://mp.mmvideocdn.com/mini-player/prod/voltax_mp.js; udid=9b1a4c3c7c65fd0b8a3ddb2e8b1cc46d; inudid=9b1a4c3c7c65fd0b8a3ddb2e8b1cc46d; adBlockerNewUserDomains=1752541883; r_p_s_n=1; __eventn_id=9b1a4c3c7c65fd0b8a3ddb2e8b1cc46d; PHPSESSID=qqtvifc8fcj6e76pa5cfn723u7; page_equity_viewed=0; browser-session-counted=true; user-browser-sessions=1; reg_trk_ep=google%20one%20tap; top_strip_variant=%7B%22user_type%22%3A%22guest%22%2C%22variant_id%22%3A2%2C%22variant_name%22%3A%22Free%20users%202%2C%20SummerSale25%2C%20pricing%20page%22%7D; invab=chlngsa_2|mwebe_1|noadnews_0|noleftad_1|nostrip_0|ovlayouta_-1|regwallb_0|videoalloc_1; ses_num=4; last_smd=9b1a4c3c7c65fd0b8a3ddb2e8b1cc46d-1752766026; g_state={"i_p":1753370833706,"i_l":3}; invpc=5; __cflb=0H28vY1WcQgbwwJpSw5YiDRSJhpofbwaKURzD4HnCEY; _imntz_error=1; lifetime_page_view_count=6; geoC=US; gtmFired=OK; adsFreeSalePopUp=3; nyxDorf=MTVhMmMxPnxkMGBsbz9keDdnYjkwKTEyPTpuaA%3D%3D; smd=9b1a4c3c7c65fd0b8a3ddb2e8b1cc46d-1752894749; __cf_bm=4ZtnodzyeqomtiX1_TGWwAgR3MF.zuOVrdxkupwAxKw-1752894749-1.0.1.1-1CbxF.JNt7U_sPa.L0SWWD3aoHpGNRr_.eiv4MuDHGZA715le1wNdYv2IRFcEIQZMH5saETr7kMpBej4S6cD.RUFb6OxIfSvBpH6_Hx.7AQjMzkRGjM3aH2nj_IAaOdS; page_view_count=88; cf_clearance=dW3StZEqSlNMCJK5Nj3tn06YUpch5WFabkCfjrQnicQ-1752894750-1.2.1.1-MXG1Uo_MEAIs6KOugxRHVZl61W8t6NSqXGbxufB2C5HKx1X.Uk3KCEypCHTcYi5.X3n7p4Kd.G8s15Mg5715HLP9Q.JWVIIUDqYIGPkDBwQDYZBSXtWGqNOGKCFSwR3nd_eEKHtEigSXHhWPtMswzdfNP.FLgqmBPY2hUatWoqzdMLgAhiZ1faa9gLZS5TlPamLO1I1wY_hSXDdxHYcvzTS70WNFiz_aqvx.3naJrRo',
}

data = {
    'country[]': '5',
    'category[]': [
        '_employment',
        '_economicActivity',
        '_inflation',
        '_credit',
        '_centralBanks',
        '_confidenceIndex',
        '_balance',
        '_Bonds',
    ],
    'importance[]': [
        '2',
        '3',
    ],
    'timeZone': '8',
    'timeFilter': 'timeRemain',
    'currentTab': 'thisWeek',
    'submitFilters': '1',
    'limit_from': '0',
}