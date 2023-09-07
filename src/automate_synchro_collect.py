import simulate_shortcut
import simulate_shortcut
import pyautogui as pg
from pyautogui import locateCenterOnScreen as locate_element
from pyperclip import paste
from win32 import win32clipboard
import time
import base64
import io
from PIL import Image
import cv2
from tenacity import retry, retry_if_result, stop_after_attempt, wait_fixed
import pydirectinput
import datetime
import re
import automate_synchro_main

# b64_uri`s
itens_header_msg = b"<plain_txt_msg:img>iVBORw0KGgoAAAANSUhEUgAAAFgAAAAZCAIAAAA6836qAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAASdEVYdFNvZnR3YXJlAEdyZWVuc2hvdF5VCAUAAAExSURBVFhH7dhBcoMwDAVQH4+epr1QWVKWwAn7x1/jKDLGNqGdifFbZCQZCP4DWcRN0/TjzffWgxDu0/u6q23bHkEMw/BxS+M42iDWdcXorWFXVVoOQqoCeCkaD4K7yupBiHwQzjkWQTx5XfaaJ760zSBOuD4IfZemvcpfXPNfg2ALutU1sAXp9yZgJrploSfA9oAJQk57Jmvlr0b8qQvILmnmYMhO9BLFEyN+InCKJlPv1SA0s8RC80cJtpxDdqKLgJOUOAiQM59TgIofy4MiKFkC1lWT1AEHdoMAnCiVclkQrEuW4MQkdcCBVBC7KoIIzN1QaFkA5yC9mkB2Etq4CDhJuTiI99WDED0IgV1he+WaDQIbq2WD+PYwvaFHEMuy4HFo4Ik4TYLo/2JTD8Kb51+jGjmpSGhdywAAAABJRU5ErkJggg==<!plain_txt_msg>"
enviar_msg = b"<plain_txt_msg:img>iVBORw0KGgoAAAANSUhEUgAAAIMAAAAXCAIAAACnCGtkAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAASdEVYdFNvZnR3YXJlAEdyZWVuc2hvdF5VCAUAAAD2SURBVGhD7ZVRDoJADES5Lrfibl6AG2jJbJraUsAfdhb7PsjstAb0xTCth0yTX0Bjr8BtxpFbsOgoC/azrrEji+t395Fj04WTG8cns09/8B3i6MpyFuy+a05H2VHImi5sN34XPZjnGQ5AM/Eq7mVZltQEzsU9lAkWeE3Iq9LS2gv8tMwDtYmW/oMywcJgJlDKVacaBGQ7AvaITMgY74lWff+aCHoUYgOynooh/xNAs/uhbVBsz8ljTcRN2xDyBBNCzMcNIWO8JwQtEYTTLEFxfRY6wmvi3ygTLJQJFsoEC6kJGRQ3s2NCqqILcAA2EwUDZYKDdf0AEE1ZI8k/jcgAAAAASUVORK5CYII=<!plain_txt_msg>"
navegar_msg = b"<plain_txt_msg:img>iVBORw0KGgoAAAANSUhEUgAAAHkAAAAcCAIAAADKoYf3AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAASdEVYdFNvZnR3YXJlAEdyZWVuc2hvdF5VCAUAAAEXSURBVGhD7dbrDYMwDATgrMtW3a0LsAE9xZYJCY9SEpOi+35UthOodEKBMNKRaZq0uibgRnRI07omvMgLn2s/PK/9MGs/zNrPIms9V6ieYRg03DLrN9WDb4+DrLWhy27OOoTFP2btw9yfdZovs26IWSu3M8QiznIX1koB6VBIC9pH2SRtpXbWb9Ym2wPfT1LlHme9vBvLIFAbm9ivFKl0CayOiyqd++sla4hpzAFJAdlwdY8or9qfOPunrGG/Pjtx1lHWkEVjdLS2X2i/dpU2kbQ23yoauTnrdloH94M7s0Ycq3T5PL0+0lFPHvtcd+ggayxTRZtZY4Gq03CzrKkpZu1nzhqHNdWVHiCwyBofIVRL9mIcx/EDkkZXtF1b9KgAAAAASUVORK5CYII=<!plain_txt_msg>"
mensagens_msg = b"<plain_txt_msg:img>iVBORw0KGgoAAAANSUhEUgAAAQYAAAAXCAIAAABmqnbhAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAASdEVYdFNvZnR3YXJlAEdyZWVuc2hvdF5VCAUAAAFtSURBVHhe7djbbYQwEIVhV0U/7oZi6IVWIiqIZ3wbsyBtlokiR//3ksWYeTqHS8LXRw7gn6ISwIBKAAMqAQyoBDDwqUQMIcStHFT7uoSwrHs5BKbgVYklOaVfekIlMBu3SsQ4dmKLIca0TiUwF7dKrLuUoL08rVKQtFIroW9RKu/RU6s+SMyj5HVT0QbXOXrxo+HAJcdK6IMhpy1ltCyUQPb4blF/adp78PVXv/7MzClb7IfKw+GA5VmJ3IR0WOOX/tZ1vT0Xcq6eUnZbX00k0EWb304/HQ5cca1EzuzWgmsrcbpFX6VW5YTL7n6Vjs1z+kab9Z8PB274VqLc181B/imrPZjiNrVJSb5ukfRKkPuc1pI68qPhwA3vSshXbLsLm2jm+3Mm569SK9nOTOwT+9+suufm8/r94cA1n0r8AakB4Ya/WSshN/38WgW4mqwSpzckwN20L07A76ASwIBKAAMqAQyoBDCgEoBxHN/8FQE/0euxCwAAAABJRU5ErkJggg==<!plain_txt_msg>"
navegar_h_msg = b"<plain_txt_msg:img>iVBORw0KGgoAAAANSUhEUgAAAQgAAAAcCAIAAAASpLaRAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAASdEVYdFNvZnR3YXJlAEdyZWVuc2hvdF5VCAUAAAGrSURBVHhe7djRccMgEEVRV0U/6oZi1ItbyaiC7AKLhFhlSMYknuien9grBD/vWXYeH6+zAf8FxQAcFANwUAzAQTEAB8UAHBQDcFAMwDG9GDE8ihDLaNBTbg3xWd6NWOSUZS1vkuWbOwDZzGJosg9BfcbYhPb1pAYhNNX4uhjUBlcmFkNq0X58T6dBX2M4PJooBn5mWjH0cXHRi/QkyeqKkuk0rGmtwV31S1JiN8ilZWkeSCKvl8X9Dv2hdcv8vj8CdzazGDWeLUlgyZ6GNS9Kscwvm+F5C5vo+vO15up5h4tD+z3qJri1uU8MJ2BpXj+TJZv2eb3H0RnKSzOU6bKFLRs4VN+Zfmfcza//xhjIqK2w4X6LvMrL2kybbpN+B+Uc6hyBW5tYDA3e8Rt7+a+UTstwj6MOSx6bYZqlvzrRS3mVXWo1Q10s6nr3UFvvHIFbm1kMUdKZpLxp5A5Di6AGM/2YViXBe3DtBl1Sg+7E9zRMt9nEOVR3UXpefwRubXIxRvlBB/4KxQAcFANwvEkxgPdCMQAHxQAcFANwUAzAQTEAB8UAHBQD6GzbJ1DvJaBUyA3ZAAAAAElFTkSuQmCC<!plain_txt_msg>"
sim_msg = b"<plain_txt_msg:img>iVBORw0KGgoAAAANSUhEUgAAAFwAAAAhCAIAAADbMVsQAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAASdEVYdFNvZnR3YXJlAEdyZWVuc2hvdF5VCAUAAADvSURBVGhD7dS7EYMwEEVRqqIeAieqRG2QqxeacAN0YO+uPjDwTIaXGb0bycKJzqw0rOwUUUCK8mJWFpEKyqfvQggY5d1r8zxfoeSt3iIKiCggooCIAvJGSdNQmpL8XOI4jHHJ39xyRVECs7B1LCv/XFFkTMbnUGw5Xx+5PIfbok66kcFklMrV0qmy/nC7/B/afNh6i/YoFWC3tHX77135o2g2BnZWG5A2KXUmfq1v6hko25tLlBTb8cTEzkoUPWGtPBREeWpEAREFRBQQUUBEAV2hyLduwyiy23kAhUlZRFIUdogoIKKAiAIiyql1/QLilVr21rHeiAAAAABJRU5ErkJggg==<!plain_txt_msg>"
copiar_nota_entrada_msg = b"<plain_txt_msg:img>iVBORw0KGgoAAAANSUhEUgAAAQgAAAAcCAIAAAASpLaRAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAASdEVYdFNvZnR3YXJlAEdyZWVuc2hvdF5VCAUAAAGrSURBVHhe7djRccMgEEVRV0U/6oZi1ItbyaiC7AKLhFhlSMYknuien9grBD/vWXYeH6+zAf8FxQAcFANwUAzAQTEAB8UAHBQDcFAMwDG9GDE8ihDLaNBTbg3xWd6NWOSUZS1vkuWbOwDZzGJosg9BfcbYhPb1pAYhNNX4uhjUBlcmFkNq0X58T6dBX2M4PJooBn5mWjH0cXHRi/QkyeqKkuk0rGmtwV31S1JiN8ilZWkeSCKvl8X9Dv2hdcv8vj8CdzazGDWeLUlgyZ6GNS9Kscwvm+F5C5vo+vO15up5h4tD+z3qJri1uU8MJ2BpXj+TJZv2eb3H0RnKSzOU6bKFLRs4VN+Zfmfcza//xhjIqK2w4X6LvMrL2kybbpN+B+Uc6hyBW5tYDA3e8Rt7+a+UTstwj6MOSx6bYZqlvzrRS3mVXWo1Q10s6nr3UFvvHIFbm1kMUdKZpLxp5A5Di6AGM/2YViXBe3DtBl1Sg+7E9zRMt9nEOVR3UXpefwRubXIxRvlBB/4KxQAcFANwvEkxgPdCMQAHxQAcFANwUAzAQTEAB8UAHBQD6GzbJ1DvJaBUyA3ZAAAAAElFTkSuQmCC<!plain_txt_msg>"
green_square_msg = b"<plain_txt_msg:img>iVBORw0KGgoAAAANSUhEUgAAABwAAAAWCAYAAADTlvzyAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsIAAA7CARUoSoAAAAASdEVYdFNvZnR3YXJlAEdyZWVuc2hvdF5VCAUAAAOlSURBVEhLlZZNSBtpGMf/M5OZRBMFP2oREywa6XooiNawxV22UFsipHR76MWFIj0V7KFb6KnUQ6HXtgcLexJXqJcemmJAtx9QqLQQqxR60IVqdZPW3dYaMRqSyXz0fV4n2DiT6P6GYSbv+/yff57JvO8TYWNjw8Q+qKqKtbU1bG5uIpPJQNd1SJKEyspKVFdXo76+HoqiWNHlOZChaZowDINf6SwgCAI/RVHk14NQ1pCS5/N5JBIJTE1NYWZmBktLS9ja2oLP50NLSwu6u7sRDocRCAQgy/K+xiUNqaLV1VWMj48j+uQxVrIJqB4NmswqFUwIpgBXXoSSdaHZE8CvZ86hv78fjY2NvOJSOBpqmob5+XkM/zGMx/EJqMcUiCdqIAW9EOpZFYoIU2XGa3no77dhvE5BeafiXOgsrly+gvb2drhcLitbMTZDeozJZBK3bt/Co79jME/VwHWyDlKTh340dlqBBClZvP4xC+3FVwjPUzh/NIKhG0Pw+/2Oj9dW+/b2NsbGxhB9OwHzdA3kM4cg+StY5B4zgj6zcZqnOIonHekpjxM2w+XlZTx6GoXWUQHXL3UQD7vtRnth8xRH8aQjPeVxwmYYjUbxj+sTpB/Zb9bEKvsfUDzpSE95nLAZTk9PQ68RIbV6HSv7QezCTfcI7npi/Not9lozDBZPOtJTHidshgsLCzA8bDHXydbILmR2Ub6OWqGBf6brBWWQ3xcgHekpjxM2Q9q+ILEdxF08VTCrEHzWyA4yO76H65ie53HAZkg7CHS2hanFy/OCPGgzI/Ls+B6uY3qexwGbYTAYhJhje2eqONErfdK6K2ZvhaQjPeVxwmbY09MDMWXA+JCxRnZ4rj3E79kIP2Pan9ao/YuQjvSUxwnbTjM7O4tL1y4h0bEF5Tf/zjo8IMZ/OagPkgi89WHkzgi6urqsmV1sFba1tSHyUwSYSSM/vQ7jq2rNlIfiKJ50pKc8Tji+NAMDAwi39cL86wvybI80/s1Zs87QPMVRPOlIX+qlKdkt5ubmcO/+PUy9fwYcr4IYYjvPkUqItbvdwlhn3WI5AyOeAt6kEQ724urgVXR2dh68WxSgxruysoLR0VHEXsaQVD7DrJX4oqZ1Rq++mGV9cV2HX21A5OcIr6y5uZk34lKUNCSoCdOuv7i4iMnJScTjcd7x0+k0qqqqeMcPhULo6+tDa2srvF5v2eZLlDUsQMa5XI4/avoDVYD+SNGjc7vd+xrtAHwD0/aedUvATQsAAAAASUVORK5CYII=<!plain_txt_msg>"
msg_header = b"<plain_txt_msg:img>iVBORw0KGgoAAAANSUhEUgAAAF8AAAAYCAYAAACcESEhAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAASdEVYdFNvZnR3YXJlAEdyZWVuc2hvdF5VCAUAAAJ/SURBVGhD7ZbdihMxFMfnufIWolfeCsE38MoH0F6YK5EV9sIbv+2KywjLauvHnXsh1bLIiOBii2C7yyrUrS4ckzNJJpmPzLRMje7mD3/aSTLnTH5JzkwEQd4U4HtUgO9RlfAHg/fQf/FqKQc1UyX8hxubCHLn7bDWJvjb97owmUxklCCXKuE/77+Go/kv6Xljb/dewmg0klGCXHLC/5B8gSvrvYJ3dz/Bwf4U9vY+a998vIN2w4+BRhFENJbXthJGIIoIsEQ2nHDVwr947Yl2O/AJEFIGWC5MgK/gj+HyrS0N//z1NfRg8BH2J98K8O+86TWCTylfgDzhmPITQbH/1MPf2u4h/HOddW0L/tSG/+jdU3QT+CwRv5RfZWJ4GlS/bEwYEDwNwmq8HMP4Ysk+cyEZUeMjUNUtplmbVfKM+ISxleR2qTH8Mzc62mXwh1+H6GbwUyD6AcVECYPE6DfHovjJSCcq2vkEM7IZHDw9rlnn42fPYL9vVpG7qGr4z/oa/tm1q5bL4M+PfqKbwlfAsVUvRK5f7iJtHJQDU3JPaUkz4pj5s5Eryu3QwvAvdC+1A59PG0tNbELIT8YuTakcAKTSXSwX1Iojc6r4Tvgt5K5RLfzOxv2C8/Cn/OWr3By+uEx3ZLZbzH7xv2wn1QMQEhDwXpGDQ0YWCNWOryAVy04LuWvkhH98/Bu+Hx7Ajwqr3b40fC5GzB2W60dYCxx9q7yYu1228VzU/Mw1xrtfuNxL5XbLCV9YwFzEdx90HfD/YVWWmtWpEr7QeDxGC5iLeDabyQj/j/BzVJWnvyQn/JMu87u8aaloU6cavm8F+B4V4HtUgO9RAb5HBfjeBPAHJBMd0sGPnWwAAAAASUVORK5CYII=<!plain_txt_msg>"
pesq_btn_highlight = b"<plain_txt_msg:img>iVBORw0KGgoAAAANSUhEUgAAAFkAAAAhCAYAAACyegcDAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAASdEVYdFNvZnR3YXJlAEdyZWVuc2hvdF5VCAUAAAFXSURBVGhD7ZZbqsMwDES92PxkV9lbNpAdtOhDRR3kV2LLLUzg4Hg0yvUdhGm6rutF5sKQA2DIATDkABhyAAw5gE/I27aRwUiu8nyFzGfMs+97OeTzPMkDjuNoC1k10k93yCklrh2r0BWybWxFehDPN5qRf+fut7Rv+nXhHTAq6FE8PW/IJLdov8zd82rf8kmWdwU9Oc3WPA/q1o9azac6aj0svZPtu917nhavp9s6elGv1XvRviWTrEgNsTX0evsWHT2qWXK+kt7KkjtZqX3P1tGr+169VENdyek1tG/5JHt7q3taTpd31LGOWklXcnorSydZkLri6Z6GNbvHFeuo2Rp6lJxeQ/umT/Is7v7jK5g6yeLP4fl7GPGN2egZuydZG7m2rcLfXhf/RFPIYiLPKIYsRTKGbMhkLJKrBP4JmcyDIQeQvDEnY+EkB8CQA0je7zwykuP1BlPQEyLGQOItAAAAAElFTkSuQmCC<!plain_txt_msg>"
error_icon = b"<plain_txt_msg:img>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<!plain_txt_msg>"
fiscal_win_header = b"<plain_txt_msg:img>iVBORw0KGgoAAAANSUhEUgAAACAAAAAUCAYAAADskT9PAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAASdEVYdFNvZnR3YXJlAEdyZWVuc2hvdF5VCAUAAACdSURBVEhL7ZHLDYAgEESpy4KogxKsxjN9WMzqENeMf1xI9MBLRkUI8xQnH9MEmsBBwDm3ppxBPO2HdP24vPfz9UoAd32mvAdFnaTODU8CGow5NJeHUQDEGDeFKZinNc8UCOzZC+WBIvqAOR6tFgHmnUClP8D8QiCEsIzuMApocO5nqIDmGoMAwzIsxAKl5B5mgmVqUW8nI03gYwGRCVt6G9pFnrjhAAAAAElFTkSuQmCC<!plain_txt_msg>"
n_pesq_win_header = b"<plain_txt_msg:img>iVBORw0KGgoAAAANSUhEUgAAACQAAAAZCAIAAADWhhu8AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAASdEVYdFNvZnR3YXJlAEdyZWVuc2hvdF5VCAUAAADrSURBVEhL7ZbNEYMgEEYpI7VQkDN24UwaoIRU4dkucsjRBuyA7M+HMmaDMTGcfMMgu4BvVjjobhVxbdtervc6zcUY6UF9BU7ZIZyyQ7BlLoF4J4/gsZ9oemRLMpmT5QBzW4hpMfTNEr2XKarUlsAiE1ZltQjB+/DgAe80ZdQPw6BvB0mpa2yokLWLc2LrS7KcXIyUhVUYJ/fJZsoys7K/yUpn9pWs6zoEFnz9fEDApo9vIx0VUglKkkxB6gUuL0OvImHLZrBcUDENyqY1MPOXdOM4FmQ5vEVAvJ+Nyo7FTdN0yn6G/xsryWJ8Aj2FHHGpJZTnAAAAAElFTkSuQmCC<!plain_txt_msg>"


