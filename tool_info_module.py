```python
import benchexec.tools.template
import benchexec.util as util


class Tool(benchexec.tools.template.BaseTool):
    """
    Tool info module for CBMC tool.
    """

    REQUIRED_PATHS = ["cbmc"]

    def executable(self):
        return util.find_executable("cbmc")

    def name(self):
        return "CBMC"

    def version(self, executable):
        return self._version_from_tool(executable)

    def cmdline(self, executable, options, tasks, propertyfile, rlimits):
        return [executable] + options + tasks

```