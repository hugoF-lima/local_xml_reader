import time, cv2
import pydirectinput
from pyperclip import paste
from win32 import win32clipboard

import io
from PIL import Image
from datetime import date

# import keyboard  # Because pyautogui keyboard doesn't give a damn
import simulate_shortcut
import pyautogui as pg
from pyautogui import locateCenterOnScreen as locate_element
from win32 import win32gui
import pygetwindow
from pygetwindow import getWindowsWithTitle as get_win
from tenacity import retry, retry_if_result, stop_after_attempt, wait_fixed
from itertools import count

# from os.path import dirname, abspath, join
# import numpy as np
import base64

# To enable LocateOnScreen on all monitors
from PIL import ImageGrab
from functools import partial

ImageGrab.grab = partial(ImageGrab.grab, all_screens=True)


# implement this on main window
KEY_DELAY_ITENS_WIN = 1.2
DELAY_BETWEEN_EVENTS = 0.2
INTERVAL_03 = 0.3
# TODO: Implement the physical copy_paste
# given the shaded taskbar, img recognition might be affected
TYPE_INTERVAL = 0.225
MAXVAL = 10000
STEP_INTERVAL = 10

VK_RETURN = 0x0D
VK_C_KEY = 0x43
VK_D_KEY = 0x44
VK_TAB = 0x09
retrieved_dfe_txt = r"dfe_keys.txt"


pg.FAILSAFE = True
# the tkinter slowdown happens because of time.sleep
# Gonna have to replace it with datetime equivalent
#


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


