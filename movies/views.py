import random
import datetime
import string
from django.core.management import call_command
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template import loader
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from math import ceil
from .models import Movie, Transaction, Comment, Request, Messages, TC, Sale, Season, Episode, Details, Hash
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as user_login, logout as user_logout
from django.contrib.auth import authenticate

domain = "swifftech-app"
standard_price = 200
pro_price = 350
pro_max_price = 500
current_year = datetime.date.year


def hash_generator(user):
    characters = list(string.ascii_letters + string.digits)
    length = random.randint(87, 1000)
    random.shuffle(characters)
    password = []

    for i in range(length):
        password.append(random.choice(characters))

    random.shuffle(password)

    new_hash = "".join(password)
    num = random.randint(length, 3000) + length

    while True:
        try:
            Hash.objects.get(num=num)
            length = random.randint(87, 1000)
        except Hash.DoesNotExist:
            break
        num = random.randint(length, 3000) + length

    Hash(user=user, hash=new_hash, num=num).save()

    return new_hash, num


# def hash_list():
#     hashes = [
#         "TVuDOgGqT3p83v6WMg7gRP3jmUEKiLB8S3GNIvetojB93C0BmsHiaYwINHlQxh1qTuWYfcxj9e1fe3fcRH9Nq4j4vIh9npHv8MGBAkysd9dVamCi04VXuOHvUsCVRAHy0dCgmmh7h6fXVAr7twOeU6e5pdTvUIyVapvxmwi8k1Hkxdgp30vnbTLgmlz83s6rvpGJyjEFvnzKGtuE4fsA8N7GB9bFLpKlUC3uAuFRdd4LCFAo5srqfB63stzIpudP2lORlzXwLYHlmktNzeXMFyK8Zy4GrbqI5piGAyRTEYZxc44p4SpaPIoQndCg7SVbkmBeLLB7MXQxehzXPKxg6bRLVLDZSUw1QWoMUuudcJF5psOHOA5ZhWykd2Uem6gF5i4srDvpHZsVVeFfOANu4XkERgkXNywgyDgz5TlUWc3usxycdcITtABypFDMP7ymhVCkfYm2Q8vDeDglhnJ3G3mmYPaG7VP9hUMdD5Cciugyn4RhKYX6fixgPUxAumFSr8qNOauVxfQwXTcqWUlXSGMNSQ50Ym1jzCxORMp4BMZGrCoygcTbj8tQOkW5ZyYXr0pUit962KtMyMjFbJhW3AaUWmI0BXZFe7vdWisdqMkHSB7kLDozmKAjJHiGudGAcFAFxe6uPYZAT6JY0Iz8BdsSXgMXX1EoodaRssG3mfyoJcyRCnU9mdCMCXV6LkPjW1S0umzz6T5ecLcBV3b9h0ht2TD1uXNsWbkhDhoTLWPNUvPQDDge0Q5czbz9XJIZG0HfW86Kr1zmmoyvvGEb1nMkwMn2oq7psqAsywOjbK6k9hiKiPCdW3GLjJxfDBqKCvSfbLwyG35L4QQL9yT2YB8fH87l834fGncVVuts4PQChG8S2RjFefRL8CnfpaRk7oXcEVdriIKWj0qYKJVecbB9kyEOCKICXkSRDZLR5VanCXbWXoAGnKYLSRCstmVNRGwPbB3hR5TsQj12mz7TDvnlC1auBBAp3gY8Jb0c2ZPBbZmXzepqaFm7gFwTrqRB",
#         "QjYsDIZ00RwNnxLcAQG4JDMzG6RmlJbui9yFOtYZ440XLRPPLszTWslbzB8lt0wrzK7UWzq3z3banIgMGGgFhiKbgQnrupDpxD66IUhgzP0FsTOOEIZsjSSmJMHPEKZkvcNlF0N94z9i5GDdnzxn71EHrVxPrza86eBkcbOmPMOVFULyVBkwiOkV6zQd9UMS829csYLhhTHciLrc7htLTXaIgGgDWU6O9QuBhiV1zc4GV0Rtr9rwuXeAn95EOOvN6D157nqzNSFJy89w3eprHRvm5sclb053k1nS2haV7BLNmhjmNxhAdLe14LXPLoalOPkR2BR5pUMy94mnB9Nhkzm0UF6AUGr52JNzhGi1BAYIj4xrfryvioziYrLX6XoqDMjVcNOFNKQB3MtO0o422eWwWXIUrt2ZvzcJHFZnX1dObWe7BoQ4KaiJTrk68BZgDXFPZfXUQ1ToyTd9fwZEfZ9Rpap1kduGDepBRGOVtEjLxIpzDGfZikdnNbSeWHxak4ABqNMf0iKiSdjfJXOHaQhNviFtdhUKF8yKc2oB3dvlqMUydJaM8ghvPQHr36jFMuHDBYZ8ywzFYSsVdHQZjSWKNLwsraaexdLSnUbDUCZYRYhV5vnbxMsL4hlRl7AueYhsDlUAW4UdlWT4nMo1BdnFqevj111yN0qEBjTLWJc0PbZqPRcKeczKs3CiH6A8KEHpZnMhRbQzRFRl6EgDoCCzZQBEw42ntXu0nCjLspDB3xyFgBaJrOXvf5UF7kFyEsukyFuzgWno6Kyoc0JLbtobro9d2TnDMLQF7ZlbrkO3ffi90gfV8Kfv2V1brduAKncL4RflrCCPo9aYcoRNjXe5YdZvsHhuMExfD2M6Ke0f91KkkP20LxuNEOkM6ddrK6k9dSf6snPsfI9ymfZedzMZhyNxbVItEsAlrqrpjCxU6rehMlu0Q3IYnpgxPtReC6vIobKal4SQPWZrzqtG7k16BN9cCxgpcAy74hIEAwWkxM4GzKqgu1ur7AvunIWg",
#         "X5Ju3C5027dGdZQzN7fztR9fJgWEytM0zdeo14gbYqmWWC4nWqFXPQXemEqDLsSRRHV5zCmXzzQqUXkSmLYg9hLxyPz61tTCEKgZPJNGBIv9oQCdNxLvs0pswRMuN2xiMASor1KT85nVgs81AV6k2LeLbj4uyR4cTk8OtXGkyoI1KjzO9AdzJjDXXiEd3rLIPEusWvslXPTPXPYH4DLaYzGtsQTHMfsSpXqVHfDrzOjVcRalrcnDoiFbfuARr3xK0bf1zbYwDZxdVLKfFumD4EWR9yPDB177W3utGQq4jfzC7C7v8zqUwbH5FaReYkIOTUbftTZMPSceYc01Ldr2uZfH9aLrv9Pg6WuWvpF4MvVIkJmOuFPkpyFIa6IRYi2igksj1w95ee6Jo1qmmB0MmKcPvRjaJrAnLmbWMHHTfirHmDCwPeuVauyojZpW9BcpQnPzKf3MQfyGn3z7XEhc7GNi5C8gfcIeuYUJzBoBh63uZ3MbkZtXPk6nkLZK8hanPCZsSwWBd4efkJsvQaBfe4ZixCrJeM3XDn7xdzgsheIlFeDLOwgVFW1NRYH86ARttVQLEzOmME8l9A6JJKvHS4FCIiJ9EQxt5GFgnoIPYAsyDgZI4Anaj9bAfsRzxZPhg476EnAoNmTpwqiVnq3X7qfcvTr1vNRtzHvx3UwncLMG4fBaqxB1UJwk0ENp4q3LhPxAHWAJk7SS5UyNXbWXNc8FLrziepie5PqYmoGCiFCXVby2dovQLCnlECXq7KYQUj2JXHSyRwIFGKZ1RS530aCnhjkdYgignG8iv1HN5JcVOELxitq84ykyWbx1FsHqE4J7AEp56jx51og7qTKSMy7VxiFRB8dL5rEjFn885uSDVIMQVRyjT8Y8enw2iD2QtL9TwffL6uAc0YHAq93mCwrU5Y06hGBSyEw5lvgdkHUKfxH6kSO2SZfPV7403UxKHY0ctQiY02bAB8VNR82KSoSIG2NhuWhdO51WVFb1Wtvny2aO7MTf5ArApRIvxbrL",
#         "vmc8h4SsgvTHOeqSg73WzdpL1bgq1eWVTDe6EooiUN6fAkFIisn1iJSQAzN3mLduT6RYGGQFrGOGqCinrbF2UmKujFxaLz1UiUYeOwRjvafjO1p4HiMEpodm5qR3VCqTww50KEOtxMtac9cLdHiqEqJF2f9tdWsAMoSh8BEBpubgBiFCzqe6YMzKH0kJdpI0MWKOaEmuNJmjkPU2FX2vclWwLTPOycNkh7tnyrz25oF2JxmygvgS2FZfkzCcT3clfcwS1bVfItR5WhdB7RZrnxs1z4mODQF7PBe2rrEYzgdRqOPFt9VpeBqh9JMlG5dpT6ogWEhDoQDDuBNvklAlKqKvVJ8pfIj8mZJridWkHgsDqsFfXEzAFERX76IfMTYaKzVeILxOrfmjc9HNbcD7Jm5x1cefGcYWsGJlTXCFLKp9jBQAPOt6dw67y6hvHDiw8VHv6Jktb4T0DJjPomgEb0OeLwlZiudJi0dufXkbqOoQRW4nPNUFAVagnXIz0jt6J7OchMjuX1kQIne8tVacyn1EoWzEpX7NYfgcBPqXssSKRVCRzkB3u53OHtWbya8mLzQAQNPi6UFbI6VD9ZnSLghiTwvNGE5ikLmpz8C0Kr5XYZGotiqjfNWkXfkhlODAoV4oTqTUDmcoLzCBuE8DFsCg6JRpgPMDJpaJ92SS78HdglTZh504koa6mD5AkKBuQRlXXaSgYK7NkQZ6o4fysfg0cEwtr2LcRYG4YE5Vt9jkcGSltvswohHaT64AiDWfT56qvLbmbcurL77Mnv40FwPnBglCVwd1MitjUGxIE1F5aioUdHIqZJiIn2pscQLFe7K7wg5NXESHGg88W7IP1W74BU5okPWejdEVzCa6RAVyfJaG7QIE1Z4OblOPbYGEIzuCEjbid22snfcKsozRWHKlmrMDPZLyFQQ1a2vyGjGsfDFhrUiurv6LR9czWOxT3DdIbmzQnAKcU51HSRuQr7P7l8gAgqkLh9iIhULLuFyFRTnE8h7DEbZP3Ytv6XFn",
#         "qV1YmaKsyVfBUQ7MpSNCDNpNeKehh1Umj1mOXJH4KcVkaUPR2Jgi2ceFqXkejhpToYpNylLa94zTXxNPwEgoQce0mp1BXDvMLrnRBDOOR8IiCLUqGNZoRDHCmOUdwbwwptV3iZYXiikiMQvCoTXJRixlcVo9fnuBegmc98WfkswadPaLSgSuEomNACB8olfHWLhUWDqgQHl1CC4izmRsdiA5SDsKkiN0TST63n2fE8pyn7tTZM3bdSg1Attaht9EKCoCKqJPpkhKx5KM51jY8m69BUyYNjVyzdnlk54VjoI7Vit77qJpkq2W16AMq2LMTOIeRkRjpNziKOfoRXZ36VVnxZ1uJ75cnkmB07mAQyDoPZ5TfmENKqN1rpwHoKeWNq7rIw5D4xY8JUZnLQzKDgSC2gF8ztK5mRgIV6s61RuPpkuMBJNmsXJl443T9ZGQoct4WAF95HnXcVdnF19q5CtaRPsAzR8o2PKTCBqisfgHAs3Ph6R7et2i9adX7Dkr2fShFZswIoHrrXarryzq9DAzgvIap0d8zSAwTIpX3gntfkeGYmG6N8NFOJAz0B5HI6SixaJYklDMBAFYsltKM3cgEYpDnaZWlhmCePYLQc3rS2LsVy62FQTEc7EBPwPNHygzpJAfxxCWmAY3NBFj0SEat53dh5aopmq8FrJVHKgaQueAu1fFEEKy1HFVzFS7PMv55MYKbwRI2F4OZS280rUaISi47FNu9ZDFqSqWAMBHxDZMXbHGwLSu758jFDj5XkozYGukHr90vq6DfHxUhIDybmm6f0CPARWM04gbkUM9HEl5slzvQXjaCgp7XFQIunAm1oGBA7ZKiaMUSQDJw8BEwtbln1Y6day5TgQn6pGMtZ04JkaHGCRAKSN34y2ukEWNxGY9WI7YTiznrm0sQ5Vn3V1xkY3bx4t8tJ0vPUinL8WexKOOlhRJl0YXivlXKBIdbb5idfRcIFGZe5WuhGgql8GdueSgVdkFGixkZWG5ENPHR4pZtksXIgbVxQJz",
#         "6nnyNOx6sfwgrS8QVpUZ6XmYywcTndtMivFuKa72tGQMDSpT1MpBLt6I9pUG9VSF0H5YlsraiVDSi8x03fy3CmIelC4CdHmrJf9oIeyiQpRk2IFHFSdAjpXxglZ4tHeUNywOreWGGtwYLBwkZY00KJcrLdZJByg04AEpQPxHOQV7wDiLEZxRGcY4EeMLcrcRV4SQFwY2GgPD3qEi9PNupn2E2ItqRgN1elPla9vnG8L0gsfdVbzMGI5tjUWEPYvxfbR0jrwmdRYJdeL7pXdCmLgWqm21K6d0eXh9MhndAxGupkEXuUM3u1tJSlmjNGST4R1wtwlDSsIdlVPFpAhS27DTC9LnLzoccDYvu77bie8mA7JoZNpjuquvBNYEXNWbCOn4zRsYNl86HWAe9JxjqMIqifs4kduZjbjQD0LVN7QpTm3W7sloA3Hu0mTpfG8V4ZBavvLc8CEGt3PmEfdOhcBdHksEr8e3vZoUoMtgKNt70kw2I9Yunch4oPSgX1CGapPgFvJ5ukfYQOqCOlGJxDxpAt5leZq5rjwJgAaAyZds3taOo1Tj9OwPZZynlMiIIiiiYm3ljHUgdkyBDjP0kkRNB1eEojtjumj9GOACPoaPkt9wpMuMYScyC0AOmGoJW4anA8CbSL4xZhJ0dBn0OcIXcrr3DA0DmxXw0noDXk65ITMmxG8lV2ZtoSedWILw9IctULNv2vgYL82tSeLREioKoR4YZZ61EWXn7HR4lhqw9FKuRr0LAOxpdzwpzQ9UJAeehctrR2vbmh7OIu1PDzmQ43wig59wiHn4Z1tvPjzKTlvV8jPQJ17Z6pG9a042u8koJmK7rbWiMmmHYLrWc8q3NelHKvJNixYEoHeEK54UoiRUrIP2UOGQZx6OeSKz8NEnuU6aSGPNGnmWjxBjOaGMg0REYw20g20UJiuuPbniaOvW2nEkP0gTF9VD5zLCnUq3MdND6FBKdnZqklzsI3L0Vf0kSvr9OAjCaftYvTxZE9cCt3bb5ah0CaOAe9o1",
#         "x4MkYYBeGr9QsebSsnwNIZMI7hYwhTdtFtbxi1g4rlhWtKYsfD5nLPEjMeDAv9znPjmzxzFfk7Q7HW2KRKQF287UfnT5f0qN3mTMFJ8seFhyixOCToLRH1iFBcCFgyReMiOaZuNA6IGuCYd1hX9HHj9ANSTJKXLWiVx0Jvd1EmXqVsdZ03kyOIeCb8lOJupS0cqaQ033awz3dSmy2m4TtFMc9fi0cF7VBOcsdfRyvgzfyrBbi44wEZRyJNhX5SwjoBUwDDa7XLFi6NsBg4wC50Zh9z6Ja0yMDFE3ShbIttxrj5geGy0uwKMF6j7jJrrq9Vxt8JyRewt4Koc97VxefY1MZ2CNddhPTLeka3gjg3x86CK1Npnb4N72rRHY67XNrhvKQKefh8yFzI6F1DGGV68A9wliAuVyOguaeclhZbEEeoa8TWZcDJbQyJaykisiKyD7Ji6dKaQTiEWhK1wbxDvQBI1TyitrptDHXcCtsyJSkSNArmV9gBIET3r0BiN6VRwVUErKhDeBBepuXu0v5NBbVucwp1WtHSNw8MiMknLykkw8Lh9FbRm6TQXErR26AiqKvagYzZv43TqGNZG4QcRMQTdYOe6m3GLGDwrJ7WS74hacGNa5hrEv7gRA8NjznBwpCsURz5EWfhgYGLMzzdyDOQpGUy7dMsvK2akrhPqBJzoSXa23LmpzDHlgAbhtXl4cWBYRFjjRItjt44TxhDFXd63UJHQnY0GlsJxPA9JkS5fDPKeeDbyRK7NCUERXeYXt5aygXA6n4s4eTXDBbrVFvCwfYNzyZ1eLstksvgAXNWujFW7kwjmSyz60YdHoidm8dqtjHCil3ARKm8a8wqcXo3gAkco8r00cErTIcpyGJ1ZbWdkSvu4t58YkjChJMcFb1bJCjXlNVTraq7wuDvP54nO28Ar60OaxvdUgAGULC9WKX4pOxAu1wGg2L0ze7JiHHEytNA1QhfEyMOtbBMqxuprn3g9BSSo1FrdKUyhznETpy7yibCsot1M9If1t",
#         "UPDJGLKgvJ7OpPT8ipiTT9KtzfJgy4HH3XpZpkDjtseRjbW7g9sCwCM4HljAVJ7OnsbZdY6Igy1mxJaczuUoL0RMst8E1wd1lzmoiiCWXTUFx3fduJv3EhenNitPjX6HjrYC6ZQ5YUhcmn1p2fJ9DhSe3iErtugOjbEflJIVnAmHCajBboPrrly9misnbtB7G0NOeTVk1HsTk6Osx77LLAeLH4kbKwMgVXVN59zeeErueyh5YBYhupqwQPioxI0O16DPNJbTcAoKZUfFyo2o0VYkD7YWGTjAQ1QKi195lpHuLBBju4vNkudHBiusc6l2O9wCa3Uwaol94knXvtxIpLHGTEHV02JKGfqSaJ6rxMWqurM7AimxEANh2aumPp7e7lb1xFp9e01VWDjM5r9QPLM9xaeS1dpA9DqyEGBsrIV9UDiiTE01plhAzneBMZwZCWCXSVWBbANSz4zGw6CGnLzx847e9d05hEWgBofytKEb32W6nL4xHvuNnGXfvNATTth4150hv23JEdPSoRQz3jVy5AX2HYae0EvG4QFcPiWZUB6hYO0Fo54owyq7WVVsz2AhYbFeV0O5azdZnI9m6TM12rUUwsicYilO7sHnsSE9eF0gpWQpTCxrtyT5pyA9OKElduPBzCFCBXhKrivKk7oVqwsjkIBSVsTkDrHMsLKbNVGHXaAXOiXtVBSNUngAmyiLarsWMnBDUQipZagN5JoCy0QU6l4mMPANjrZ57KXfzzNo4FKNo733oPIsyjL1vZj7MI2oIWHiMYxe3T9xNTzeeiVAdpQGxoMg6oBnk9qejMndj0PKSm1s7lZiodv4EgCbwPi4zKfnFf2wNRms7AYTXSHGLCh5IMefR2fmRBCgsCa5v9Xw5RJiijN4aEpNxblYGrrSHeECK4L2VzR9J4GMKbSwfIhFDvrOaSyJhuqpgMuTORfFqjHLMMic1GFuVy8Ya1yg2h5xyNuiw0zu4NjvFUcnJ547xFh2IounPZ7qZcZpmRwlTk6TJLhG17eK",
#         "DTzC1iH2A9Y0HOdwmvHBrvO9pLo3gvNsTqoBZXW2XU905u7pOhzOgpHbr1isQhefM2IMuZZXS7Rf21DJhU0x1PCPsC64FiR0jlAuthZY0m6x58OxNlzNN9lBvL4AoqkowZDcJQUr6a2KzS9hWv9ihmzcVMMcf51PyA7gz8BAQbhXfiqEVVWpgigdcGV1h4JTWuaQyt9IglFI0NaE6TQpfVq8qdT9Ea4LlHygM5aCP8HZMqPi9ElcARU0iAa2scTRCpEjGjyLlMQxGMwoleCwKrHX4Wuer0mCqxlRT0bOKEgzvWAFDaAhupoeEUGcyb1Ope6qW7RCfyYNr8LffQAkbMXuXbSqsUcMA1wO3YlxkHgQSCXuK7n6qZDfBxf9jfJoLLz7NswTWMEm7MnO8w2GLSiPLRl8m2YEdymRJyQJihvWIrsqVJg4QjJXtyhmbf1FbMYU9IIGNttjW8kc6lbeS7QxeqfdUet9MHiIDE6xtBcJkAgmfpxgUDkLgHBhQDPL5Gj4hC2NCdJWjEJ9vZD6e1PBR6sspvN5HOzDOXpLgs7gxPeerQsBcwcJpZAbYBHVPqvATLGdHWHW4Q9M5vFr32BfFgEkhB1VHtlp0K3QTZeXCevJwyt8UIXHaMkXAQOzaV5cQ9FSkst20hz1jxzb6tL82bwRfkvdjAyrKLgmGB6kwlXD7XuC6zKtTaRLNXfJghXuRyJxBACzp9lS0LA4x92aT7Okym6YOTwUOMjgEZDSLmmlPGF6akoODg0Lenef3GtdCytAiDE4GbdQL6r6rRdfYkp8zuOSsibAnVyI7VYOXcFfyLZBTRxn8wJc73CZxK5gO4GcT1hmfCkJMndVmOvjMpbgnJhE5mATMNc7ipnCSYqc9Zg482IZxQ2HAQLM0SCFRAkNDOlmddVp61I7sJkkS5xtKPRWMIRNSIZmvU5Qed1ATo76qV3GlUjxpiEg2MaxtZQpkwqvAI8CwOQ8YwWXOv5HFW6avNY4N8HIZgBNL9LFFhsusgwHCZQnCunD",
#         "dQnWDmSPwJINNy0m15GdsFKLNloZzwA1yNi6EQygfB0L4DoqfCr0EtUrDyTO066v53QIHWhVXlV10hFHg3i9k00bZ8sdBouSBmbnOhDdUdyKxt3UvYS4ErmFAnxPBWDXN6jTux4U9fPy4JbuuVAoL6WbGQ7j3WI5N3lygiJsRF5IauMKW8GJ1B1fzYi0pskNxnJkIxzhbdCQD8tRRgaR1YnkaBOKhiUEKMeYrBSfVkqSVNSa4InYFeCHxHGNM6XT3td9dkAKU2J1NCWuKr48P6hqVTnSuiEehoB9TR0jh8bgyR0fmXvLmynlkvo3uI2M42sLmBJQVp0JlNQt3lJjB3XwjRXUHv8wZspsbI6DYden4PrMUrxq2UX0LNT3GrnEazJA0OmStNBL3rKxNquQJEaTp44QQDI2PyIpcA2TGd3CEjGAVujDJN38UVF8sZzws2J7YLY1R6i0E8YG8Blkj3uKecHIrBioj1rN1d03HOk2IR8Cgfhw9INXxyflwusMW9EkjbkHDkRix9tPP8xAS2QPZn6YHsqy5zW6Z9ELBF2Vk8HeVklJcdR0aZNLaBDzJtUtj7BQZHMNPVNJpjX5A6j9qNeYBp2uKJESvHBLn3ec9Mwu3fLVCTWXXnFRAz0x2KMT8NlfD7W2jvIFB2k3N3Z808K5nKFophIYI3rGjyOOzjBSNZfnm0DbPTmxMoj6V4u5HZGlMtiLqw2V8WR7e0dGa0BiFzA10RzWaHdP7XkBh9g4OK6AnesxSKGy2dcKEyn9BUgeYR2eVSkSDooImtcWueO0sOqsygUraneVgkcg4LWkFbMAk9TrXoiEbMuReBqG8I9pPRZ7carmjC3V1DeDbcdlMJE64XlY8okqTjq6IkhrKe8qWAYWiTapOLuXayRoqkdOwrNGGOP4e2q8qwzhysP28se4yV08pVRDOZaysUj72PNSY837RaHVGtX9EIEEiD7Cmp3Og91cwlobhhc1Epu1ZvfYayUBvWdsw1MrD3nCjfBfNz0dh8tiwXOX"
#     ]
#
#     return random.choice(hashes)


