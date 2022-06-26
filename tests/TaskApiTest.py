import json
from yiban import Task
task_data = {
    "WFId": "",
    "Data": {
        "9843754e97aad058523524bdb8991bcd": "否",
        "72fe9c2c81a48fd0968edbbb3f2c1c42": "36.5",
        "769bbfbfb026629f1ddb0294a9c0d257": "",
        "90b5b83950ae456fefebb0f751406e2d": [{
            "name": "348816E7-275F-42D8-9118-625FB45D8D48.png",
            "type": "image/png",
            "size ": 472092,
            "status": "done",
            "percent ": 100,
            "fileName": "workflow/202110/18/4c3599675b629e14e80ffe19c507b806.png ",
            "path": "workflow/202110/18/4c3599675b629e14e80ffe19c507b806.png "
        }],
        "0242914b8746275c5073ccdb156f9d1d": [{
            "name": "86E7DCB9-7FEE-441F-B921-039302A1048B.png",
            "type": "image/png",
            "size": 179394,
            "status": "done",
            "percent": 100,
            "fileName": "workflow/202110/23/30150ea922a720e7fb732eb7150cc532.png ",
            "path": "workflow/202110/23/30150ea922a720e7fb732eb7150cc532.png "
        }],
        "1bac180dd37455f7c16a36336c0411a8": {
            "time": "2022-05-20 00:00",
            "longitude": 0,
            "latitude": 0,
            "address": ""
        }
    },

    "Extend": {
        "TaskId": "",
        "title": "任务信息",
        "content": [
            {"label": "任务名称", "value": ""},
            {"label": "发布机构", "value": ""},
            {"label": "发布人", "value": ""}
        ]
    }
}

Str = 'SkJsUnR1ZGFUMitSMGZMYUZKcm5qM3doSnlnSW0vWXA3L1pvcjNzUkEzRVlvKzhrT1lXTHRHZi91c1BNOHRzMFZwVS91WlhsdW1yaUNJUzJHYVF0RUY1VjdaK1JDZmlXS0t3R2RsT1NQajlyR3dzdVVIZ1VTWkl1UmpjY0srNk01VDlxY09OMFBUZXZtTVQrYmNQcEVsS3RGOEdDNHNoOE5MM01wVDh2V2R4c092N3l4L0Y2TGp0UWxzSk95Q0tQY1kyc25HVTBBSlUxYjBQY25EMzUwM0xSVGZyblJ6blhERkZDemdvbE10WGhVZ3lrSmpPUnhFZHo3bCtlZFZOMkhZWEhOY3poWjZBYUxDYndvM1ZDaXg0OTJpYlV1aGZGc0RBZ3FLR1NJNEJmbkk3NmJwR2FCNUtJNitMTVQ0d2hnWVQyRTRka25yWlVsTUFHQ2hNb0w1K2l5UmxGaG1pbjc1aU91eWQ2TnFZVUFuUk95YXI5cWtxQ2RxUFY2TzRSUkRqMWdsaEE5Zmtsa0c5MmczRkkxbE5YNGhOMDQ5ZU5JUUlKNGJPeTRpcWxVRC82dG1VYnZtY1dzT1hMaVBjYmJzKzNrSCs0TzRkN0hoR2QyY0R0amR6U3A2azB1VlVNVk0wOTJwclpWZ1l1LzNUd3F6S2ZJemN1UlA3Vlk0T3hFeDhSbVd5a3hsc0dsM1F0a3FxSk4yTmUrUEpQUCtuTzBEUmxDaTFRU2QwUFFiLzdzOVorRldyUm5iNDNJMElEMkRsUzEyU21hOFdRRlpyVlVDeHRxL2ljRWphWE9kVW5BYXJ3bkQ5Sko1dG9UellXRlkrd1lPSTNxNWFmZ0RRVzVpK3NEVW1IVUZsVDN6bzV4NUJYdUx6cmZYN21nRUFOUHFJZG5BUWhTZTZWUENuUjhKd0IweE1XVGFPWWRMWGZGSWI0Y0pmRjFCbFo4eUY2czlVUm5KWWRidjVmVDZ1ZjRzcUZ3MDhBbXhyZGpmYWFPMmJkeDFSSGgwVnM2SjBEeFNqQzhTOVdIMlN0TFhTL280a0Y2clBROXAzVjMrenFCV3l4bWtCbHNlVWN5Q096S1A0LzBjckEwT2NTM1VHbGhXNXZrZUtUbVhwZ0IxVENqaHk0QzVsRHJyeWhwa2FrcG1UdmlFZzliTGdlQ21kdWw0eC8xTUtNM3FOVlArcnBTT2k3RlJiTm1GUDJSYXI2MzI0S1pmc01ITzFBYXkraXIyb3I4Y2lTaUpUckYwMVRiSlFPM29meU1LZTQxaG12Z3ZQcnpzaWx6UmN4cXBzWG83SGl1Ri9RWXhkYTJvN3JqUGVrdktHcUl1OERLUGdvdEg2bmRGdGl6dTA4Zm1TZjBTT1VKUUR6SkFNOWhrUUppOTdocnB6MmJ2WlJMSmJwNTFmMUVLNmtRRmhYZjI0VWRuczhlZWk5blRNeUVGSnVuL0RRRE1TNTFxTDRKSTlWTCtJNDJrL1lkZm41TWVtaGxDOXpJRGRMMHdYNFluQXVXY0EvOWltT1pmOS96K2ZzcG1ueHgrb3g3R3RaeVdDSGd6Uy9vU280TGxMNzZNY0xZakRKS0ZIQ3gzS2JPNlZNOHo3REhmaXFzTHAwUW9OTTVpUEF3Zys5NnhMcTViMS9WaEk5eHVsSWRGckpnQ296VVBCMnpzbU5aR3FmSCtDMXhMT21vSlJNWVpmNURESDRvUzNhLzBCcGRGNGh4V3FIbEhBOEhKZzcxR2R4VVp1dnFJUy9MRmVpZ1d0Qm1tTlFmTGRBMEpSZXNLR0NRbmZlemkvZVd3VlhjQk0rM1FNUDQ0eFQzTnpVeTRtOG9PVkc3OTUweUE4TkhYNnpQZ1VGVWEzK2xWQTVnN1QwbHlDazdxRDhVczRLUmVJVTdYa0JZUXgybzNVcy9SL2NSMlF0Q1lMc3pCbzlxWHEzNUE2aEtBaEpiU013L000dDZpdzk= '
# print(Task.aes_encrypt(json.dumps(task_data)))
print(Task.aes_decrypt(Str))

