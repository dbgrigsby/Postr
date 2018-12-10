from typing import List, Dict

import datetime

from dateutil import parser

from kivy.app import App
# from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.tabbedpanel import TabbedPanelHeader
from kivy.uix.textinput import TextInput

from postr import config
from postr.reddit_postr import Reddit
from postr.facebook_api import FacebookApi
from postr.twitter_postr import Twitter
from postr.youtube_postr import Youtube
from postr.tumblr_api import TumblrApi
from postr.instagram_postr import Instagram
from postr.slack_api import SlackApi
from postr.schedule.writer import Writer


class TabbedPanelApp(App):
    @classmethod
    def build(cls) -> TabbedPanel:
        performance_layout = FloatLayout()
        posts_layout = FloatLayout()
        events_layout = FloatLayout()
        update_layout = FloatLayout()
        profile_layout = FloatLayout()

        def spinner() -> Spinner:
            spin = Spinner(
                # default value
                text='Choose a site:',
                # available values
                values=(
                    'Discord', 'Facebook', 'Instagram', 'Reddit',
                    'Slack', 'Tumblr', 'Twitter', 'YouTube',
                ),

                size_hint=(.15, .1),
                pos=(15, 985),
                background_color=(0.094, 0.803, 0.803),
            )

            def show_selected_value(spnr: Spinner, text: str) -> None:
                print('The spinner', spnr, 'have text', text)

            spin.bind(text=show_selected_value)
            return spin

        performance_spinner = spinner()
        # performance_button = Button(
        #     text='Show Stats',
        #     font_size=14,
        #     color=(0.094, 0.803, 0.803),
        # )
        # performance_button.bind(on_press=callback)
        performance_layout.add_widget(performance_spinner)
        performance_layout.add_widget(
            Label(
                text='Follower Count: ', font_size='20sp',
                pos=(300, 850), size_hint=(.15, .2),
                color=(0, 0, 0, 1),
            ),
        )
        performance_layout.add_widget(
            Label(
                text='Total Likes: ', font_size='20sp',
                pos=(300, 800), size_hint=(.15, .2),
                color=(0, 0, 0, 1),
            ),
        )
        performance_stats = cls.performance(performance_spinner.values)
        performance_layout.add_widget(
            Label(
                text=str(performance_stats[0]), font_size='20sp',
                pos=(500, 850), size_hint=(.15, .2),
                color=(0, 0, 0, 1),
            ),
        )
        performance_layout.add_widget(
            Label(
                text=str(performance_stats[1]), font_size='20sp',
                pos=(500, 800), size_hint=(.15, .2),
                color=(0, 0, 0, 1),
            ),
        )

        post_spinner = spinner()
        # post_button = Button(
        #     text='Submit',
        #     font_size=14,
        #     color=(0.094, 0.803, 0.803),
        # )
        # # post_button.bind(on_press=callback)
        posts_layout.add_widget(post_spinner)
        posts_layout.add_widget(
            Label(
                text='Scheduled Posts: ', font_size='20sp',
                pos=(375, 675), size_hint=(.15, .2),
                color=(0, 0, 0, 1),
            ),
        )
        post_types = Spinner(
            text='Post type',
            italic=True,
            values=(
                'Text', 'Image', 'Video', 'Link', 'Announcement',
            ),
            size_hint=(.15, .1),
            pos=(315, 985),
        )
        post_timing = Spinner(
            text='Choose a time:',
            italic=True,
            values=(
                'Immediately', 'Schedule for',
            ),

            size_hint=(.15, .1),
            pos=(615, 985),
        )
        posts_layout.add_widget(post_types)
        posts_layout.add_widget(post_timing)
        month = Spinner(
            text='Month',
            italic=True,
            values=(
                'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
                'November', 'December',
            ),
            size_hint=(.15, .1),
            pos=(915, 985),
        )
        day = Spinner(
            text='Day',
            italic=True,
            values=(
                '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19',
                '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31',
            ),
            size_hint=(.15, .1),
            pos=(1215, 985),
        )
        year = Spinner(
            text='Year',
            italic=True,
            values=(
                '2018', '2019', '2020',
            ),
            size_hint=(.15, .1),
            pos=(315, 850),
        )
        hour = Spinner(
            text='Hour',
            italic=True,
            values=(
                '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19',
                '20', '21', '22', '23',
            ),
            size_hint=(.15, .1),
            pos=(615, 850),
        )
        minute = Spinner(
            text='Minute',
            italic=True,
            values=(
                '00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16',
                '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33',
                '34', '35', '36', '37', '38', '39', '40', '41', '42', '43', '44', '45', '46', '47', '48', '49', '50',
                '51', '52', '53', '54', '55', '56', '57', '58', '59',
            ),
            size_hint=(.15, .1),
            pos=(915, 850),
        )
        posts_layout.add_widget(month)
        posts_layout.add_widget(day)
        posts_layout.add_widget(year)
        posts_layout.add_widget(hour)
        posts_layout.add_widget(minute)

        events_spinner = spinner()
        # events_button = Button(
        #     text='Submit',
        #     font_size=14,
        #     color=(0.094, 0.803, 0.803),
        # )
        # events_button.bind(on_press=callback)
        events_layout.add_widget(events_spinner)
        events_layout.add_widget(
            Label(
                text='React to: ', font_size='20sp',
                pos=(275, 900), size_hint=(.15, .2),
                color=(0, 0, 0, 1),
            ),
        )
        events_layout.add_widget(
            Label(
                text='Hastag(s)', font_size='12sp',
                pos=(275, 850), size_hint=(.15, .2),
                color=(0, 0, 0, 1),
            ),
        )
        hashtag_checkbox = CheckBox(pos=(450, 850), size_hint=(.15, .2), )
        events_layout.add_widget(hashtag_checkbox)
        events_layout.add_widget(
            Label(
                text='Key word', font_size='12sp',
                pos=(275, 800), size_hint=(.15, .2),
                color=(0, 0, 0, 1),
            ),
        )
        keyword_checkbox = CheckBox(
            pos=(450, 800), size_hint=(.15, .2),
        )
        events_layout.add_widget(
            keyword_checkbox,
        )
        events_layout.add_widget(
            Label(
                text='Mention/Tag', font_size='12sp',
                pos=(275, 750), size_hint=(.15, .2),
                color=(0, 0, 0, 1),
            ),
        )
        mention_tag_checkbox = CheckBox(
            pos=(450, 750), size_hint=(.15, .2),
        )
        events_layout.add_widget(
            mention_tag_checkbox,
        )
        events_layout.add_widget(
            Label(
                text='Like', font_size='12sp',
                pos=(275, 700), size_hint=(.15, .2),
                color=(0, 0, 0, 1),
            ),
        )
        like_checkbox = CheckBox(
            pos=(450, 700), size_hint=(.15, .2),
        )
        events_layout.add_widget(
            like_checkbox,
        )
        events_layout.add_widget(
            Label(
                text='Comment', font_size='12sp',
                pos=(275, 650), size_hint=(.15, .2),
                color=(0, 0, 0, 1),
            ),
        )
        comment_checkbox = CheckBox(
            pos=(450, 650), size_hint=(.15, .2),
        )
        events_layout.add_widget(
            comment_checkbox,
        )
        events_layout.add_widget(
            Label(
                text='Retweet/Repost/Share', font_size='12sp',
                pos=(275, 600), size_hint=(.15, .2),
                color=(0, 0, 0, 1),
            ),
        )
        retweet_repost_share_checkbox = CheckBox(
            pos=(450, 600), size_hint=(.15, .2),
        )
        events_layout.add_widget(
            retweet_repost_share_checkbox,
        )

        update_spinner = spinner()
        # update_button = Button(
        #     text='Update',
        #     font_size=14,
        #     color=(0.094, 0.803, 0.803),
        # )
        # update_button.bind(on_press=callback)
        update_layout.add_widget(update_spinner)
        update_layout.add_widget(
            Label(
                text='Search for: ', font_size='20sp',
                pos=(275, 950), size_hint=(.15, .2),
                color=(0, 0, 0, 1),
            ),
        )
        search_input = TextInput(
            multiline=False,
            pos=(300, 970), size_hint=(.15, .04),
        )
        update_layout.add_widget(
            search_input,
        )
        update_layout.add_widget(
            Label(
                text='Replace with: ', font_size='20sp',
                pos=(575, 950), size_hint=(.15, .2),
                color=(0, 0, 0, 1),
            ),
        )
        replace_input = TextInput(
            multiline=False,
            pos=(575, 970), size_hint=(.15, .04),
        )
        update_layout.add_widget(
            replace_input,
        )

        profile_layout.add_widget(
            Label(
                text='Username: ', font_size='20sp',
                pos=(45, 970), size_hint=(.15, .2),
                color=(0, 0, 0, 1),
            ),
        )
        profile_layout.add_widget(
            Label(
                text='TEMP USERNAME', font_size='15sp',
                pos=(275, 967), size_hint=(.15, .2),
                color=(0, 0, 0, 1),
            ),
        )
        profile_layout.add_widget(
            Label(
                text='Change Password: ', font_size='20sp',
                pos=(55, 900), size_hint=(.15, .2),
                color=(0, 0, 0, 1),
            ),
        )
        profile_layout.add_widget(
            Label(
                text='Old Password: ', font_size='12sp',
                pos=(50, 850), size_hint=(.15, .2),
                color=(0, 0, 0, 1),
            ),
        )
        old_password_input = TextInput(
            multiline=False,
            pos=(300, 935), size_hint=(.1, .04),
        )
        profile_layout.add_widget(
            old_password_input,
        )
        profile_layout.add_widget(
            Label(
                text='New Password: ', font_size='12sp',
                pos=(50, 795), size_hint=(.15, .2),
                color=(0, 0, 0, 1),
            ),
        )
        new_password_input = TextInput(
            multiline=False,
            pos=(300, 885), size_hint=(.1, .04),
        )
        profile_layout.add_widget(
            new_password_input,
        )
        profile_layout.add_widget(
            Label(
                text='Confirm New Password: ', font_size='12sp',
                pos=(50, 745), size_hint=(.15, .2),
                color=(0, 0, 0, 1),
            ),
        )
        confirm_new_password_input = TextInput(
            multiline=False,
            pos=(300, 835), size_hint=(.1, .04),
        )
        profile_layout.add_widget(
            confirm_new_password_input,
        )

        tb_panel = TabbedPanel()
        tb_panel.do_default_tab = False
        tb_panel.background_color = (1, 1, 1, 1)
        tb_panel.border = [0, 0, 0, 0]
        tb_panel.background_image = 'path/to/background/image'

        # Create Performance tab
        performance_tab = TabbedPanelHeader(text='Performance')
        performance_tab.content = performance_layout
        tb_panel.add_widget(performance_tab)

        # Create Posts tab
        posts_tab = TabbedPanelHeader(text='Posts')
        posts_tab.content = posts_layout
        tb_panel.add_widget(posts_tab)

        # Create Events tab
        events_tab = TabbedPanelHeader(text='Events')
        events_tab.content = events_layout
        tb_panel.add_widget(events_tab)

        # Create Update tab
        update_tab = TabbedPanelHeader(text='Update')
        update_tab.content = update_layout
        tb_panel.add_widget(update_tab)

        # Create Profile tab
        profile_tab = TabbedPanelHeader(text='Profile')
        profile_tab.content = profile_layout
        tb_panel.add_widget(profile_tab)

        return tb_panel

    @staticmethod
    def performance(platform: str) -> List[int]:
        if platform == 'Reddit':
            reddit = Reddit()
            follower_count = len(reddit.get_user_followers(''))
            total_likes = reddit.get_user_likes()
        elif platform == 'Facebook':
            facebook = FacebookApi()
            follower_count = len(facebook.get_user_followers(''))
            total_likes = facebook.get_user_likes()
        elif platform == 'Tumblr':
            tumblr = TumblrApi()
            follower_count = len(tumblr.get_user_followers(''))
            total_likes = tumblr.get_user_likes()
        elif platform == 'Instagram':
            instagram = Instagram()
            follower_count = len(instagram.get_user_followers(''))
            total_likes = instagram.get_user_likes()
        elif platform == 'Twitter':
            twitter = Twitter()
            follower_count = len(twitter.get_user_followers(''))
            total_likes = twitter.get_user_likes()
        elif platform == 'Youtube':
            youtube = Youtube()
            follower_count = len(youtube.get_user_followers(''))
            total_likes = youtube.get_user_likes()
        elif platform == 'Slack':
            slack = SlackApi()
            follower_count = len(slack.get_user_followers(''))
            total_likes = slack.get_user_likes()
        elif platform == 'Discord':
            follower_count = 0
            total_likes = 0
        else:
            follower_count = 0
            total_likes = 0
        stats = [follower_count, total_likes]
        return stats

    @staticmethod
    def immediate_post(platform: str, post_type: str, text: str, media: str) -> None:
        # dict = {
        #     'Comment': 'bahgb comment idiot',
        #     'MediaPath': 'testpath123',
        #     'OptionalText': '',
        #     'Platforms': 'reddit,discord',
        #     'Action': 'post_text'
        # }

        if platform == 'Reddit':
            reddit = Reddit()
            if post_type == 'Text':
                reddit.post_text(text)
            elif post_type == 'Image':
                reddit.post_photo(media, text)
            elif post_type == 'Video':
                reddit.post_video(media, text)
            elif post_type == 'Link':
                reddit.post_link(media, text)
        elif platform == 'Facebook':
            facebook = FacebookApi()
            if post_type == 'Text':
                facebook.post_text(text)
            elif post_type == 'Image':
                facebook.post_photo(media, text)
            elif post_type == 'Video':
                facebook.post_video(media, text)
        elif platform == 'Tumblr':
            tumblr = TumblrApi()
            if post_type == 'Text':
                tumblr.post_text(text)
            elif post_type == 'Image':
                tumblr.post_photo(media, text)
            elif post_type == 'Video':
                tumblr.post_video(media, text)
        elif platform == 'Instagram':
            instagram = Instagram()
            if post_type == 'Text':
                instagram.post_text(text)
            elif post_type == 'Image':
                instagram.post_photo(media, text)
            elif post_type == 'Video':
                instagram.post_video(media, text)
        elif platform == 'Twitter':
            twitter = Twitter()
            if post_type == 'Text':
                twitter.post_text(text)
            elif post_type == 'Image':
                twitter.post_photo(media, text)
            elif post_type == 'Video':
                twitter.post_video(media, text)
        elif platform == 'Youtube':
            youtube = Youtube()
            if post_type == 'Text':
                youtube.post_text(text)
            elif post_type == 'Image':
                youtube.post_photo(media, text)
            elif post_type == 'Video':
                youtube.post_video(media, text)
        elif platform == 'Slack':
            slack = SlackApi()
            if post_type == 'Text':
                slack.post_text(text)
            elif post_type == 'Image':
                slack.post_photo(media, text)
            elif post_type == 'Video':
                slack.post_video(media, text)

    @staticmethod
    def scheduled_post(plat: str, pst: str, text: str, mda: str, mnt: int, day: int, yr: int, hr: int, mn: int) -> None:
        writer = Writer()
        job_id = writer.create_job('', mda, text, plat, pst)
        date = datetime.datetime(mn, hr, 0, yr, mnt, day)
        time = int(date.timestamp() * 1000)
        writer.create_custom_job(time, job_id)

    # def callback(instance):
    #     print('The button <%s> is being pressed' % instance.text)

    # def update(self, platform, search, replace):
    #     if platform == 'Reddit':
    #
    #     elif platform == 'Facebook':
    #
    #     elif platform == 'Tumblr':
    #
    #     elif platform == 'Instagram':
    #
    #     elif platform == 'Twitter':
    #
    #     elif platform == 'Youtube':
    #
    #     elif platform == 'Slack':
    #
    #     elif platform == 'Discord':
    #
    #     else:

    # def update_profile(self, new_password):

    @staticmethod
    def get_missing_keys() -> Dict:
        # Discord
        discord = []
        if config.get_api_key('Discord', 'client_secret') is None \
                or config.get_api_key('Discord', 'client_secret') == '':
            discord.append('client_secret')
        if config.get_api_key('Discord', 'bot_token') is None or config.get_api_key('Discord', 'bot_token') == '':
            discord.append('bot_token')
        if config.get_api_key('Discord', 'default_channel') is None \
                or config.get_api_key('Discord', 'default_channel') == '':
            discord.append('default_channel')
        # Twitter
        twitter = []
        if config.get_api_key('Twitter', 'ACCESS_TOKEN') is None or config.get_api_key('Twitter', 'ACCESS_TOKEN') == '':
            twitter.append('ACCESS_TOKEN')
        if config.get_api_key('Twitter', 'ACCESS_TOKEN_SECRET') is None \
                or config.get_api_key('Twitter', 'ACCESS_TOKEN_SECRET') == '':
            twitter.append('ACCESS_TOKEN_SECRET')
        if config.get_api_key('Twitter', 'CONSUMER_KEY') is None or config.get_api_key('Twitter', 'CONSUMER_KEY') == '':
            twitter.append('CONSUMER_KEY')
        if config.get_api_key('Twitter', 'CONSUMER_SECRET') is None \
                or config.get_api_key('Twitter', 'CONSUMER_SECRET') == '':
            twitter.append('CONSUMER_SECRET')
        # Reddit
        reddit = []
        if config.get_api_key('Reddit', 'subreddit') is None or config.get_api_key('Reddit', 'subreddit') == '':
            reddit.append('subreddit')
        if config.get_api_key('Reddit', 'client_id') is None or config.get_api_key('Reddit', 'client_id') == '':
            reddit.append('client_id')
        if config.get_api_key('Reddit', 'refresh_token') is None or config.get_api_key('Reddit', 'refresh_token') == '':
            reddit.append('refresh_token')
        # Slack
        slack = []
        if config.get_api_key('Slack', 'default_channel') is None \
                or config.get_api_key('Slack', 'default_channel') == '':
            slack.append('default_channel')
        if config.get_api_key('Slack', 'API_TOKEN') is None or config.get_api_key('Slack', 'API_TOKEN') == '':
            slack.append('API_TOKEN')
        # Instagram
        instagram = []
        if config.get_api_key('Instagram', 'USERNAME') is None or config.get_api_key('Instagram', 'USERNAME') == '':
            instagram.append('USERNAME')
        if config.get_api_key('Instagram', 'PASSWORD') is None or config.get_api_key('Instagram', 'PASSWORD') == '':
            instagram.append('PASSWORD')
        if config.get_api_key('Instagram', 'PRE_PROFILE_JSON_URL') is None \
                or config.get_api_key('Instagram', 'PRE_PROFILE_JSON_URL') == '':
            instagram.append('PRE_PROFILE_JSON_URL')
        if config.get_api_key('Instagram', 'RANK_TOKEN') is None or config.get_api_key('Instagram', 'RANK_TOKEN') == '':
            instagram.append('RANK_TOKEN')
        if config.get_api_key('Instagram', 'POST_PROFILE_JSON_URL') is None \
                or config.get_api_key('Instagram', 'POST_PROFILE_JSON_URL') == '':
            instagram.append('POST_PROFILE_JSON_URL')
        # YouTube
        youtube = []
        if config.get_api_key('YouTube', 'client_id') is None or config.get_api_key('YouTube', 'client_id') == '':
            youtube.append('client_id')
        if config.get_api_key('YouTube', 'project_id') is None or config.get_api_key('YouTube', 'project_id') == '':
            youtube.append('project_id')
        if config.get_api_key('YouTube', 'auth_uri') is None or config.get_api_key('YouTube', 'auth_uri') == '':
            youtube.append('auth_uri')
        if config.get_api_key('YouTube', 'token_uri') is None or config.get_api_key('YouTube', 'token_uri') == '':
            youtube.append('token_uri')
        if config.get_api_key('YouTube', 'auth_provider_x509_cert_url') is None \
                or config.get_api_key('YouTube', 'auth_provider_x509_cert_url') == '':
            youtube.append('auth_provider_x509_cert_url')
        if config.get_api_key('YouTube', 'client_secret') is None \
                or config.get_api_key('YouTube', 'client_secret') == '':
            youtube.append('client_secret')
        if config.get_api_key('YouTube', 'redirect_uri') is None or config.get_api_key('YouTube', 'redirect_uri') == '':
            youtube.append('redirect_uri')

        missing_keys = {}
        if discord:
            missing_keys.update({'Discord': discord})
        if twitter:
            missing_keys.update({'Twitter': twitter})
        if reddit:
            missing_keys.update({'Reddit': reddit})
        if slack:
            missing_keys.update({'Slack': slack})
        if instagram:
            missing_keys.update({'Instagram': instagram})
        if youtube:
            missing_keys.update({'YouTube': youtube})

        return missing_keys

    @staticmethod
    def str_to_seconds_post_epoch(desired_time: str) -> float:
        time = parser.parse(desired_time)
        return time.timestamp()


if __name__ == '__main__':
    TabbedPanelApp().run()