def tc_calculate():
    code_object = TC.objects.get(pk=1)

    # Mv2Qx0Aa0
    dig = code_object.code[-1]
    code = list(code_object.code)
    if int(dig) == 9:
        dig = code_object.code[-2]
        code[-1] = "0"
        if dig == "z":
            dig = code_object.code[-3]
            code[-2] = "a"
            if dig == "Z":
                dig = code_object.code[-4]
                code[-3] = "A"
                if int(dig) == 9:
                    dig = code_object.code[-5]
                    code[-4] = "0"
                    if dig == "z":
                        dig = code_object.code[-6]
                        code[-5] = "a"
                        if dig == "Z":
                            dig = code_object.code[-7]
                            code[-6] = "A"
                            if int(dig) == 9:
                                dig = code_object.code[-8]
                                code[-7] = "0"
                                if dig == "z":
                                    dig = "A"
                                    code[-8] = dig
                            else:
                                dig = int(dig) + 1
                                code[-7] = str(dig)
                        else:
                            dig = chr(ord(dig) + 1)
                            code[-6] = dig
                    else:
                        dig = chr(ord(dig) + 1)
                        code[-5] = dig
                else:
                    dig = int(dig) + 1
                    code[-4] = str(dig)
            else:
                dig = chr(ord(dig) + 1)
                code[-3] = dig
        else:
            dig = chr(ord(dig) + 1)
            code[-2] = dig
    else:
        dig = int(dig) + 1
        code[-1] = str(dig)

    new_code = "".join(code)
    code_object.code = new_code
    code_object.save()

    return new_code