# b64_uri`s
itens_header_msg = b"<plain_txt_msg:img>iVBORw0KGgoAAAANSUhEUgAAAFgAAAAZCAIAAAA6836qAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAASdEVYdFNvZnR3YXJlAEdyZWVuc2hvdF5VCAUAAAExSURBVFhH7dhBcoMwDAVQH4+epr1QWVKWwAn7x1/jKDLGNqGdifFbZCQZCP4DWcRN0/TjzffWgxDu0/u6q23bHkEMw/BxS+M42iDWdcXorWFXVVoOQqoCeCkaD4K7yupBiHwQzjkWQTx5XfaaJ760zSBOuD4IfZemvcpfXPNfg2ALutU1sAXp9yZgJrploSfA9oAJQk57Jmvlr0b8qQvILmnmYMhO9BLFEyN+InCKJlPv1SA0s8RC80cJtpxDdqKLgJOUOAiQM59TgIofy4MiKFkC1lWT1AEHdoMAnCiVclkQrEuW4MQkdcCBVBC7KoIIzN1QaFkA5yC9mkB2Etq4CDhJuTiI99WDED0IgV1he+WaDQIbq2WD+PYwvaFHEMuy4HFo4Ik4TYLo/2JTD8Kb51+jGjmpSGhdywAAAABJRU5ErkJggg==<!plain_txt_msg>"
msg_header_msg = b"<plain_txt_msg:img>iVBORw0KGgoAAAANSUhEUgAAAH8AAAAWCAIAAABmJNTWAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAASdEVYdFNvZnR3YXJlAEdyZWVuc2hvdF5VCAUAAAGDSURBVGhD7ZNLcgIxDEQ58hwr65wwEm06XZItMzDEWfgtXNKT5tcFt6/NOjz9Y7OIlv73ZgW/6fs/YfO37PRXstNfyU5/JVX6N6Gp8+Dad+6gTO+TF6569CfwNyvSb9XsG4opRldFML1PXrjq0Z/A3+yZ9I3iM6ajqyKY3scWdCe0/w1/sxfSv3+Uo63WBls9UQC0RuvTAoEHwaAlQXZbgy0ljNFtjdaLMYLJLYsuPjibvnrU3QfoyE4UatAawejIyJtKdzmfWhgcUdJoq4QFY2pyEXD7QvqKjgxIgJYnoFF0FFCpmwQGoM0nCkVHBmuVhq8+QAtv0Cj03SLg9p3fPuiOUOsJslGyr68N+2yLgqjp1lnWBtDkIuD2mfTrmmY0GnkQjI6MYtMYLReFgbow0wVjanIRcFukT5p60Kx41vCAHidg7Rt30BqhJfBgZEBoDTX3dYctCkNl8GRq2I6KgNtR+puaUabPs9M/hyVOmnqDnf5Kdvor2emvZJi+yc1nOY4fPRSjzyk1BlAAAAAASUVORK5CYII=<!plain_txt_msg>"
enviar_msg = b"<plain_txt_msg:img>iVBORw0KGgoAAAANSUhEUgAAAIMAAAAXCAIAAACnCGtkAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAASdEVYdFNvZnR3YXJlAEdyZWVuc2hvdF5VCAUAAAD2SURBVGhD7ZVRDoJADES5Lrfibl6AG2jJbJraUsAfdhb7PsjstAb0xTCth0yTX0Bjr8BtxpFbsOgoC/azrrEji+t395Fj04WTG8cns09/8B3i6MpyFuy+a05H2VHImi5sN34XPZjnGQ5AM/Eq7mVZltQEzsU9lAkWeE3Iq9LS2gv8tMwDtYmW/oMywcJgJlDKVacaBGQ7AvaITMgY74lWff+aCHoUYgOynooh/xNAs/uhbVBsz8ljTcRN2xDyBBNCzMcNIWO8JwQtEYTTLEFxfRY6wmvi3ygTLJQJFsoEC6kJGRQ3s2NCqqILcAA2EwUDZYKDdf0AEE1ZI8k/jcgAAAAASUVORK5CYII=<!plain_txt_msg>"
red_square_dot_msg = b"<plain_txt_msg:img>iVBORw0KGgoAAAANSUhEUgAAABwAAAAaCAYAAACkVDyJAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsIAAA7CARUoSoAAAAASdEVYdFNvZnR3YXJlAEdyZWVuc2hvdF5VCAUAAANfSURBVEhL7VU7SBxRFD26UdYfflklgmIEUYiyElRsrCwUEpGAIEgKPwFLm4hlSCOYyl5LdW3ihxAliIiFRSBxUaMigaAoiPGLn12yUXPO7KirM24sTKocOLy5991z787b++5E7O/vn+Mf4k4Ft7a2MD09Da/Xi7W1NRwfHyMuLg5ZWVlwu92oqKiAy+Uyo8MjbEHuYXh4GO9HR7G6vAz/wQECJyfAOSUREYiKjYUzMRHZ+fl4WlOD2tpaJCUlmWp72BY8Ozsz3qS3pwejHg/ce3uoPj2Fm3sZpJP0k5uklxxzOOBNTkZNfT2aW1qMN4+MjOSOFbYFd3Z28LarC5/7+lB9dITn9OWRD0xGkBL9MrlCviPH4uPxpKEBr9rbkZqaSo8Vlp9xwiPz8K0+9ffjGYu9oO8xGUNGkSomaJUtv/YVp3jppFceO1gKqkFGBgdReHhovNkj0mHs3A7tK07x0kmvPHawFFSTRK+soIrP+eRlAJsDJSVAXR3Q2BhcZctPKE7x0kmvPHawFJyamoIrEEARn69tKnlrK9DZCXR3B1fZ8ptQvHTSK48dLAUXFxcRz458yOeL/8tAaSlQWQnk5gIJCcFVtvwmFC+d9MpjB0vB7e1toxlig+YVMjOB9HTTMCFb/hBIJ73y2MFS0Ol04oyr2v0a1HV+3b4QyL7RjdJJrzx2sBTMycmBn1Nk17QvsbAAzM0BbH3wyIxVtvwhkE565bGDpWAp/5MdTo5vpn2JmRlgYAAYGQEmJ4OrbPlDIJ30ymMLTZpQDg0NnZekp5+/4TD5EZyad6bipZNeeW7mFi1vWFxcjDx230c+q7H3De+foTjFSye98tjBUjCBLd/U1ISY8nLwwMDDg32/XUH7ilO8dNIrjx0cHR0dr81nA5ryaWlpSMnIwMzGBr6sr8NHv+6YBnc0qVH2k+QR4iv5gfSQPhZ72daGsrIyREXpclhx6/fQ5/OxCefQ29uLpYkJFOzuQn2XTCpVgNwjv5NLKSko4DE2NzejqKgIMTEa6fYI+wE+Zftvbm5ifn4e4+PjmJ2dxerqKm/EEeL5KcrOzjb+q6qqKhQWFiKDp+Jgh4ZD2IIXCHA2HvBrr0J+XnZ9oHX0utwqnMgBftsR3sSdCt4nLF36t/G/4D0D+A2RF4NBXk+tUQAAAABJRU5ErkJggg==<!plain_txt_msg>"
red_square_msg = b"<plain_txt_msg:img>iVBORw0KGgoAAAANSUhEUgAAABwAAAAXCAYAAAAYyi9XAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsIAAA7CARUoSoAAAAASdEVYdFNvZnR3YXJlAEdyZWVuc2hvdF5VCAUAAAMUSURBVEhLvVY9TFNRGD2lpQRoUmJIIylLCUUYdLGEOKCDVQMLhEDShKmLIhOjLgwsrExoXHCsCwYH8KcsLg1SY2IiIbSAiWkg1RhICtXSH7/zeBh8977CYDjJyX33u9/5Tu99P18de3t7FVwgaszxwnCuHZZKJeTzeRQKBRSLRZTLZdTU1MDlcsHtdqO+vh5Op9PMro6qhiy8v7+PjY0NLC0tYXV1FVtbW8jlcvB4PGhra0N3dzf6+vrQ0dEBr9dr/JBqsDXkbtLpNObm5vBxcRG+nR34KxV4hC5ZLwpzDgcywmxLC6739yMajaK9vd3YtR20hkdHR1hZWcHTmRn8jMcRlthNYVDYLKwT/hb+EKaE74Vx4aVwGGMTE+jp6UFtba1EVCiGPMb19XVMT06iKGYRid0RthireuwI3wljQpeYPp6aQmdnp/Z4lQjvD48xu7xsmPULq5kRXGce86mjnnV0UAzX1tbwSR6Q23KvuDMe4XnAPOZTRz3r6KAYLiwswLu7i1tyfdbOrGA+ddSzjg6KYSKRQLPcxyvm3IrXwoDJ5wxYQB31rKODYri5uYkGEdgdZVT41eRDBiygjnrW0UExPDg4MIK6N4m72z2+NPDLHE+DOupZRwfFsKmpyXip88fTf6DbkRXUUc86OiiGXV1dyMn7w51YvwgPzNEOzKeOetbRQTHs7e3Fd/kofzHnp/FIOH18aWDMHE+DOupZRwfFcHBwEPlAAG/lOi207pKmjJFPGDDBOfOpo551dFAMW1tbcXd4GB/q6vBK5t+EVlMruM485lNHPevooBg2NjZidHQUV0dG8FLELyTGDzQfhLLwxJwj54xznXnMp4561tFB2y3YcFOpFJ7NziIxP4/Q4SHuybt1TdYuC0+6BR+Qz8I38pAkGxpwY2gI98fHEQwGbRuybT+syDcxm80iFoshLp+pnDRet3R9p/RJh6xVpA+WpO8VpNt7pBGHBwYQiUTg8/ngkDU72BqegH8pMpkM4tKqkskktre3/3b8gDwcoVAIYWlJfr/f+MtxFs40/L8A/gB0ajveVmSMOQAAAABJRU5ErkJggg==<!plain_txt_msg>"
blue_square_msg = b"<plain_txt_msg:img>iVBORw0KGgoAAAANSUhEUgAAABwAAAAWCAYAAADTlvzyAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsIAAA7CARUoSoAAAAASdEVYdFNvZnR3YXJlAEdyZWVuc2hvdF5VCAUAAAOPSURBVEhLvZbLTxNRFMa/mXY6lEdLWmiggBqwLEwlxhCthBAJEFkQE4wuDQQMC1y5Y6f/gNGFcUGEBJZq0sSFqaEsJIgsTBCoLighGrSQyqPlVfpgxnumU5XO0NTE+Esm98695zvfve19DBeJRGT8R/Iy3NvbQyAQwMrKCsLhMOLxOERRhMPhQG1tLdxuN4qLi9Xo3OQ0PDw8xMzMDCYnJzE7O4vV1VVsbGxAkiTwPI+ysjLU1NTA4/Ggra0NTU1NKCgoUNX66BrKsozNzU14vV6MjY0h+JVD0nIFvKUevFgGjjdBlhKQ4sx8ZwnCznu4Tsvo6elBd3c37HY7OI5Tsx1H15B+wpGREQw/e4lQrB7GynYYS1zgjEXMTGQqAxvVETONQ07tI7UbRGrND6d5CQN3bqK/v//En5hXy1/Q/+Pz+RSztbgbwqkbEGwX2czKmY+ZmZGEjZGV9E7t1E9xFE860lMePTSGbMYYHx9HKGKD0XmNzaw+PSsy0UVW+imO4klHesqjh8aQRje3GIXB0QKj9RxLJqg9wNWDObz7Mqg8z7/dx+CWV+2hCQtKPOlIT3n00Bj6/X7EJCt4HbMna49Rkwwrjyf2Cfe2Xqi9aSiedKSnPHpoDOfn5yEZimEwV7C33yvt4fpTWKR99S2NKCfUWgZO0ZGe8uihMQyFQpA5NlLj8VVWfrSt1nJDOtJTHj00hrShCTlrkcQ5k1rLTUaXyZONprWqqgoc29RycldtSfPIdkutAZ/FM0r5puiSUv4J6UhPefTQbHzatK/8YXC1AxBKz6ut+ZOMLEJeGcb1dodyeGSjmWFnZyeKjFEcRQLsMImprflB8aQjPeXRQ2PY2tqKy42VkMJTbLQLLIn+iZENxVE86UhPefTQGFosFvT29qKuKoHUdx9SUZrpAeuhLZJ9IKfbqJ/iKJ50pKc8ehiGhoYeqHUFg8GA6upqFJp5LAfeYmNtlQ3LyB5RuQE4jtXpPJUlZrQP6fAHUttzzOw16uzfcHfwNrq6uk68pk68nqLRKCYmJjA6OoqPgS3ECxvBl5wFZ7KxQ5tdT0dsJSe2IO0uQzz4gAtuG/r6+tDR0QGr1fp311OGRCKBhYUFTE9PY2pqCsFgEOvr60gmkxAEARUVFXC5XGhpaUFzczMaGhpgMuXerzkNM8RiMeXzgk4PugUynxilpaVwOp3KZ4bZzK6uPMjL8N8B/AQkD5LznRcU4wAAAABJRU5ErkJggg==<!plain_txt_msg>"
navegar_msg = b"<plain_txt_msg:img>iVBORw0KGgoAAAANSUhEUgAAAHkAAAAcCAIAAADKoYf3AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAASdEVYdFNvZnR3YXJlAEdyZWVuc2hvdF5VCAUAAAEXSURBVGhD7dbrDYMwDATgrMtW3a0LsAE9xZYJCY9SEpOi+35UthOodEKBMNKRaZq0uibgRnRI07omvMgLn2s/PK/9MGs/zNrPIms9V6ieYRg03DLrN9WDb4+DrLWhy27OOoTFP2btw9yfdZovs26IWSu3M8QiznIX1koB6VBIC9pH2SRtpXbWb9Ym2wPfT1LlHme9vBvLIFAbm9ivFKl0CayOiyqd++sla4hpzAFJAdlwdY8or9qfOPunrGG/Pjtx1lHWkEVjdLS2X2i/dpU2kbQ23yoauTnrdloH94M7s0Ycq3T5PL0+0lFPHvtcd+ggayxTRZtZY4Gq03CzrKkpZu1nzhqHNdWVHiCwyBofIVRL9mIcx/EDkkZXtF1b9KgAAAAASUVORK5CYII=<!plain_txt_msg>"
mensagens_msg = b"<plain_txt_msg:img>iVBORw0KGgoAAAANSUhEUgAAAQYAAAAXCAIAAABmqnbhAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAASdEVYdFNvZnR3YXJlAEdyZWVuc2hvdF5VCAUAAAFtSURBVHhe7djbbYQwEIVhV0U/7oZi6IVWIiqIZ3wbsyBtlokiR//3ksWYeTqHS8LXRw7gn6ISwIBKAAMqAQyoBDDwqUQMIcStHFT7uoSwrHs5BKbgVYklOaVfekIlMBu3SsQ4dmKLIca0TiUwF7dKrLuUoL08rVKQtFIroW9RKu/RU6s+SMyj5HVT0QbXOXrxo+HAJcdK6IMhpy1ltCyUQPb4blF/adp78PVXv/7MzClb7IfKw+GA5VmJ3IR0WOOX/tZ1vT0Xcq6eUnZbX00k0EWb304/HQ5cca1EzuzWgmsrcbpFX6VW5YTL7n6Vjs1z+kab9Z8PB274VqLc181B/imrPZjiNrVJSb5ukfRKkPuc1pI68qPhwA3vSshXbLsLm2jm+3Mm569SK9nOTOwT+9+suufm8/r94cA1n0r8AakB4Ya/WSshN/38WgW4mqwSpzckwN20L07A76ASwIBKAAMqAQyoBDCgEoBxHN/8FQE/0euxCwAAAABJRU5ErkJggg==<!plain_txt_msg>"
navegar_h_msg = b"<plain_txt_msg:img>iVBORw0KGgoAAAANSUhEUgAAAQgAAAAcCAIAAAASpLaRAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAASdEVYdFNvZnR3YXJlAEdyZWVuc2hvdF5VCAUAAAGrSURBVHhe7djRccMgEEVRV0U/6oZi1ItbyaiC7AKLhFhlSMYknuien9grBD/vWXYeH6+zAf8FxQAcFANwUAzAQTEAB8UAHBQDcFAMwDG9GDE8ihDLaNBTbg3xWd6NWOSUZS1vkuWbOwDZzGJosg9BfcbYhPb1pAYhNNX4uhjUBlcmFkNq0X58T6dBX2M4PJooBn5mWjH0cXHRi/QkyeqKkuk0rGmtwV31S1JiN8ilZWkeSCKvl8X9Dv2hdcv8vj8CdzazGDWeLUlgyZ6GNS9Kscwvm+F5C5vo+vO15up5h4tD+z3qJri1uU8MJ2BpXj+TJZv2eb3H0RnKSzOU6bKFLRs4VN+Zfmfcza//xhjIqK2w4X6LvMrL2kybbpN+B+Uc6hyBW5tYDA3e8Rt7+a+UTstwj6MOSx6bYZqlvzrRS3mVXWo1Q10s6nr3UFvvHIFbm1kMUdKZpLxp5A5Di6AGM/2YViXBe3DtBl1Sg+7E9zRMt9nEOVR3UXpefwRubXIxRvlBB/4KxQAcFANwvEkxgPdCMQAHxQAcFANwUAzAQTEAB8UAHBQD6GzbJ1DvJaBUyA3ZAAAAAElFTkSuQmCC<!plain_txt_msg>"
sim_msg = b"<plain_txt_msg:img>iVBORw0KGgoAAAANSUhEUgAAAFwAAAAhCAIAAADbMVsQAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAASdEVYdFNvZnR3YXJlAEdyZWVuc2hvdF5VCAUAAADvSURBVGhD7dS7EYMwEEVRqqIeAieqRG2QqxeacAN0YO+uPjDwTIaXGb0bycKJzqw0rOwUUUCK8mJWFpEKyqfvQggY5d1r8zxfoeSt3iIKiCggooCIAvJGSdNQmpL8XOI4jHHJ39xyRVECs7B1LCv/XFFkTMbnUGw5Xx+5PIfbok66kcFklMrV0qmy/nC7/B/afNh6i/YoFWC3tHX77135o2g2BnZWG5A2KXUmfq1v6hko25tLlBTb8cTEzkoUPWGtPBREeWpEAREFRBQQUUBEAV2hyLduwyiy23kAhUlZRFIUdogoIKKAiAIiyql1/QLilVr21rHeiAAAAABJRU5ErkJggg==<!plain_txt_msg>"
copiar_nota_entrada_msg = b"<plain_txt_msg:img>iVBORw0KGgoAAAANSUhEUgAAAQgAAAAcCAIAAAASpLaRAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAASdEVYdFNvZnR3YXJlAEdyZWVuc2hvdF5VCAUAAAGrSURBVHhe7djRccMgEEVRV0U/6oZi1ItbyaiC7AKLhFhlSMYknuien9grBD/vWXYeH6+zAf8FxQAcFANwUAzAQTEAB8UAHBQDcFAMwDG9GDE8ihDLaNBTbg3xWd6NWOSUZS1vkuWbOwDZzGJosg9BfcbYhPb1pAYhNNX4uhjUBlcmFkNq0X58T6dBX2M4PJooBn5mWjH0cXHRi/QkyeqKkuk0rGmtwV31S1JiN8ilZWkeSCKvl8X9Dv2hdcv8vj8CdzazGDWeLUlgyZ6GNS9Kscwvm+F5C5vo+vO15up5h4tD+z3qJri1uU8MJ2BpXj+TJZv2eb3H0RnKSzOU6bKFLRs4VN+Zfmfcza//xhjIqK2w4X6LvMrL2kybbpN+B+Uc6hyBW5tYDA3e8Rt7+a+UTstwj6MOSx6bYZqlvzrRS3mVXWo1Q10s6nr3UFvvHIFbm1kMUdKZpLxp5A5Di6AGM/2YViXBe3DtBl1Sg+7E9zRMt9nEOVR3UXpefwRubXIxRvlBB/4KxQAcFANwvEkxgPdCMQAHxQAcFANwUAzAQTEAB8UAHBQD6GzbJ1DvJaBUyA3ZAAAAAElFTkSuQmCC<!plain_txt_msg>"
green_square_msg = b"<plain_txt_msg:img>iVBORw0KGgoAAAANSUhEUgAAABwAAAAWCAYAAADTlvzyAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsIAAA7CARUoSoAAAAASdEVYdFNvZnR3YXJlAEdyZWVuc2hvdF5VCAUAAAOlSURBVEhLlZZNSBtpGMf/M5OZRBMFP2oREywa6XooiNawxV22UFsipHR76MWFIj0V7KFb6KnUQ6HXtgcLexJXqJcemmJAtx9QqLQQqxR60IVqdZPW3dYaMRqSyXz0fV4n2DiT6P6GYSbv+/yff57JvO8TYWNjw8Q+qKqKtbU1bG5uIpPJQNd1SJKEyspKVFdXo76+HoqiWNHlOZChaZowDINf6SwgCAI/RVHk14NQ1pCS5/N5JBIJTE1NYWZmBktLS9ja2oLP50NLSwu6u7sRDocRCAQgy/K+xiUNqaLV1VWMj48j+uQxVrIJqB4NmswqFUwIpgBXXoSSdaHZE8CvZ86hv78fjY2NvOJSOBpqmob5+XkM/zGMx/EJqMcUiCdqIAW9EOpZFYoIU2XGa3no77dhvE5BeafiXOgsrly+gvb2drhcLitbMTZDeozJZBK3bt/Co79jME/VwHWyDlKTh340dlqBBClZvP4xC+3FVwjPUzh/NIKhG0Pw+/2Oj9dW+/b2NsbGxhB9OwHzdA3kM4cg+StY5B4zgj6zcZqnOIonHekpjxM2w+XlZTx6GoXWUQHXL3UQD7vtRnth8xRH8aQjPeVxwmYYjUbxj+sTpB/Zb9bEKvsfUDzpSE95nLAZTk9PQ68RIbV6HSv7QezCTfcI7npi/Not9lozDBZPOtJTHidshgsLCzA8bDHXydbILmR2Ub6OWqGBf6brBWWQ3xcgHekpjxM2Q9q+ILEdxF08VTCrEHzWyA4yO76H65ie53HAZkg7CHS2hanFy/OCPGgzI/Ls+B6uY3qexwGbYTAYhJhje2eqONErfdK6K2ZvhaQjPeVxwmbY09MDMWXA+JCxRnZ4rj3E79kIP2Pan9ao/YuQjvSUxwnbTjM7O4tL1y4h0bEF5Tf/zjo8IMZ/OagPkgi89WHkzgi6urqsmV1sFba1tSHyUwSYSSM/vQ7jq2rNlIfiKJ50pKc8Tji+NAMDAwi39cL86wvybI80/s1Zs87QPMVRPOlIX+qlKdkt5ubmcO/+PUy9fwYcr4IYYjvPkUqItbvdwlhn3WI5AyOeAt6kEQ724urgVXR2dh68WxSgxruysoLR0VHEXsaQVD7DrJX4oqZ1Rq++mGV9cV2HX21A5OcIr6y5uZk34lKUNCSoCdOuv7i4iMnJScTjcd7x0+k0qqqqeMcPhULo6+tDa2srvF5v2eZLlDUsQMa5XI4/avoDVYD+SNGjc7vd+xrtAHwD0/aedUvATQsAAAAASUVORK5CYII=<!plain_txt_msg>"


