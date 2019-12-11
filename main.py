import argparse

def detect_include_section(filename: str):
    with open(filename, 'r+') as file:
        line: str = file.readline()
        begin_section_line = 0
        end_section_line = 0
        i = 0

        while line:
            i += 1

            if line == "__lua__\r\n" or line == "__lua__\n" or line == "__lua__\r":
                begin_section_line = i + 1
            elif line == "__gfx__\r\n" or line == "__gfx__\n" or line == "__gfx__\r":
                end_section_line = i - 1

                break

            line = file.readline()

    return begin_section_line, end_section_line


def clean_section_in_file(filename: str):
    begin_content: str = ""
    end_content: str = ""

    begin, end = detect_include_section(filename)

    with open(filename, 'r+') as file:
        line: str = file.readline()
        i = 0

        while line:
            i += 1

            if i < begin:
                begin_content += line
            elif i > end:
                end_content += line

            line = file.readline()

    return begin_content, end_content


def get_file_content(filename: str):
    content: str = ""

    with open(filename, 'r+') as file:
        line: str = file.readline()

        while line:
            content += line
            line = file.readline()

    return content


def get_require_list_in_file(filename: str):
    require_list = []

    with open(filename, 'r+') as file:
        line: str = file.readline()

        while line:
            line = file.readline()

            if line.find("require(\"") != -1:
                require_list.append("{}.lua".format(line.replace("require(\"", "").replace("\")", "").replace("\n", "")
                                                    .replace("\r", "").replace("\r\n", "")))

    return require_list


def get_require_content_list(filename_list: []):
    require_content_list = []

    for filename in filename_list:
        content = get_file_content(filename)

        require_content_list.append(content)

    return require_content_list


def get_filecontent_without_require(filename: str):
    content: str = ""

    with open(filename, 'r') as file:
        line: str = file.readline()

        while line:
            if line.find("require(\"") == -1:
                content += line

            line = file.readline()

    return content


def main(game_filename, main_filename):
    begin_content, end_content = clean_section_in_file(game_filename)
    require_list = get_require_list_in_file(main_filename)
    require_content_list = get_require_content_list(require_list)

    lua_content = ""

    for i in range(0, len(require_list)):
        lua_content += "=========== {} ===========\n\n".format(require_list[i])
        lua_content += require_content_list[i]
        lua_content += "\n\n"

    main_content = get_filecontent_without_require(main_filename)

    if main_content != "":
        main_content = "=========== main.lua ===========\n\n" + main_content
        main_content += "\n"

    with open(game_filename, 'w') as file:
        file.write(begin_content)
        file.write(main_content)
        file.write(lua_content)
        file.write(end_content)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("pico8_file")

    args = parser.parse_args()

    main(args.pico8_file, "main.lua")