def movie_month(num_month):
    months = {
        1: "Jan",
        2: "Feb",
        3: "March",
        4: "April",
        5: "May",
        6: "June",
        7: "July",
        8: "Aug",
        9: "Sep",
        10: "Oct",
        11: "Nov",
        12: "Dec"
    }
    month = months[num_month]
    return month


def user_details_updater(user, genres):
    for genre in genres.split(","):
        genre = genre.lower().strip()
        print("|" + genre + "|")
        if genre == "action":
            count = user.details.action
            count += 1
            user.details.action = count
            user.save()

        elif genre == "epic":
            count = user.details.epic
            count += 1
            user.details.epic = count
            user.save()

        elif genre == "drama":
            count = user.details.drama
            count += 1
            user.details.drama = count
            user.save()

        elif genre == "animation":
            count = user.details.animation
            count += 1
            user.details.animation = count
            user.save()

        elif genre == "thriller":
            count = user.details.thriller
            count += 1
            user.details.thriller = count
            user.save()

        elif genre == "horror":
            count = user.details.horror
            count += 1
            user.details.horror = count
            user.save()

        elif genre == "sci-fi":
            count = user.details.sci_fy
            count += 1
            user.details.sci_fy = count
            user.save()

        elif genre == "fiction":
            count = user.details.fiction
            count += 1
            user.details.fiction = count
            user.save()

        elif genre == "fantasy":
            count = user.details.fantasy
            count += 1
            user.details.fantasy = count
            user.save()

        elif genre == "historical film":
            count = user.details.historical_film
            count += 1
            user.details.historical_film = count
            user.save()

        elif genre == "musical":
            count = user.details.musical
            count += 1
            user.details.musical = count
            user.save()

        elif genre == "christian":
            count = user.details.christian
            count += 1
            user.details.christian = count
            user.save()

        elif genre == "romance":
            count = user.details.romance
            count += 1
            user.details.romance = count
            user.save()

        elif genre == "sitcom":
            count = user.details.sitcom
            count += 1
            user.details.sitcom = count
            user.save()

        elif genre == "comedy":
            count = user.details.comedy
            count += 1
            user.details.comedy = count
            user.save()

        elif genre == "mystery":
            count = user.details.mystery
            count += 1
            user.details.mystery = count
            user.save()

        elif genre == "adventure":
            count = user.details.adventure
            count += 1
            user.details.adventure = count
            user.save()

        elif genre == "war":
            count = user.details.war
            count += 1
            user.details.war = count
            user.save()

        elif genre == "crime":
            count = user.details.crime
            count += 1
            user.details.crime = count
            user.save()

        elif genre == "western":
            count = user.details.western
            count += 1
            user.details.western = count
            user.save()

        elif genre == "documentary":
            count = user.details.documentary
            count += 1
            user.details.documentary = count
            user.save()

        elif genre == "sports":
            count = user.details.sports
            count += 1
            user.details.sports = count
            user.save()

        elif genre == "disaster":
            count = user.details.disaster
            count += 1
            user.details.disaster = count
            user.save()

        elif genre == "investigative":
            count = user.details.investigative
            count += 1
            user.details.investigative = count
            user.save()

        elif genre == "biographical":
            count = user.details.biographical
            count += 1
            user.details.biographical = count
            user.save()

        else:
            print(genre, "is not found in the database")

    return None