def update_clipboard(list_content):
    win32clipboard.OpenClipboard()
    time.sleep(0.2)
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardText(list_content)  # ICMS
    win32clipboard.CloseClipboard()


def seek_window(win_obj):
    win_ob = pygetwindow.getWindowsWithTitle(win_obj)[0]
    if win_ob:
        return
    else:
        print("Synchro window not found!")
        return False


def window_restore(w_spotted, module_str="EMIF"):  # helper...
    while True:
        win_identifier = get_win(f"{module_str} : Documentos Fiscais --> {w_spotted}")[
            0
        ]
        if win_identifier:
            win_identifier.activate()
            win_identifier.restore()
            time.sleep(0.2)
            break
        else:
            print("No window was found")


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


def repaste(value: str):
    win32clipboard.OpenClipboard()
    time.sleep(0.2)
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardText(value, win32clipboard.CF_UNICODETEXT)
    win32clipboard.CloseClipboard()
    time.sleep(0.01)
    simulate_shortcut.get_key_comb("ctrl+v")
    time.sleep(0.1)


# Pending to inform user with _: Tk, message: messagebox,
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

    # Precisava retornar false ou um dialogo caso não encontrasse o ícone.
    # Ou algum tipo de retry, visto que as vezes ele não localiza o objeto


