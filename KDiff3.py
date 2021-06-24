import sublime, sublime_plugin
from tempfile import NamedTemporaryFile
from subprocess import Popen
from os import path

class Kdiff3FilesCommand(sublime_plugin.WindowCommand):
    def run(self, files):
        if len(files) < 2: 
            raise ArgumentsRequired("Must provide at least 2 files")
        Popen(["kdiff3"] + files[:3])

    def is_visible(self, files):
        return len(files) >= 2

class Kdiff3ViewsCommand(Kdiff3FilesCommand):
    def run(self, views):
        files = []
        for view in views:
            file_name = view.file_name()
            if view.is_dirty() or not file_name or not path.exists(file_name):
                with NamedTemporaryFile(mode='w+', encoding='utf-8', delete=False) as temp:
                    temp.write(view.substr(sublime.Region(0, view.size())))
                    files.append(temp.name)
            else:
                files.append(file_name)
        super().run(files)

class Kdiff3GroupsCommand(Kdiff3ViewsCommand):
    def run(self):
        views = [view for view in (self.window.active_view_in_group(i) for i in range(self.window.num_groups()))
                    if view is not None]
        if len(views) >=2:
            super().run(views)

    def is_visible(self):
        return self.window.num_groups() >= 2

class Kdiff3TabsCommand(Kdiff3ViewsCommand):
    def run(self):
        views = [sheet.view() for sheet in self.window.selected_sheets() if sheet.view()]
        if len(views) >=2:
            super().run(views)

    def is_visible(self):
        return len(self.window.selected_sheets()) >= 2
