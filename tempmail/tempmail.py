import requests

from bs4 import BeautifulSoup


BASE_URL = 'https://tempmail.net/en'
DEFAULT_PARSER = 'html.parser'


class TempMail:
    """TempMail class that provides interaction with tempmail.net
    """

    def get_address(self, cookies=None):
        """Get new email address

        :param cookies: cookies object to load mail account from
        :type cookies: RequestsCookieJar

        :return: email object
        :rtype: Email
        """
        response = requests.get(BASE_URL, cookies=cookies)
        content = response.content.decode('utf-8')

        bs = BeautifulSoup(content, DEFAULT_PARSER)
        selector = bs.find('input')

        return Email(selector['value'], response.cookies)


class Email:
    """Email class that represents email address from tempmail.net

    :param address: temporary email address
    :type address: str

    :param cookies: temporary email address cookies
    :type cookies: RequestsCookieJar
    """

    def __init__(self, address, cookies):
        self.address = address
        self.cookies = cookies

    def __str__(self):
        return self.address

    def _get_page_html(self, url):
        """Get page html content

        :param url: web-page url address
        :type url: str

        :return: web-page html code
        :rtype: str
        """
        response = requests.get(url, cookies=self.cookies)
        content = response.content.decode('utf-8')
        return content

    def get_messages(self):
        """Get inbox messages list

        :return: list of inbox messages represented in Message object
        :rtype: list
        """
        content = self._get_page_html(BASE_URL)

        bs = BeautifulSoup(content, DEFAULT_PARSER)
        mailer = bs.find('ul', {'class': 'mailler'})

        try:
            mailer.find('p', {'class': 'yukleniyor'}).text
            return []
        except Exception:
            pass

        mails = []
        for mail in mailer.find_all('li', {'class': 'mail'}):
            a = mail.find('a')

            id = a['href'][5:-1]
            sender = a.find('div', {'class': 'gonderen'}).text
            theme = a.find('div', {'class': 'baslik'}).text
            time = a.find('div', {'class': 'zaman'}).text
            avatar = a.find('div', {'class': 'avatar'}).find('img')['src']

            message = Message(self, id, sender, theme, time, avatar)
            mails.append(message)

        return mails


class Message:
    """Message object

    :param email: parent temporary email
    :type email: Email

    :param id: message id
    :type id: int

    :param sender: sender address
    :type sender: str

    :param theme: message theme
    :type theme: str

    :param time: message send time
    :type time: str

    :param avatar: sender avatar url
    :type avatar: str
    """

    def __init__(self, email, id, sender, theme, time, avatar):
        self.email = email
        self.id = id
        self.sender = sender
        self.theme = theme
        self.time = time
        self.avatar = avatar
        self.content = self.get_content()

    def __str__(self):
        return '<{}:{}> From: {} | Theme: {} | Time: {}'.format(
            self.__class__.__name__,
            self.id, self.sender, self.theme, self.time)

    def get_content(self, content_only=True):
        """Get message content

        :param content_only: return html content only w/o google javascript
        :type content_only: bool

        :return: message content markup
        :rtype: str
        """

        url = BASE_URL + '/api/icerik/?oturum={}&mail_no={}'
        url = url.format(self.email.cookies.get_dict()['oturum'], self.id)

        response = requests.get(url, cookies=self.email.cookies)
        content = response.content.decode('utf-8')

        if content_only:
            pos = content.find('cb=googleTranslateElementInit\"></script>')
            return content[pos + 40:].strip()
        else:
            return content