def decode_img(msg):
    msg = msg[
        msg.find(b"<plain_txt_msg:img>")
        + len(b"<plain_txt_msg:img>") : msg.find(b"<!plain_txt_msg>")
    ]
    msg = base64.b64decode(msg)
    buf = io.BytesIO(msg)
    img = Image.open(buf)
    return img


def return_img(data):
    data = cv2.imread(data)
    return data


# Doesn't work:
def regex_nfe_num(input_text):
    pattern = re.compile(r"\s[0-9]{6,6}\s", re.IGNORECASE)
    return pattern.match(pattern, input_text)


# helper for retry decorator (This one manages a default exception from retry)
def return_last_value(retry_state):
    """return the result of the last call attempt"""
    return retry_state.outcome.result()


# helper for retry decorator
def is_false(value):
    """Return True if value is False"""
    return value is False


retr = retry(
    stop=stop_after_attempt(3),
    retry_error_callback=return_last_value,
    retry=retry_if_result(is_false),
    wait=wait_fixed(0.3),
)


def copy_clipboard():  # Make this a bool function?
    simulate_shortcut.get_key_comb("ctrl+c")
    time.sleep(0.01)
    return paste()


@retr
def locate_img(obj_search, img_gather, pausefloat: float, clicknum=1):
    obj_search = locate_element(decode_img(img_gather), grayscale=True)
    time.sleep(pausefloat)
    if not obj_search:
        print("Element not found")
        return False
    else:
        pg.click(obj_search, clicks=clicknum)
        time.sleep(pausefloat)
        return True