def moving_into(element, pausefloat, keyrelease, clicks_in, x_offset=0):
    loc_f = locate_element(decode_img(element), grayscale=False)
    if not loc_f:
        print("Field not found")
        return False
    else:
        time.sleep(pausefloat)
        loc_f = (
            loc_f[0] - x_offset,
            loc_f[1],
        )  # Where the offset thing happens
        pg.click(
            loc_f, clicks=clicks_in
        )  # Changing contents do require mouse for now...
        grab_me = copy_clipboard()
        time.sleep(pausefloat)  # Though i could write a string to memory grabbing
        simulate_shortcut.get_key_comb(f"{keyrelease}")  # the contents on the field...
        time.sleep(pausefloat)  # It would've been neat
        return grab_me


""" @retr
def re_focus_window():  # A helper to not leave synchro on the blue
    re_focus_win = pg.moveTo(x=597, y=482)
    pg.click(re_focus_win)
    time.sleep(0.3) """


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


def query_nnf(obj_search, img_gather, num_value, pausefloat: float, clicknum=1):
    obj_search = locate_element(decode_img(img_gather), grayscale=True)
    if not obj_search:
        print("Not possible to locate NNF Search")
        return False
    else:
        pg.click(obj_search, clicks=clicknum)
        pg.write(f"%{num_value}%", interval=TYPE_INTERVAL)
        time.sleep(pausefloat)
        return True