def calculate_pay(user, no_of_episodes=0):
    cash = 0
    subparts = ceil(no_of_episodes / 14)

    if user.details.subscription == "not subscribed":
        if no_of_episodes == 0:
            cash = 30
        else:
            cash = 30 * subparts
    elif user.details.subscription == "standard":
        cash = 20
    elif user.details.subscription == "pro":
        cash = 15
    elif user.details.subscription == "pro max":
        cash = 10

    return cash


def subscription_updater(user):
    subscription_date = user.details.subscription_date
    if user.details.subscription != "not subscribed" and (timezone.now() - subscription_date) >= timedelta(hours=744):
        user.details.subscription = "not subscribed"
        user.save()
    return None


def user_details(user):
    count = {
        'action': user.details.action,
        'epic': user.details.epic,
        'thriller': user.details.thriller,
        'drama': user.details.drama,
        'horror': user.details.horror,
        'comedy': user.details.comedy,
        'fantasy': user.details.fantasy,
        'investigative': user.details.investigative,
        'sci_fy': user.details.sci_fy,
        'historical_film': user.details.historical_film,
        'romance': user.details.romance,
        'mystery': user.details.mystery,
        'sitcom': user.details.sitcom,
        'adventure': user.details.adventure,
        'war': user.details.war,
        'musical': user.details.musical,
        'documentary': user.details.documentary,
        'western': user.details.western,
        'crime': user.details.crime,
        'sports': user.details.sports,
        'disaster': user.details.disaster,
        'biographical': user.details.biographical,
        'animation': user.details.animation,
        'christian': user.details.christian
    }
    total = 0
    for value in count.values():
        total += value
    count = sorted(count.items(), key=lambda x: x[1], reverse=True)
    tempdict = {}

    for movie in count:
        tempdict[movie[0]] = movie[1]

    return total, tempdict