def locate_img_new(img_gather, pausefloat: float, click_it=True, clicknum=1, conf=0.7):
    found_elem = False
    obj_search = locate_element(decode_img(img_gather), grayscale=True, confidence=conf)
    time.sleep(pausefloat)
    if not obj_search:
        print("Element not found")
        found_elem = False
    else:
        if click_it == True:
            # pg.click(obj_search, clicks=clicknum)
            time.sleep(pausefloat)
        found_elem = True
    return found_elem, obj_search


@retr
def header_locate(header):  # helper...
    # replace message_in with message
    head_locate = locate_element(decode_img(header), grayscale=True)
    if not head_locate:
        # message.showerror(title="Not found!", message="Tela Pesquisa não Encontrado")
        print("Elemento da janela não encontrado")
        return False
    else:
        print("Pesq window found")
        return True


def update_clipboard(list_content):
    win32clipboard.OpenClipboard()
    time.sleep(0.2)
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardText(list_content)  # ICMS
    win32clipboard.CloseClipboard()


def grab_nf_saida():
    synchro_pesq = ""
    nav = bool(locate_img(synchro_pesq, navegar_msg, 0.3))
    if nav == True:
        msg = bool(locate_img(synchro_pesq, mensagens_msg, 0.3))
        if msg == True:
            msg_head = bool(header_locate(msg_header))
            if msg_head == True:
                pydirectinput.press("i")

                pg.moveTo(x=959, y=455)
    pass