def pause_cursor():  # the listener of mouse wheel icon
    counter = 0.0
    while True:
        e = win32gui.GetIconInfo(int(win32gui.GetCursorInfo()[1]))
        # GetCursorInfo()[1] to get "HCURSOR",GetIconInfo to get the info about the cursor.
        condition = e[1] == 16
        if condition:
            print(f"e[1] == 16 means spinning")
            counter += 1.0
            return True
        if not condition:
            break
        print(counter)


def copiar_nota():
    synchro_pesq = ""

    nav = bool(locate_img(synchro_pesq, navegar_msg, 0.2))
    if nav == True:
        copy = bool(locate_img(synchro_pesq, copiar_nota_entrada_msg, 0.2))
        if copy == True:
            confirm = locate_img(synchro_pesq, sim_msg, 0.2)
            if confirm:
                time.sleep(0.1)
                return True
    else:
        print("Não foi possível copiar a nota")
        return False


# default values for xy_nnf and xy_ipi are for sp


def edit_msg_single_shot(values_in, establ_in):
    msg_model_sc = f"""Outras saídas referente a NFe  {values_in[1]} (Nota da Sensormatic) de acordo com os arts. 41 e 43 do Anexo 6 ao RICMS/SC IPI R$ {values_in[2]} alíquota 10%.  Pedido: {values_in[0]} . Etiqueta aplicada na peça para revenda a consumidor final. Adquirida da Sensormatic. CNPJ: 65494817000109"""
    msg_model_sp = f"""Outras saídas referente a NFe {values_in[1]} (Nota da Sensormatic) de acordo com o artigo 129 do RICMS/SP IPI R$ {values_in[2]} alíquota 10%. Pedido: {values_in[0]} . Etiqueta aplicada na peça para revenda a consumidor final. Adquirida da Sensormatic. CNPJ: 65494817000109"""
    msg_model_rj = f"""Outras saidas referente a Nfe {values_in[1]} (Sensormatic), conforme conforme o artigo 40, § 3º, item 2B do ajuste SINIEF 01/87 RICMS RJ. Alíquota 10% IPI R$ {values_in[2]} . Pedido: {values_in[0]} . Etiqueta aplicada na peça para revenda a consumidor final. Adquirida da Sensormatic. CNPJ: 65494817000109"""

    synchro_pesq = ""
    nav = bool(locate_img(synchro_pesq, navegar_msg, 0.3))
    if nav == True:
        msg = bool(locate_img(synchro_pesq, mensagens_msg, 0.3))
        if msg == True:
            msg_head = bool(header_locate(msg_header_msg))
            if msg_head == True:

                pydirectinput.press("i")

                pg.moveTo(x=959, y=455)
                pg.dragTo(460, 41, button="left")
                # 499x414 - subttract reference
                if establ_in == "C&A0093SC":
                    update_clipboard(msg_model_sc)
                elif establ_in == "C&A0050FX":
                    update_clipboard(msg_model_rj)
                else:
                    update_clipboard(msg_model_sp)

                simulate_shortcut.get_key_comb("ctrl+v")
                time.sleep(0.1)
                simulate_shortcut.get_key_comb("alt+g")
                # gravar, this can't be helped with mouse
                time.sleep(0.2)
                simulate_shortcut.get_key_comb("alt+f4")

                update_clipboard(values_in[2])

                return True
    else:
        print("Não foi possível editar Campo de Mensagem")
        return False


