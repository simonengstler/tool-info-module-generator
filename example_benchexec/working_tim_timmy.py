from benchexec.tools.template import BaseTool2
import benchexec.tools.template
import benchexec.result as result
from benchexec.tools.sv_benchmarks_util import get_data_model_from_task, ILP32, LP64


class Tool(BaseTool2):
    def executable(self, tool_locator):
        return tool_locator.find_executable("timmy")

    def version(self, executable):
        return self._version_from_tool(executable, "--version")

    def name(self):
        return "timmy"

    def cmdline(self, executable, options, task, rlimits):
        data_model_param = get_data_model_from_task(task, {ILP32: "--datenmodell=ilp32", LP64: "--datenmodell=lp64"})

        if data_model_param and data_model_param not in options:
            options += [data_model_param]

        return [executable] + options + [f"--eigenschaftsfile={task.property_file}", task.single_input_file]

    def determine_result(self, run):
        status = result.RESULT_UNKNOWN

        if run.was_timeout:
            status = result.RESULT_TIMEOUT
        elif not run.exit_code:
            status = result.RESULT_TRUE_PROP
        else:
            status = result.RESULT_FALSE_PROP

        return status
