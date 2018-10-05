from kivy.app import App
from kivy.uix.spinner import Spinner
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.tabbedpanel import TabbedPanelHeader
from kivy.uix.textinput import TextInput


class TabbedPanelApp(App):
    def build(self):
        spinner = Spinner(
            # default value
            text='Choose a site:',

            # available values
            values=(
                "Discord", "Facebook", "Instagram", "Reddit",
                "Slack", "Tumblr", "Twitter", "YouTube",
            ),

            size_hint=(None, None),
            size=(200, 44),
            pos_hint={'center_x': -10, 'center_y': -10},
        )

        def show_selected_value(spinner, text):
            print('The spinner', spinner, 'have text', text)

        spinner.bind(text=show_selected_value)

        updatePassword = TextInput(text='Update Password')
        updatePassword.multiline = False

        tb_panel = TabbedPanel()
        tb_panel.do_default_tab = False

        # Create Performance tab
        performance_tab = TabbedPanelHeader(text='Performance')
        performance_tab.content = spinner
        tb_panel.add_widget(performance_tab)

        # Create Posts tab
        posts_tab = TabbedPanelHeader(text='Posts')
        posts_tab.content = spinner
        tb_panel.add_widget(posts_tab)

        # Create Events tab
        events_tab = TabbedPanelHeader(text='Events')
        events_tab.content = spinner
        tb_panel.add_widget(events_tab)

        # Create Update tab
        update_tab = TabbedPanelHeader(text='Update')
        update_tab.content = spinner
        tb_panel.add_widget(update_tab)

        # Create Profile tab
        profile_tab = TabbedPanelHeader(text='Profile')
        profile_tab.content = updatePassword
        tb_panel.add_widget(profile_tab)

        return tb_panel


if __name__ == '__main__':
    TabbedPanelApp().run()