# data_model used:
""" fill_match = [
    {"563458": [121210, "Autorizado", datetime.datetime(2023, 1, 27, 0, 0), "6.949"]},
    {"563471": [121211, "Autorizado", datetime.datetime(2023, 1, 27, 0, 0), "6.949"]},
] """


def find_error_msg():
    warning = False
    obj_search = locate_element(decode_img(error_icon), grayscale=True)
    if not obj_search:
        print("No Error found")
        warning = True
    else:
        print("Error found")
        warning = False
    return warning


# TODO: Use coord search relative to found_img index
def query_notes(cfop, nat_op, fato_gerador):
    # see if window is already opened
    found_notes = False

    def form_query(nav_in, coords):
        nonlocal found_notes
        if nav_in:
            time.sleep(0.3)
            pg.moveTo(x=(coords[0] + 145), y=(coords[1] + 72))
            # pg.moveTo(x=595, y=244)
            pg.doubleClick()
            time.sleep(0.01)
            simulate_shortcut.key_press("backspace")
            update_clipboard(cfop)
            time.sleep(0.1)
            simulate_shortcut.get_key_comb("ctrl+v")
            time.sleep(0.1)
            update_clipboard(nat_op)
            pg.moveTo(x=(coords[0] + 145), y=(coords[1] + 99))
            # pg.moveTo(x=595, y=271)
            time.sleep(0.1)
            pg.doubleClick()
            time.sleep(0.01)
            simulate_shortcut.key_press("backspace")
            time.sleep(0.01)
            simulate_shortcut.get_key_comb("ctrl+v")
            time.sleep(0.1)
            update_clipboard(fato_gerador)
            pg.moveTo(x=(coords[0] + 145 + 92), y=(coords[1] + 99 + 60))
            # pg.moveTo(x=688, y=332)
            pg.click()
            time.sleep(0.1)
            simulate_shortcut.get_key_comb("ctrl+v")
            time.sleep(0.1)
            simulate_shortcut.key_press("tab")
            time.sleep(0.1)
            simulate_shortcut.get_key_comb("ctrl+v")
            time.sleep(0.1)
            simulate_shortcut.key_press("VK_RETURN")
            time.sleep(0.7)
            found_notes = find_error_msg()
            """ obj_search = locate_element(decode_img(error_icon), grayscale=True)
            if not obj_search:
                print("No Error found")
                found_notes = True
            else:
                print("Error found")
                found_notes = False """

    # Check any error_msg left up by user:
    absent_win = find_error_msg()
    if absent_win == False:
        time.sleep(0.2)
        simulate_shortcut.key_press("VK_RETURN")
        time.sleep(0.3)
    # Check if Search window is already opened
    nav, coords = locate_img_new(n_pesq_win_header, pausefloat=0.2, conf=0.9)
    if nav == True:
        print("coords in", "x", coords[0], "y", coords[1])
        print("Window already opened")
        form_query(nav, coords)
    else:
        simulate_shortcut.get_key_comb("alt+p")
        time.sleep(0.2)
        # nav = bool(locate_img(synchro_pesq, pesq_btn_highlight, 0.3))
        nav, _ = locate_img_new(pesq_btn_highlight, 0.2, click_it=False)
        simulate_shortcut.key_press("VK_RETURN")
        time.sleep(0.35)
        nav, coords = locate_img_new(
            n_pesq_win_header, pausefloat=0.2, conf=0.9, click_it=False
        )
        form_query(nav, coords)

    return found_notes