def create_superuser(request):
    # Check if the superuser already exists
    if not User.objects.filter(is_superuser=True).exists():
        # Create the superuser
        superuser = User.objects.create_superuser(
            username='phillipsaint',
            email='phillipsaint254@gmail.com',
            password='milacre4321'
        )

        # Customize additional superuser attributes if needed
        superuser.first_name = 'Admin'
        superuser.last_name = 'User'
        superuser.save()


def index(request):
    call_command('makemigrations')
    call_command('migrate')
    create_superuser(request)
    comments = Comment.objects.filter(useful=True)
    categs = []
    display = Movie.objects.filter(
        Q(year=2005) | Q(year=2006) | Q(year=2007) | Q(year=2008) | Q(year=2009) | Q(year=2010) | Q(year=2011) | Q(
            year=2012) | Q(year=2013) | Q(year=2014) | Q(year=2015) | Q(year=2016) | Q(year=2017) | Q(year=2018) | Q(
            year=2019) | Q(year=2020) | Q(year=2021)).order_by("-views")[:50]
    latest = Movie.objects.filter(Q(year=current_year)).order_by("-date_of_release")
    if request.user.is_authenticated:

        most = 0
        genre = ""
        total_movies, movie_dict = user_details(request.user)
        count = 0
        for view, value in zip(movie_dict, movie_dict.values()):
            if count < 5:
                categs.append(view)
            if value > most:
                most = value
                genre = view
            count += 1
        views = Movie.objects.filter(Q(genre__contains=genre)).order_by("views")
        subscription_updater(request.user)

        if not request.user.is_superuser:
            return render(request, "movies/index.html",
                          {"movies": views, "comments": comments, "display": display, "categs": categs,
                           "latest": latest})
    else:
        categs = ["action", "epic", "investigative", "horror", "crime"]

    if request.user.is_superuser:
        if request.method == "POST":
            if request.POST.get("admin"):
                transactions = Transaction.objects.filter(Q(status=False)).order_by("created_at")
                return render(request, "movies/admin.html", {"transactions": transactions})
            elif request.POST.get("index"):
                return render(request, "movies/index.html",
                              {"categs": categs, "unverified": False, "movies": latest, "display": display,
                               "comments": comments})
        return render(request, "movies/index.html", {"unverified": True, "comments": comments, "display": display})
    return render(request, "movies/index.html",
                  {"unverified": True, "categs": categs, "movies": latest, "comments": comments, "display": display})


def series(request):
    all_series = Movie.objects.filter(Q(movie=False))
    rand = random.choice(range(1, 20))
    total_movies, movie_dict = user_details(request.user)
    most = 0
    genre = ""
    for view_genre, value in zip(movie_dict, movie_dict.values()):
        if value > most:
            most = value
            genre = view_genre
    user_series = Movie.objects.filter(Q(genre=genre)).order_by("views")
    latest = Movie.objects.filter(Q(movie=False) & Q(year=2022)).order_by("views")
    most_viewed = Movie.objects.filter(Q(movie=False)).order_by("views")[:100:rand]
    most_searched = Movie.objects.filter(Q(movie=False)).order_by("searches")[:100:rand]
    return render(request, "movies/series.html", {"user_series": user_series,
                                                  "latest": latest, "most_viewed": most_viewed,
                                                  "most_searched": most_searched, "series": all_series})


def all_movies(request):
    all_mov = Movie.objects.filter(Q(movie=True)).order_by("name")
    return render(request, 'movies/all movies.html', {"all_movies": all_mov})


def all_series(request):
    all_ser = Movie.objects.filter(Q(movie=False)).order_by("name")
    return render(request, "movies/all series.html", {"all_series": all_ser})


def latest(request):
    latest_movies = Movie.objects.filter(Q(year=2022)).order_by("date_of_release")
    return render(request, "movies/latest.html", {"latest_movies": latest_movies})


def categories(request):
    return render(request, "movies/categories.html")


def epic(request):
    movs = Movie.objects.filter(Q(genre__contains="epic")).order_by("views")
    return render(request, "movies/epic.html", {"movies": movs})


def sitcom(request):
    movs = Movie.objects.filter(Q(genre__contains="sitcom")).order_by("views")
    return render(request, "movies/sitcom.html", {"movies": movs})


def drama(request):
    movs = Movie.objects.filter(Q(genre__contains="drama")).order_by("views")
    return render(request, "movies/drama.html", {"movies": movs})


def investigative(request):
    movs = Movie.objects.filter(Q(genre__contains="investigative")).order_by("views")
    return render(request, "movies/investigative.html", {"movies": movs})


def sci_fi(request):
    movs = Movie.objects.filter(Q(genre__contains="sci-fi")).order_by("views")
    return render(request, "movies/sci-fi.html", {"movies": movs})


def war(request):
    movs = Movie.objects.filter(Q(genre__contains="war")).order_by("views")
    return render(request, "movies/war.html", {"movies": movs})


def crime(request):
    movs = Movie.objects.filter(Q(genre__contains="crime")).order_by("views")
    return render(request, "movies/crime.html", {"movies": movs})


def historical_film(request):
    movs = Movie.objects.filter(Q(genre__contains="historical")).order_by("views")
    return render(request, "movies/historical films.html", {"movies": movs})


def fiction(request):
    movs = Movie.objects.filter(Q(genre__contains="fiction")).order_by("views")
    return render(request, "movies/fiction.html", {"movies": movs})


def thriller(request):
    movs = Movie.objects.filter(Q(genre__contains="thriller")).order_by("views")
    return render(request, "movies/thriller.html", {"movies": movs})


def adventure(request):
    movs = Movie.objects.filter(Q(genre__contains="adventure")).order_by("views")
    return render(request, "movies/adventure.html", {"movies": movs})


def action(request):
    movs = Movie.objects.filter(Q(genre__contains="action")).order_by("views")
    return render(request, "movies/action.html", {"movies": movs})


def musical(request):
    movs = Movie.objects.filter(Q(genre__contains="musical")).order_by("views")
    return render(request, "movies/musical.html", {"movies": movs})


def romance(request):
    movs = Movie.objects.filter(Q(genre__contains="romance")).order_by("views")
    return render(request, "movies/romance.html", {"movies": movs})


def christian(request):
    movs = Movie.objects.filter(Q(genre__contains="christian")).order_by("views")
    return render(request, "movies/christian.html", {"movies": movs})


def animation(request):
    movs = Movie.objects.filter(Q(genre__contains="animation")).order_by("views")
    return render(request, "movies/animation.html", {"movies": movs})


def biographical(request):
    movs = Movie.objects.filter(Q(genre__contains="biographical")).order_by("views")
    return render(request, "movies/biographical.html", {"movies": movs})


def disaster(request):
    movs = Movie.objects.filter(Q(genre__contains="disaster")).order_by("views")
    return render(request, "movies/disaster.html", {"movies": movs})


