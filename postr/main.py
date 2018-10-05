from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.spinner import Spinner
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.tabbedpanel import TabbedPanelHeader
from kivy.uix.textinput import TextInput


class TabbedPanelApp(App):
    def build(self):
        performance_layout = FloatLayout(size=(300, 300))
        posts_layout = FloatLayout()
        events_layout = FloatLayout()
        update_layout = FloatLayout()
        profile_layout = FloatLayout()

        update_password = TextInput(text='Update Password')
        update_password.multiline = False
        update_password.width = 100
        update_password.height = 44

        def spinner():
            spinner = Spinner(
                # default value
                text='Choose a site:',

                # available values
                values=(
                    "Discord", "Facebook", "Instagram", "Reddit",
                    "Slack", "Tumblr", "Twitter", "YouTube",
                ),

                size_hint=(.5, .25),
                size=(200, 44),
                pos_hint={'center_x': -10, 'center_y': -10},
                pos=(100, 100),
            )

            def show_selected_value(spinner, text):
                print('The spinner', spinner, 'have text', text)

            spinner.bind(text=show_selected_value)
            return spinner

        performance_layout.add_widget(spinner())
        posts_layout.add_widget(spinner())
        events_layout.add_widget(spinner())
        update_layout.add_widget(spinner())
        profile_layout.add_widget(update_password)

        tb_panel = TabbedPanel()
        tb_panel.do_default_tab = False

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


if __name__ == '__main__':
    TabbedPanelApp().run()
