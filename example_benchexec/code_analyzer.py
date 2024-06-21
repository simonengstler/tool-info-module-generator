# To run the analysis: static_analyzer --input <input_file>
# To get the version: static_analyzer --version

import benchexec.tools.template
import benchexec.util as util
import benchexec.result as result

class Tool(benchexec.tools.template.BaseTool2):
    """
    Tool info for StaticAnalyzer.
    """

    def executable(self, tool_locator):
        return tool_locator.find_executable("static_analyzer")

    def name(self):
        return "StaticAnalyzer"

    def version(self, executable):
        return self._version_from_tool(executable, arg="--version").strip()

    def cmdline(self, executable, options, task, rlimits):
        # Generate the command line call to execute the tool
        return [executable] + options + ["--input"] + list(task.input_files_or_identifier)

    def determine_result(self, run):
        # Analyze the output to determine the result
        output = run.output
        if "No errors found" in output:
            return result.RESULT_TRUE_PROP
        elif "Error:" in output:
            return result.RESULT_FALSE_REACH
        else:
            return result.RESULT_UNKNOWN

    def get_value_from_output(self, output, identifier):
        # Example implementation to extract specific values from the output
        for line in output:
            if identifier in line:
                return line.split(identifier)[-1].strip()
        return None

    def get_run_properties(self, output):
        # Example implementation to extract run properties from the output
        properties = {}
        properties["error_count"] = self.get_value_from_output(output, "Error count:")
        return properties
