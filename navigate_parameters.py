import sublime
import sublime_plugin


class GotoNextParameterCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        # print(f"Invoking GotoNextParameterCommand")
        new_sel = []
        for region in self.view.sel():
            new_region = self._find_next_parameter(region.b)
            new_region.a = new_region.b
            invalid_region = sublime.Region(-1, -1)

            if new_region == invalid_region:
                # print(f"Adding {region=}")
                new_sel.append(region)
            else:
                # print(f"Adding {new_region=}")
                new_sel.append(new_region)

        self.view.sel().clear()
        self.view.sel().add_all(new_sel)

    def _find_next_parameter(self, start_pt) -> sublime.Region:
        """Find next comma after `start_pt`.
        
        Returns:
            Region(-1, -1) if nothing found.
        """
        invalid_region = sublime.Region(-1, -1)
        patterns = (
            ", ?",
            "\\)",
            "\\}")

        regions = (
            self.view.find(pattern, start_pt, sublime.FindFlags.NONE)
            for pattern in patterns)
        regions = filter(lambda r: r != invalid_region, regions)

        try:
            closest_region = min(regions, key=lambda r: r.a)
            # print(f"Closest region: {closest_region=}")
            return closest_region
        except ValueError:
            # print("No valid region")
            return invalid_region

class GotoPrevParameterCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        # print(f"Invoking GotoPrevParameterCommand")
        new_sel = []
        for region in self.view.sel():
            new_region = self._find_prev_parameter(region.a - 2)
            new_region.a = new_region.b
            invalid_region = sublime.Region(-1, -1)

            if new_region == invalid_region:
                # print(f"Adding {region=}")
                new_sel.append(region)
            else:
                # print(f"Adding {new_region=}")
                new_sel.append(new_region)

        self.view.sel().clear()
        self.view.sel().add_all(new_sel)
        # self.view.insert(edit, 0, "Hello, World!")

    def _find_prev_parameter(self, start_pt) -> sublime.Region:
        """Find prev comma before `start_pt`.
        
        Returns:
            Region(-1, -1) if nothing found.
        """
        invalid_region = sublime.Region(-1, -1)
        patterns = (
            ", ?",
            "\\(",
            "\\{")

        regions = (
            self.view.find(pattern, start_pt, sublime.FindFlags.REVERSE)
            for pattern in patterns)
        regions = filter(lambda r: r != invalid_region, regions)

        try:
            closest_region = max(regions, key=lambda r: r.b)
            # print(f"Closest region: {closest_region=}")
            return closest_region
        except ValueError:
            # print("No valid region")
            return invalid_region
