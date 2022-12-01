import re


def add_header_xml(html):
    xmlText = """<?xml version="1.0" encoding="UTF-8" ?>\n""" + html
    return xmlText


def get_tag_text(text):
    pat = r"<(.*?)>"
    ret = re.search(pat, text)
    if ret is None:
        return None
    ret = ret.group(0)
    ret = ret[1:len(ret) - 1]
    return ret


def get_between_tags(text):
    pat = r"(.*?)<"
    ret = re.match(pat, text)
    ret = ret.group(0)
    ret = ret[:len(ret) - 1]
    return ret


def replace_w_spaces(text):
    if ' ' in text:
        x = text.split('"')
        x[1] = x[1].replace(' ', 'wEoN')
        united = ''
        for i in x:
            if i == x[-1]:
                return united
            united += i + '"'
        return united
    else:
        return text


def replace_weon(text):
    x = text.replace('wEoN', ' ')
    return x


def xml_to_yaml(xmlinput: str):
    yamlText = "---\n"
    indentations = 0
    temp = xmlinput.removeprefix("""<?xml version="1.0" encoding="UTF-8" ?>""")
    while temp is not None:
        between = get_tag_text(temp)
        if between is None:
            yamlText += "\n..."
            yamlText = replace_weon(yamlText)
            return yamlText
        to_remove = "<" + between + ">"
        end = temp.find(to_remove) + len(to_remove)
        to_remove = temp[0:end]
        temp = temp.removeprefix(to_remove)
        if '"' in between:
            between = replace_w_spaces(between)
        between = between.split(" ")
        comparador = []
        for i in between:
            if "/" in between[0]:
                indentations -= 1
            elif i == between[0]:
                yamlText += (indentations * " ") + '- ' + i + ":\n"
            elif len(between) > 1:
                if comparador != between:
                    indentations += 1
                i = i.split("=")
                yamlText += (indentations * " ") + i[0] + ": " + i[1] + "\n"
                comparador = between
            if (i == between[-1] or len(between) == 1) and not "/" in between[0]:
                indentations += 1
        temp = temp.lstrip()
        if temp is not None and temp != '':
            if temp[0] != '<':
                data = get_between_tags(temp)
                to_remove = data
                temp = temp.removeprefix(to_remove)
                data = data.lstrip()
                if data != '':
                    yamlText += (indentations * " ") + '"' + data + '"' + "\n"

    yamlText += "\n..."
    yamlText = replace_weon(yamlText)
    return yamlText


def second(text):
    x = add_header_xml(text)
    y = xml_to_yaml(x)
    outputFile = open("2.yml", "w")
    outputFile.write(y)