def editar_msg(
    input_values, xy_nnf=[685, 415], xy_ipi=[614, 428], pedido_coord=[786, 427]
):

    synchro_pesq = ""
    # Gonna have to include some if to change rather msg_sp or msg_sc coordinates
    # re_focus_window()  # 0.5
    nav = bool(locate_img(synchro_pesq, navegar_msg, 0.3))
    if nav == True:
        msg = bool(locate_img(synchro_pesq, mensagens_msg, 0.3))
        if msg == True:
            msg_head = bool(header_locate(msg_header_msg))
            if msg_head == True:

                pydirectinput.press("i")  # ICMS
                # time.sleep(0.2)
                # Map the pixel of the region to identify the blue tone.

                # Bridging with my application
                # update_clipboard(input_values[0])
                print("Current Pedido value", input_values[0])
                update_clipboard(input_values[0])
                # moving_into(red_square_dot_msg, 0.1, "ctrl+c", 1, 140)
                print("pedido_coords", pedido_coord)
                pg.moveTo(
                    x=pedido_coord[0], y=pedido_coord[1], duration=0.1
                )  # 840x428 SC
                pg.click(clicks=2, duration=0.1)
                simulate_shortcut.get_key_comb("ctrl+v")
                pydirectinput.press("space")  # nnf
                # pg.click(clicks=2, duration=0.1)

                print("Current NF value", input_values[1])
                update_clipboard(input_values[1])
                # moving_into(red_square_msg, 0.1, "ctrl+c", 1, 140)
                pg.moveTo(x=xy_nnf[0], y=xy_nnf[1], duration=0.1)
                pg.click(clicks=2, duration=0.1)
                simulate_shortcut.get_key_comb("ctrl+v")
                pydirectinput.press("space")  # nnf
                # pg.click(clicks=2, duration=0.1)

                print("Current IPI value", input_values[2])
                update_clipboard(input_values[2])
                # moving_into(blue_square_msg, 0.1, "ctrl+c", 1, 140)
                pg.moveTo(x=xy_ipi[0], y=xy_ipi[1], duration=0.1)  # ipi edit
                pg.click(clicks=2, duration=0.1)
                simulate_shortcut.get_key_comb("ctrl+v")
                # time.sleep(0.2)
                pydirectinput.press("space")
                # pg.click(clicks=2, duration=0.1)

                time.sleep(0.1)
                simulate_shortcut.get_key_comb("alt+g")
                # gravar, this can't be helped with mouse
                time.sleep(0.2)
                simulate_shortcut.get_key_comb("alt+f4")
                # time.sleep(0.2)

                return True
    else:
        print("Não foi possível editar Campo de Mensagem")
        return False


