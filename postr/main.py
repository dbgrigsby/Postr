# from typing import List

from kivy.app import App
from kivy.uix.checkbox import CheckBox
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.tabbedpanel import TabbedPanelHeader
from kivy.uix.textinput import TextInput


class TabbedPanelApp(App):
    @classmethod
    def build(cls) -> TabbedPanel:
        performance_layout = FloatLayout()
        posts_layout = FloatLayout()
        events_layout = FloatLayout()
        update_layout = FloatLayout()
        profile_layout = FloatLayout()

        def spinner() -> Spinner:
            spinner = Spinner(
                # default value
                text='Choose a site:',

                # available values
                values=(
                    'Discord', 'Facebook', 'Instagram', 'Reddit',
                    'Slack', 'Tumblr', 'Twitter', 'YouTube',
                ),

                size_hint=(.15, .1),
                pos=(15, 985),
            )

            def show_selected_value(spinner: Spinner, text: str) -> None:
                print('The spinner', spinner, 'have text', text)

            spinner.bind(text=show_selected_value)
            return spinner

        performance_layout.add_widget(spinner())
        performance_layout.add_widget(
            Label(
                text='Follower Count: ', font_size='20sp',
                pos=(300, 900), size_hint=(.15, .2),
                color=(0, 0, 0, 1),
            ),
        )
        performance_layout.add_widget(
            Label(
                text='Total Likes: ', font_size='20sp',
                pos=(300, 850), size_hint=(.15, .2),
                color=(0, 0, 0, 1),
            ),
        )

        posts_layout.add_widget(spinner())
        posts_layout.add_widget(
            Label(
                text='Scheduled Posts: ', font_size='20sp',
                pos=(315, 900), size_hint=(.15, .2),
                color=(0, 0, 0, 1),
            ),
        )

        events_layout.add_widget(spinner())
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
        events_layout.add_widget(
            CheckBox(
                pos=(450, 850), size_hint=(.15, .2),
            ),
        )
        events_layout.add_widget(
            Label(
                text='Key word', font_size='12sp',
                pos=(275, 800), size_hint=(.15, .2),
                color=(0, 0, 0, 1),
            ),
        )
        events_layout.add_widget(
            CheckBox(
                pos=(450, 800), size_hint=(.15, .2),
            ),
        )
        events_layout.add_widget(
            Label(
                text='Mention/Tag', font_size='12sp',
                pos=(275, 750), size_hint=(.15, .2),
                color=(0, 0, 0, 1),
            ),
        )
        events_layout.add_widget(
            CheckBox(
                pos=(450, 750), size_hint=(.15, .2),
            ),
        )
        events_layout.add_widget(
            Label(
                text='Like', font_size='12sp',
                pos=(275, 700), size_hint=(.15, .2),
                color=(0, 0, 0, 1),
            ),
        )
        events_layout.add_widget(
            CheckBox(
                pos=(450, 700), size_hint=(.15, .2),
            ),
        )
        events_layout.add_widget(
            Label(
                text='Comment', font_size='12sp',
                pos=(275, 650), size_hint=(.15, .2),
                color=(0, 0, 0, 1),
            ),
        )
        events_layout.add_widget(
            CheckBox(
                pos=(450, 650), size_hint=(.15, .2),
            ),
        )
        events_layout.add_widget(
            Label(
                text='Retweet/Repost/Share', font_size='12sp',
                pos=(275, 600), size_hint=(.15, .2),
                color=(0, 0, 0, 1),
            ),
        )
        events_layout.add_widget(
            CheckBox(
                pos=(450, 600), size_hint=(.15, .2),
            ),
        )

        update_layout.add_widget(spinner())
        update_layout.add_widget(
            Label(
                text='Search for: ', font_size='20sp',
                pos=(275, 950), size_hint=(.15, .2),
                color=(0, 0, 0, 1),
            ),
        )
        update_layout.add_widget(
            TextInput(
                multiline=False,
                pos=(300, 970), size_hint=(.15, .04),
            ),
        )
        update_layout.add_widget(
            Label(
                text='Replace with: ', font_size='20sp',
                pos=(575, 950), size_hint=(.15, .2),
                color=(0, 0, 0, 1),
            ),
        )
        update_layout.add_widget(
            TextInput(
                multiline=False,
                pos=(575, 970), size_hint=(.15, .04),
            ),
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
        profile_layout.add_widget(
            TextInput(
                multiline=False,
                pos=(300, 935), size_hint=(.1, .04),
            ),
        )
        profile_layout.add_widget(
            Label(
                text='New Password: ', font_size='12sp',
                pos=(50, 795), size_hint=(.15, .2),
                color=(0, 0, 0, 1),
            ),
        )
        profile_layout.add_widget(
            TextInput(
                multiline=False,
                pos=(300, 885), size_hint=(.1, .04),
            ),
        )
        profile_layout.add_widget(
            Label(
                text='Confirm New Password: ', font_size='12sp',
                pos=(50, 745), size_hint=(.15, .2),
                color=(0, 0, 0, 1),
            ),
        )
        profile_layout.add_widget(
            TextInput(
                multiline=False,
                pos=(300, 835), size_hint=(.1, .04),
            ),
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

    # def performance(platform_enum) -> List[int]:
    #     if platform_enum is platform_enum.REDDIT:
    #         from postr.reddit_postr import Reddit
    #         follower_count = Reddit.get_user_followers(),
    #         total_likes = Reddit.get_user_likes(),
    #     elif platform_enum is platform_enum.FACEBOOK:
    #         from postr.facebook_api import FacebookApi
    #         follower_count = FacebookApi.get_user_followers(),
    #         total_likes = FacebookApi.get_user_likes(),
    #     elif platform_enum is platform_enum.TUMBLR:
    #         follower_count = 0,
    #         total_likes = 0,
    #     elif platform_enum is platform_enum.INSTAGRAM:
    #         follower_count = 0,
    #         total_likes = 0,
    #     elif platform_enum is platform_enum.TWITTER:
    #         from postr.twitter_postr import Twitter
    #         follower_count = Twitter.get_user_followers(),
    #         total_likes = Twitter.get_user_likes(),
    #     elif platform_enum is platform_enum.YOUTUBE:
    #         follower_count = 0,
    #         total_likes = 0,
    #     elif platform_enum is platform_enum.PINTEREST:
    #         follower_count = 0,
    #         total_likes = 0,
    #     elif platform_enum is platform_enum.SLACK:
    #         follower_count = 0,
    #         total_likes = 0,
    #     elif platform_enum is platform_enum.DISCORD:
    #         follower_count = 0,
    #         total_likes = 0,
    #     elif platform_enum is platform_enum.YELP:
    #         follower_count = 0,
    #         total_likes = 0,
    #     elif platform_enum is platform_enum.LINKEDIN:
    #         follower_count = 0,
    #         total_likes = 0,
    #     else:
    #         follower_count = 0,
    #         total_likes = 0,
    #     return [follower_count, total_likes]


if __name__ == '__main__':
    TabbedPanelApp().run()