def validate_nf_entrada(coord_val_in):
    def find_pedido(x_coords, y_coords):
        # 967x28
        time.sleep(0.1)
        pg.moveTo(x=x_coords, y=y_coords)
        pg.click()
        time.sleep(0.2)
        # pg.moveTo(x=959, y=455)
        pg.moveTo(x=coord_val_in[0] + 548, y=coord_val_in[1] + 234)
        pg.click()
        # pg.dragTo(x=460, y=41, button="left")
        pg.dragTo(x=coord_val_in[0] + 49, y=coord_val_in[1] - 188, button="left")
        grab_msg = copy_clipboard()
        time.sleep(0.1)
        pedido_retrieve = [s for s in grab_msg.split() if s.startswith("CA")]
        pedido_val = pedido_retrieve[0].replace(".", "")
        if str(pedido_val):
            print(pedido_val)
            return pedido_val
        else:
            raise IndexError  # to pass exception to another function if happens
        # I wonder if i could pass ValueError to the Raise

    pedido_val = None
    while pedido_val is None:
        try:
            simulate_shortcut.key_press("i")
            # X=967 y= 268
            pedido_val = find_pedido(
                x_coords=coord_val_in[0] + 548, y_coords=coord_val_in[1] + 47
            )
        except ValueError:
            pass
        except IndexError:
            # X=967 y= 279
            pedido_val = find_pedido(
                x_coords=coord_val_in[0] + 548, y_coords=coord_val_in[1] + 58
            )

        return pedido_val