def sports(request):
    movs = Movie.objects.filter(Q(genre__contains="sports")).order_by("views")
    return render(request, "movies/sports.html", {"movies": movs})


def documentary(request):
    movs = Movie.objects.filter(Q(genre__contains="documentary")).order_by("views")
    return render(request, "movies/documentary.html", {"movies": movs})


def western(request):
    movs = Movie.objects.filter(Q(genre__contains="western")).order_by("views")
    return render(request, "movies/western.html", {"movies": movs})


def horror(request):
    movs = Movie.objects.filter(Q(genre__contains="horror")).order_by("views")
    return render(request, "movies/horror.html", {"movies": movs})


def comedy(request):
    movs = Movie.objects.filter(Q(genre__contains="comedy")).order_by("views")
    return render(request, "movies/comedy.html", {"movies": movs})


def mystery(request):
    movs = Movie.objects.filter(Q(genre__contains="mystery")).order_by("views")
    return render(request, "movies/mystery.html", {"movies": movs})


def fantasy(request):
    movs = Movie.objects.filter(Q(genre__contains="fantasy")).order_by("views")
    return render(request, "movies/fantasy.html", {"movies": movs})


def suggestions(request):
    if request.user.is_authenticated:
        most = 0
        genre = ""
        total_movies, movie_dict = user_details(request.user)
        for view, value in zip(movie_dict, movie_dict.values()):
            if value > most:
                most = value
                genre = view
        views = Movie.objects.filter(Q(genre__contains=genre)).order_by("views")
        return render(request, "movies/suggested.html", {"all_movies": views})
    messages.error(request, "Please login for us to suggest movies of your liking!")
    return redirect("movies:index")


def movies(request):
    most_searched = Movie.objects.all().order_by("searches")
    all_movies = Movie.objects.all().order_by('name')
    most_viewed = Movie.objects.all().order_by('views')
    latest = Movie.objects.filter(Q(year=2022)).order_by("-date_of_release")
    latest1 = Movie.objects.filter(Q(year=2021)).order_by("-date_of_release")
    top_rating = Movie.objects.all().order_by('rating')
    movie = Movie.objects.filter(Q(movie=True))
    series = Movie.objects.filter(Q(movie=False))

    if request.method == "POST":
        if request.POST.get("all_movies"):
            return render(request, "movies/movies.html", {"movies": all_movies})
        elif request.POST.get("most_searched"):
            return render(request, "movies/movies.html", {"movies": most_searched})
        elif request.POST.get("most_viewed"):
            return render(request, "movies/movies.html", {"movies": most_viewed})
        elif request.POST.get("latest"):
            return render(request, "movies/movies.html", {"movies": latest, "latest1": latest1})
        elif request.POST.get("top_rating"):
            return render(request, "movies/movies.html", {"movies": top_rating})
        elif request.POST.get("movies"):
            return render(request, "movies/movies.html", {"movies": movie})
        elif request.POST.get("series"):
            return render(request, "movies/movies.html", {"movies": series})

    return render(request, "movies/movies.html")


def detail(request, movie_id):
    movie = Movie.objects.get(pk=movie_id)
    views = movie.views
    views += 1
    movie.views = views
    if request.user.is_authenticated:
        genres = movie.genre
        user_details_updater(request.user, genres)
        subscription_updater(request.user)
    return render(request, "movies/details.html", {"movie": movie})


def search(request):
    if request.method == "POST":
        query = request.POST.get("search")

        try:
            result = Movie.objects.filter(Q(name__contains=query))
            if len(result) == 1:
                res = Movie.objects.get(name=query)
                res.searches += 1
                res.save()
            return render(request, "movies/results.html", {"result": result, "st": True, "query": query})
        except Movie.DoesNotExist:
            pass

        if query.lower() == "movie" or query.lower() == "movies":
            result = Movie.objects.filter(Q(movie=True))
            return render(request, "movies/results.html", {"result": result, "st": False, "query": query})
        elif query.lower() == "series":
            result = Movie.objects.filter(Q(movie=False))
            return render(request, "movies/results.html", {"result": result, "st": False, "query": query})

        result = Movie.objects.filter(
            Q(name__icontains=query) | Q(genre__icontains=query) | Q(description__icontains=query) | Q(
                rating__contains=query))
        if request.user.is_authenticated:
            subscription_updater(request.user)
        return render(request, "movies/results.html", {"result": result, "st": False, "query": query})


def user_request(request):
    if not request.user.is_authenticated:
        messages.error(request, "Please login to access this service")
        return redirect("movies:index")

    if request.method == "POST":
        movie_name = request.POST.get("movie_name")
        Request(user=request.user, name=movie_name).save()
        messages.info(request, "Thank you for your request. We are going to download your movie within the day.")
        return redirect("movies:index")
    return render(request, "movies/request.html")


def deposit(request):
    user = request.user
    if not request.user.is_authenticated:
        return render(request, "movies/login.html", {"message": "Log In is required in order to initiate transaction!"})
    if request.method == "POST":
        transaction_code = request.POST.get("transaction_code")
        amount = request.POST.get("amount")
        transaction = Transaction()
        Sale(user=user, username=user.username, transaction_type="credit", price=amount,
             item_sold="Deposited a total of " + str(amount), transaction_code=tc_calculate()).save()
        transaction.transaction_code = transaction_code
        transaction.code_stamp = tc_calculate()
        transaction.amount = amount
        transaction.username = user.username
        transaction.user = user

        if transaction.status:
            status = False
        else:
            status = True

        transaction.save()
        messages.info(request,
                      "Your transaction has been submitted successfully. Please visit the admin for confirmation!")
        return render(request, "movies/index.html", {
            "status": status})
    return render(request, "movies/deposit.html")


def confirm_pay(request, transaction_id):
    trans = Transaction.objects.get(pk=transaction_id)
    added_amount = trans.amount
    user = trans.user
    trans.status = True
    trans.save()
    amount = user.details.coins
    amount += added_amount
    user.details.coins = amount
    user.save()
    messages.info(request, "Transaction " + str(trans.transaction_code) + " successfully added to the database.")
    return redirect("movies:index")


def delete_pay(request, transaction_id):
    Transaction.objects.get(pk=transaction_id).delete()
    messages.info(request, "You have successfully cancelled transaction!")
    return redirect("movies:index")


def signup(request):
    if request.method == "POST":
        form = request.POST
        username = form.get("username")
        first_name = form.get("first_name")
        last_name = form.get("last_name")
        email = form.get("email")
        phone = form.get("phone")
        password1 = form.get("password1")
        password2 = form.get("password2")

        try:
            user_exists = User.objects.get(username=username)
            messages.error(request, f"User by the username '{user_exists.username}' already exists!")
            return redirect("movies:signup")
        except User.DoesNotExist:
            pass

        try:
            user_exists = User.objects.get(email=email)
            messages.error(request, f"User by the email '{user_exists.email}' already exists!")
            return redirect("movies:signup")
        except User.DoesNotExist:
            pass

        if password1 != password2:
            messages.error(request, "Password missmatch!")
            return redirect("movies:signup")

        if len(username) <= 2:
            messages.error(request, "Username too short!")
            return redirect("movies:signup")
        if len(first_name) <= 2:
            messages.error(request, "First name too short!")
            return redirect("movies:signup")
        if len(last_name) <= 2:
            messages.error(request, "Last name too short!")
            return redirect("movies:signup")
        if 10 < len(phone) > 13:
            messages.error(request, "Invalid phone too short!")
            return redirect("movies:signup")
        if len(password1) < 5:
            messages.error(request, "Password must be 5 characters or more.")
            return redirect("movies:signup")

        user = User.objects.create_user(first_name=first_name, last_name=last_name, email=email, password=password1,
                                        username=username)
        user.save()

        user_detail = Details.objects.get(user=user)

        user_detail.phone = phone
        user_detail.username = username
        user_detail.save()

        user = authenticate(request, username=username, password=password1)
        if user is not None:
            user_login(request, user)
        else:
            messages.info(request, "Failed to log in as user can not be none!")
            return render(request, "movies/index.html")
        messages.info(request, "Congratulations! You have successfully registered as a swifftech member.")
        return redirect("movies:index")
    return render(request, "movies/signup.html")


