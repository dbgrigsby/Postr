from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.tabbedpanel import TabbedPanelHeader


class TabbedPanelApp(App):
    def build(self):
        tb_panel = TabbedPanel()
        tb_panel.do_default_tab = False

        # Create Performance tab
        performance_tab = TabbedPanelHeader(text='Performance')
        performance_tab.content = Label(text='Performance graphs go here')
        tb_panel.add_widget(performance_tab)

        # Create Posts tab
        posts_tab = TabbedPanelHeader(text='Posts')
        posts_tab.content = Label(text='Posts scheduling is here')
        tb_panel.add_widget(posts_tab)

        # Create Events tab
        events_tab = TabbedPanelHeader(text='Events')
        events_tab.content = Label(text='Event responses are here')
        tb_panel.add_widget(events_tab)

        # Create Update tab
        update_tab = TabbedPanelHeader(text='Update')
        update_tab.content = Label(text='Update information across accounts')
        tb_panel.add_widget(update_tab)

        # Create Profile tab
        profile_tab = TabbedPanelHeader(text='Profile')
        profile_tab.content = Label(
            text='The user can update their profile here!',
        )
        tb_panel.add_widget(profile_tab)

        return tb_panel


if __name__ == '__main__':
    TabbedPanelApp().run()