def validate_nf_saida():
    grab_nf_emit = None
    while grab_nf_emit is None:
        try:
            nav, coords = locate_img_new(fiscal_win_header, pausefloat=0.2, conf=0.9)
            if nav == True:
                # pg.moveTo(x=711, y=129)
                print("aha", coords)
                pg.moveTo(x=coords[0] + 408, y=coords[1] + 66)
                pg.click()
                time.sleep(0.2)
                grab_nf_emit = copy_clipboard()
                if int(grab_nf_emit):
                    return coords, grab_nf_emit
        except ValueError:
            pass


def collect_data_from_note(cfop_def, data_emit):
    list_encapsulate = []
    status = "Autorizado"
    synchro_pesq = ""
    nav = bool(locate_img(synchro_pesq, navegar_msg, 0.3))
    if nav == True:
        msg = bool(locate_img(synchro_pesq, mensagens_msg, 0.3))
        if msg == True:
            # msg_head = bool(header_locate(msg_header))
            nav, coords = locate_img_new(msg_header, 0.1)
            if nav == True:
                # Regex pattern for retrieving number
                # \s[0-9]{6,6}\s
                pedido_val = validate_nf_entrada(coords)
                simulate_shortcut.get_key_comb("alt+f4")
                # data_emit = copy_clipboard()

                n_coords, grab_nf_emit = validate_nf_saida()

                datetime_object = datetime.datetime.strptime(data_emit, "%d/%m/%Y")
                # datetime_object = date_obj.strftime("%d/%m/%Y")
                # print(datetime_object)
                list_encapsulate.append(
                    {
                        str(pedido_val): [
                            int(grab_nf_emit),
                            status,
                            datetime_object,
                            cfop_def,
                        ]
                    }
                )

                # pg.moveTo(x=483, y=635)
                # 505, 642
                pg.moveTo(x=n_coords[0] + 186, y=n_coords[1] + 575)

                pg.click()
    # 483x635
    return list_encapsulate


# window_restore(w_spotted="C&A0020FX", module_str="FISCAL")


#automate_synchro_main.window_restore(w_spotted="C&A0020FX", module_str="FISCAL")

# print(val)
# print(nav, coords)
# 505, 642
# simulate_shortcut.get_key_comb("alt+p")
""" time.sleep(0.2)
nav, coords = locate_img_new(img_gather=pesq_win_header, click_it=False, pausefloat=0.2)
print(nav, coords) """
"""nav = locate_element(decode_img(pesq_win_header), grayscale=True)
if nav:
    print(nav, "Window already opened") """
# 75,148