@retr
def alterar_valores(input_values, is_rj_establ=False):
    simulate_shortcut.get_key_comb("alt+n")
    time.sleep(0.1)
    simulate_shortcut.get_key_comb("alt+n")  # Navegar
    time.sleep(0.1)
    simulate_shortcut.PressKey(VK_RETURN)  # Return/Enter
    time.sleep(0.1)
    # locate_img(synchro_pesq, navegar_h_msg, 0.2)
    # The unrefined part bellow...

    pydirectinput.press("i")  # Itens
    time.sleep(0.2)
    pydirectinput.press("enter")
    time.sleep(1.2)  ## Key part to insert delay

    # Header_locate, could put @retr keyword here.
    item_found = bool(header_locate(itens_header_msg))
    if item_found == True:
        obj_click = pg.moveTo(x=900, y=456, duration=0.1)
        time.sleep(0.2)
        pg.click(obj_click)
        simulate_shortcut.get_key_comb("ctrl+v")  # last ctrl v from icms ipi
        # time.sleep(0.2)

        # moving_into("purple_square", 0.2, "ctrl+c", 1, 140)  # Qtd
        print("Current value from qtd", input_values[3])
        update_clipboard(input_values[3])
        """ obj_click = pg.moveTo(x=360, y=85, duration=0.1)
        time.sleep(0.2)
        pg.click(obj_click)
        time.sleep(0.2)
        simulate_shortcut.get_key_comb("ctrl+c")  # grab qtd """

        obj_click = pg.moveTo(x=518, y=298, duration=0.1)
        time.sleep(0.2)
        pg.click(obj_click)
        time.sleep(0.2)
        simulate_shortcut.get_key_comb("ctrl+v")  # paste qtd
        # time.sleep(0.2)

        pydirectinput.press("tab")
        time.sleep(0.2)
        # pydirectinput.press("tab")  # passing through val unit...
        update_clipboard(input_values[5])  # updating val unit
        time.sleep(0.1)
        simulate_shortcut.get_key_comb("ctrl+v")
        time.sleep(0.1)
        pg.moveTo(x=918, y=117)
        pg.dragTo(415, 117, button="left")
        update_clipboard(input_values[6])  # updating item value
        time.sleep(0.1)
        simulate_shortcut.get_key_comb("ctrl+v")
        time.sleep(0.1)
        obj_click = pg.moveTo(x=727, y=295, duration=0.1)
        time.sleep(0.1)
        pg.click(obj_click)

        simulate_shortcut.get_key_comb("ctrl+c")
        # time.sleep(0.2)
        pg.moveTo(x=1008, y=458)  # valor fiscal total?
        time.sleep(0.2)
        pg.click()
        time.sleep(0.3)
        simulate_shortcut.get_key_comb("ctrl+v")
        # time.sleep(0.3)

        print("Current value from Total Nota", input_values[4])
        update_clipboard(input_values[4])
        """ moving_into(green_square_msg, 0.2, "ctrl+c", 1, 130)
        simulate_shortcut.get_key_comb("ctrl+c")  # grab total """
        # time.sleep(0.2) """

        pg.moveTo(x=1008, y=497)
        time.sleep(0.1)
        pg.click()
        time.sleep(0.1)
        simulate_shortcut.get_key_comb("ctrl+v")  # This should be total from entry nf
        # time.sleep(0.3)

        obj = pg.moveTo(x=1005, y=543)
        time.sleep(0.3)
        pg.click(obj)
        time.sleep(0.2)
        simulate_shortcut.get_key_comb("ctrl+v")
        # time.sleep(0.3)

        pg.moveTo(x=503, y=474)  # Base Plena ICMS
        time.sleep(0.5)
        pg.click(clicks=3)
        time.sleep(0.2)
        simulate_shortcut.get_key_comb("ctrl+v")
        # time.sleep(0.3)

        pydirectinput.press("tab")
        time.sleep(0.2)
        simulate_shortcut.get_key_comb("ctrl+v")
        # time.sleep(0.2)

        if is_rj_establ == True:
            print("Does this trigger", is_rj_establ)
            pg.moveTo(x=617, y=536)  # Fundo Comb. Pobreza
            time.sleep(0.3)
            pg.click(clicks=3)
            time.sleep(0.2)
            simulate_shortcut.get_key_comb("ctrl+v")
            time.sleep(0.2)
            pydirectinput.press("tab")
            time.sleep(0.2)
        else:
            pydirectinput.press("tab")
            time.sleep(0.2)
            """ pydirectinput.press("tab")  # To update tax
            time.sleep(0.2) """

        # Finally?
        simulate_shortcut.get_key_comb("alt+g")
        # time.sleep(0.3)
        simulate_shortcut.get_key_comb("alt+f4")
        # time.sleep(0.2)
        return True