def login(request):
    if request.user.is_authenticated:
        messages.error(request, "You are already logged in. Please Log out to log in as a different user!")
        return render(request, "movies:index")

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)

            if user is not None:
                user_login(request, user)
                messages.info(request, f"You have successfully logged in as {username}.")
                return render(request, "movies/index.html")
            else:
                messages.error(request, "Login information not found!")
                return redirect("movies:login")
        else:
            messages.error(request, "Authentication failed!")
            return redirect("movies:login")
    return render(request, "movies/login.html")


def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get("email")
        try:
            User.objects.get(email=email)
            template = loader.get_template("movies/email template.html")

            context = {
                "email": email.lower(),
                "domain": domain,
                "hash": Hash.objects.get(user=request.user)
            }

            email_message = template.render(context)

            the_email = EmailMultiAlternatives(
                "Change Password",
                email_message,
                "smh",
                ["swifftechpy@gmail.com", email]
            )

            the_email.content_subtype = "html"
            the_email.send()
            messages.info(request, "We have mailed you a password change link.")
            return render(request, "movies/login.html")

        except User.DoesNotExist:
            messages.error(request, "User with email '" + email + "' does not exist.")
            return render(request, "movies/email.html")
        except:
            messages.error(request, "Email not sent because of other reasons")
            return render(request, "movies/email.html")

    return render(request, "movies/email.html")


