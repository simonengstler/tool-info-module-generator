def get_cli_command_from_file():
    tool = "cbmc_1"
    #tool = "goblint_1"
    #tool = "javac_1"
    #tool = "timmy"

    with open(f'template/cmd/{tool}.txt', 'r') as f:
        return tool, f.read()

def get_cli_command_from_user():
    tool = input("Enter the name of the tool for which you want to generate a tool_info_module file:\n")
    cli_command = input("Enter an exemplary CLI command for which you want to generate a tool_info_module file:\n")
    return tool, cli_command