def totalizar_enviar():
    sent = False
    # re_focus_window()
    # simulate_shortcut.get_key_comb("alt+t")  # Needs confirmation

    synchro_pesq = pg.moveTo(x=1005, y=394)  # botão totalizar
    time.sleep(0.2)
    pg.click(synchro_pesq)
    time.sleep(0.3)
    simulate_shortcut.get_key_comb("alt+e")
    # time.sleep(0.3)

    synchro_pesq = locate_element(decode_img(enviar_msg), grayscale=True)
    if synchro_pesq:
        pg.rightClick(synchro_pesq)  # rightClick
        print(synchro_pesq, "Nota enviada!")
        time.sleep(0.8)
        """ pg.moveTo(x=350, y=237)  # Select the next note
        time.sleep(0.2)
        pg.click() """
        time.sleep(0.2)
        sent = True
    return sent

    # return next decrement?

    # moving_into("field_coordinates_forn", 0.4, "ctrl+c", 1)
    # previous_clip = pyperclip.paste()  # getting the forn


# put first consult outside.


def navigate_dfe_retrieve():
    pg.moveTo(x=998, y=321, duration=0.1)
    pg.click()

    simulate_shortcut.PressKey(VK_C_KEY)  # C_Key
    time.sleep(0.1)
    simulate_shortcut.PressKey(VK_D_KEY)  # C_Key
    time.sleep(0.1)
    pydirectinput.press("enter")
    time.sleep(0.1)
    simulate_shortcut.PressKey(VK_TAB)

    grab_df_key = copy_clipboard()

    with open(retrieved_dfe_txt, "a") as g:
        g.write(grab_df_key + "\n")
        g.close()

    time.sleep(0.1)
    simulate_shortcut.get_key_comb("alt+f4")
    time.sleep(0.2)
    pg.moveTo(x=488, y=639, duration=0.1)
    pg.click()
    time.sleep(0.2)
    # locate_img(synchro_pesq, navegar_h_msg, 0.2)
    # The unrefined part bellow...
    # #480x639


def retrieve_dfe_keys(w_get, notes_ahead, note_widget):
    finished = False
    today = str(date.today().strftime("%d/%m/%Y"))
    window_restore(w_spotted=w_get, module_str="FISCAL")
    with open(retrieved_dfe_txt, "a") as g:
        g.write(f"{w_get} ({today}) :" + "\n")
        g.close()

    if notes_ahead > 0:
        for number in count(start=1):
            navigate_dfe_retrieve()
            # note_widget.invoke("buttondown") #for tk, not ttk
            note_widget.event_generate("<<Decrement>>")
            if number == notes_ahead:
                finished = True
                break

        return finished


# TODO: Single paste on icms msg field
# 356x251
# TODO: Bellow the prospect/contract:
# KeyInterrupts only work on the console...
# When the main tk loop starts, not sure if that intervenes
# With a parallel thread loop...
# I need to make the keyboard read a shortcut...
# Given i'm outside the console when the thread runs...

# consultar_nota("COTTON STAR INDUSTRIAL LTDA")
# Definetely need a ComboBox on my reader
# Definetely need a ComboBox on my reader
# I've needed a smarter way to read the string msg.

# For some reason it's not altering items at the first run...
# It also needs to resume execution of minimized widgets.

# As vezes não totaliza...
# Ele deveria parar o script quando um campo não é encontrado,
# ou fazer um retry.

# For some reason it does ignores the clip comparisson...
# And i end up loosing numbers...

# the Window delay is still a problem from time to time...
# If i could use some regex to read the msg field...


# generate time.sleep delays based on mouse cursor state.

# get window by header id rather than icon... Because all synchro icons are
# the same

# My RFID reader needs some Combo Box filtering.
# Save the Main Total from Pandas.
# I think pyperclip only works with user input...
# Not machine induced copy...


# Auto update path variables?

# If clipboard is not digit, then call certain action to take IPI

# He could read if variables on Total NNF are the same, and skip emission

# Unfortunately i can't save the numbers of the NNF while doing them...
# If only i had an outlet to grab the number.