def change_password(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 == password2:
            if len(password1) >= 5:
                user = User.objects.get(email=email)
                user.set_password(password1)
                user.save()
                messages.info(request, "You have successfully changed your password.")
                Hash.objects.get(user=request.user).delete()
                return render(request, "movies/login.html")
            else:
                messages.info(request, "Password must be 5 characters or more!")
                return redirect("movies:change_password")
        else:
            messages.error(request, "Password missmatch!")
            return redirect("movies:change_password")
    return render(request, "movies/forgot password.html")


@login_required
def logout(request):
    user_logout(request)
    messages.info(request, "Logout successful.")
    return render(request, "movies/index.html")


def edit(request):
    if request.method == "POST":
        user = request.user
        form = request.POST
        username = form.get("username")
        first_name = form.get("first_name")
        last_name = form.get("last_name")
        email = form.get("email")
        phone = form.get("phone")

        if len(username) <= 2:
            messages.error(request, "Username too short!")
            return redirect("movies:edit")
        if len(first_name) <= 2:
            messages.error(request, "First name too short!")
            return redirect("movies:edit")
        if len(last_name) <= 2:
            messages.error(request, "Last name too short!")
            return redirect("movies:edit")
        if 10 < len(phone) > 13:
            messages.error(request, "Invalid phone too short!")
            return redirect("movies:edit")

        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.username = username
        user.details.phone = phone

        user.save()
        messages.info(request, "You have successfully changed your account information.")
        return redirect("movies:index")

    return render(request, "movies/edit.html")


def account(request):
    if not request.user.is_authenticated:
        messages.error(request, "You can't access any account until you log in to yours.")
        return redirect("movies:index")

    sales = Sale.objects.filter(user=request.user).order_by("transaction_time")

    subscription_updater(request.user)
    total, count = user_details(request.user)
    dictionary = zip(count, count.values())
    days = None
    if request.user.details.subscription != "not subscribed":
        days = 31 - (timezone.now() - request.user.details.subscription_date).days
    return render(request, 'movies/account.html',
                  {'total': total, 'dictionary': dictionary, "days": days, "sales": sales})


"""subscription urls"""


def subscribe(request):
    user = request.user
    if not user.is_authenticated:
        messages.error(request, "Login required in order subscribe with us!")
        return redirect("movies:index")

    return render(request, 'movies/subscribe.html')


def standard(request):
    user = request.user

    if not user.is_authenticated:
        messages.error(request, "Login required in order subscribe with us!")
        return redirect("movies:index")

    user_coins = user.details.coins

    if user.details.subscription == 'standard' or user.details.subscription == 'pro' or user.details.subscription == 'pro max':
        messages.error(request, 'You have an active subscription!')
        return redirect('movies:index')

    if request.method == 'POST':
        if user_coins >= standard_price:
            user_coins -= standard_price
            user.details.coins = user_coins
            user.details.subscription = 'standard'
            user.details.points += 10
            Sale(user=user, username=user.username, transaction_type="debit", price=standard_price,
                 item_sold="Subscribed to the standard account type.", transaction_code=tc_calculate()).save()
            user.details.subscription_date = timezone.now()
            user.save()
            messages.info(request, 'Congratulations! You have successfully subscribed to the Standard monthly package.')
            return render(request, 'movies/index.html')

    if user_coins >= standard_price:
        return render(request, 'movies/standard.html', {"user_coins": user_coins})
    messages.error(request, 'You have ' + str(
        user_coins) + '. You must have ' + str(standard_price) +
                   ' coins or more to qualify for this subscription! Visit swifftech to '
                      'increase your coins.')
    return redirect('movies:index')


def pro(request):
    user = request.user

    if not user.is_authenticated:
        messages.error(request, "Login required in order subscribe with us!")
        return redirect("movies:index")

    user_coins = request.user.details.coins
    if user.details.subscription == 'standard' or user.details.subscription == 'pro' or user.details.subscription == 'pro max':
        messages.error(request, 'You have an active subscription!')
        return redirect('movies:index')

    if request.method == 'POST':
        if user_coins >= pro_price:
            user_coins -= pro_price
            user.details.coins = user_coins
            user.details.subscription = 'pro'
            user.details.points += 20
            Sale(user=user, username=user.username, transaction_type="debit", price=pro_price,
                 item_sold="Subscribed to the pro account type.", transaction_code=tc_calculate()).save()
            user.details.subscription_date = timezone.now()
            user.save()
            messages.info(request, 'Congratulations! You have successfully subscribed to the Pro monthly package.')
            return render(request, 'movies/index.html')

    if user_coins >= pro_price:
        return render(request, 'movies/pro.html', {"user_coins": user_coins})
    messages.error(request, 'You have ' + str(
        user_coins) + '. You must have ' + str(pro_price) +
                   ' coins or more to qualify for this subscription! Visit swifftech to '
                      'increase your coins.')
    return redirect('movies:index')


def pro_max(request):
    user = request.user

    if not user.is_authenticated:
        messages.error(request, "Login required in order subscribe with us!")
        return redirect("movies:index")

    user_coins = request.user.details.coins

    if user.details.subscription == 'standard' or user.details.subscription == 'pro' or user.details.subscription == 'pro max':
        messages.error(request, 'You have an active subscription!')
        return redirect('movies:index')

    if request.method == 'POST':
        if user_coins >= pro_max_price:
            user_coins -= pro_max_price
            Sale(user=user, username=user.username, transaction_type="debit", price=pro_max_price,
                 item_sold="Subscribed to pro max account type.", transaction_code=tc_calculate()).save()
            user.details.coins = user_coins
            user.details.subscription = 'pro max'
            user.details.points += 30
            user.details.subscription_date = timezone.now()
            user.save()
            messages.info(request, 'Congratulations! You have successfully subscribed to the Pro Max monthly package.')
            return render(request, 'movies/index.html')

    if user_coins >= pro_max_price:
        return render(request, 'movies/pro max.html', {"user_coins": user_coins})

    messages.error(request, 'You have ' + str(
        user_coins) + '. You must have ' + str(pro_max_price) +
                   ' coins or more to qualify for this subscription! Visit swifftech to '
                      'increase your coins.')

    return redirect('movies:index')


def buy_movie(request, movie_id):
    movie = Movie.objects.get(pk=movie_id)
    new_hash, num = hash_generator(request.user)
    if not request.user.is_authenticated:
        messages.error(request, "You have not logged in to your account. Please log in to access this service.")
        return redirect("movies:index")

    if request.method == "POST":
        parts = {
            1: "A",
            2: "A and B",
            3: "A, B and C",
            4: "A, B, C and D",
            5: "A, B, C, D and E"
        }

        seasons = []
        for season in movie.all_seasons.all():
            if request.POST.get(str(season.season_no)):
                seasons.append(season.season_no)
        cash = 0
        info = {}

        for season in seasons:
            episodes = movie.all_seasons.get(season_no=season).all_episodes.get(season_no=season).no_of_episodes
            cash += calculate_pay(user=request.user, no_of_episodes=episodes)
            subparts = ceil(episodes / 14)
            info[season] = parts[subparts]

        season_parts = zip(info, info.values())

        if request.user.details.coins >= cash:
            return render(request, "movies/confirm buy.html",
                          {"movie": movie, "season_parts": season_parts, "cash": cash, "hash": new_hash, "num": num})
        else:
            messages.error(request, "You have insufficient coins!")
            return redirect("movies:index")

    if not movie.movie:
        return render(request, "movies/buy movie.html", {"movie": movie.all_seasons.all()})

    cash = calculate_pay(user=request.user)
    return render(request, "movies/confirm buy.html", {"cash": cash, "movie": movie, "hash": new_hash, "num": num})


def about_us(request):
    return render(request, "movies/about us.html")


def services(request):
    return render(request, "movies/services.html")


def privacy_policy(request):
    return render(request, "movies/privacy policy.html")


def confirm_buy(request, cash):
    user = request.user.details
    if request.user.is_authenticated:
        if int(user.coins) > int(cash):
            balance = int(user.coins) - int(cash)
            Sale(user=request.user, transaction_type="debit", price=cash, item_sold="Bought movies worth " + str(cash),
                 username=request.user.username, transaction_code=tc_calculate()).save()
            user.coins = balance
            user.save()
            messages.info(request, "Transaction successful.")
            return render(request, "movies/index.html")
        else:
            messages.info(request, "You have insufficient balance.")
            return redirect("movies:index")
    messages.info(request, "Please log in to access this service!")
    return redirect("movies:index")


def convert_points(request):
    user = request.user
    if user.is_authenticated:
        if user.details.coins > 0:
            coins = user.details.coins + user.details.points / 100
            user.details.coins = coins
            Sale(user=user, username=user.username, transaction_type="credit", transaction_code=tc_calculate(),
                 price=coins, item_sold="Converted " + str(user.details.points) + " to coins.").save()
            user.details.points = 0
            user.save()
            return redirect("movies:account")
        else:
            messages.info(request, "You do not have any points to convert.")
            return redirect("movies:index")
    messages.info(request, "Please log in to access this service!")
    return redirect("movies:index")


def app_messages(request):
    all_messages = Messages.objects.all().order_by("-created_at")
    return render(request, "movies/messages.html", {"messages": all_messages})


def message(request, message_id):
    user_message = Messages.objects.get(pk=message_id)
    time = user_message.created_at + timezone.timedelta(hours=3)
    return render(request, "movies/message.html", {"message": user_message, "time": time})


def add_movie(request):
    call_command('makemigrations')
    call_command('migrate')
    if request.method == "POST":
        movie_type = request.POST.get("type")
        name = request.POST.get("name")
        genre = request.POST.get("genre")
        rating = request.POST.get("rating")
        description = request.POST.get("description")
        trailer = request.POST.get("trailer")
        logo = request.POST.get("logo")
        movie_message = ""

        try:
            day = int(request.POST.get("day"))
            month = int(request.POST.get("month"))
            year = int(request.POST.get("year"))
        except ValueError:
            messages.error(request, "Date, month and year require numerical inputs.")
            return redirect("movies:add_movies")

        try:
            movie = Movie.objects.get(name=name)
            movie_message += "Movie with name '" + name + "' already exists."
            pass
        except Movie.DoesNotExist:
            movie = Movie()
            movie.name = name
            movie.genre = genre
            movie.rating = rating

            d = datetime.date(year, month, day)
            movie.date_of_release = d

            movie.description = description
            movie.trailer = trailer
            movie.year = year
            movie.logo = logo

            movie_message += "Successfully added '" + name + "'."
        except:
            messages.error(request, "some other error occurred")
            return redirect("movies:index")

        if movie_type == "movie":
            movie.movie = True
            movie.save()

        elif movie_type == "series":
            no_episodes = []
            movie.save()
            for num in range(1, 26, 1):
                season_no = "season-" + str(num)
                episodes_no = "episodes-" + str(num)

                if request.POST.get(episodes_no):

                    no_of_episodes = int(request.POST.get(episodes_no))

                    try:
                        season = Season.objects.get(unique_field=name + season_no)
                        movie_message += " Season " + str(num) + " of " + name + " already exist."
                        pass
                    except Season.DoesNotExist:
                        season = Season()

                        season.season_no = num
                        season.series_name = name
                        season.series = movie
                        season.unique_field = name + season_no
                        season.save()

                        movie.seasons = num
                        movie.save()

                        movie_message += " Successfully added season " + str(num) + "."

                    try:
                        Episode.objects.get(unique_field=name + season_no + "-episodes-" + str(no_of_episodes))
                        movie_message += " Episodes for the movie '" + name + "' season " + str(num) + " already exist."
                        pass
                    except Episode.DoesNotExist:
                        epi = Episode()
                        epi.series_name = name
                        epi.season = season
                        epi.season_no = num
                        epi.unique_field = name + season_no + "-episodes-" + str(no_of_episodes)
                        epi.no_of_episodes = no_of_episodes
                        epi.save()

                        movie_message += " Successfully added season " + str(num) + " episodes."

                else:
                    no_episodes.append(num)

        else:
            print("Unknown movie type of type |" + movie_type + "|")
            messages.info(request, "Unknown movie-type of type |" + movie_type + "|")
            return redirect("movies:index")
        messages.info(request, movie_message)
        return redirect("movies:add_movie")
    return render(request, "movies/add movie.html", {"range": range(1, 26, 1)})


def documentation(request):
    return render(request, "movies/documentation.html")


def faq(request):
    return render(request, "movies/faq.html")


def unavailable(request, **kwargs):
    return render(request, "movies/unavailable.html")


def comment(request):
    if not request.user.is_authenticated:
        messages.info(request, "Please log in to access this service!")
        return redirect("movies:index")

    if request.method == "POST":
        user_comment = request.POST.get("comment")
        Comment(comment=user_comment, user=request.user, username=request.user.username).save()
        messages.info(request, "Thank you for your feedback.")
        return render(request, "movies/index.html")
    return redirect("movies:index")


def save_comment(request, comment_id):
    user_comment = Comment.objects.get(pk=comment_id)
    user_comment.useful = True
    user_comment.save()
    messages.success(request, "You have successfully saved " + user_comment.username + "'s comment.")
    return render(request, "movies/index.html")


def delete_comment(request, comment_id):
    user_comment = Comment.objects.get(pk=comment_id)
    user_comment.delete()
    messages.success(request, "You have successfully deleted comment.")
    return render(request, "movies/index.html")
