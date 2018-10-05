from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.tabbedpanel import TabbedPanelHeader


class TabbedPanelApp(App):
    def build(self):
        performance_layout = FloatLayout()
        posts_layout = FloatLayout()
        events_layout = FloatLayout()
        update_layout = FloatLayout()
        profile_layout = FloatLayout()

        def spinner():
            spinner = Spinner(
                # default value
                text='Choose a site:',

                # available values
                values=(
                    "Discord", "Facebook", "Instagram", "Reddit",
                    "Slack", "Tumblr", "Twitter", "YouTube",
                ),

                size_hint=(.15, .1),
                pos=(15, 985),
            )

            def show_selected_value(spinner, text):
                print('The spinner', spinner, 'have text', text)

            spinner.bind(text=show_selected_value)
            return spinner

        performance_layout.add_widget(spinner())
        posts_layout.add_widget(spinner())
        events_layout.add_widget(spinner())
        update_layout.add_widget(spinner())
        profile_layout.add_widget(
            Label(
                text="Username: ", font_size='20sp',
                pos=(50, 970), size_hint=(.15, .2),
            ),
        )

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
