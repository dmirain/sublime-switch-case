# -*- coding: utf-8 -*-

import sublime
import sublime_plugin

import re

class UnknownCase(Exception):
    pass

def switch_case(text):
    '''
        Если текст состоит из маленьких букв, цифр и _, то это underscore.
            Underscore переключаем в camel_f.
        Если текст состоит из букв, цифр и начинается на маленькую букву,
            то это camel_f. Сamel_f переключаем в camel_c.
        Если текст состоит из букв, цифр и начинается на большую букву,
            то это camel_c. Сamel_c переключаем в underscore.
    '''
    if re.match(r"^[a-z][A-Za-z0-9]+$", text):
        return switch_case_to_camel_c_case(text)
    elif re.match(r"^[A-Z][A-Za-z0-9]+$", text):
        return switch_case_to_underscore_case(text)
    elif re.match(r"^[a-z][a-z0-9_]+$", text):
        return switch_case_to_camel_f_case(text)
    else:
        raise UnknownCase

def switch_case_to_underscore_case(text):
    rep = lambda m: (m.group(1) and m.group(1) + '_') + m.group(2).lower()
    return re.sub(r"(^|[a-z0-9])([A-Z]+)", rep, text)

def switch_case_to_camel_f_case(text):
    return re.sub(r"_([a-z0-9])", lambda m: m.group(1).capitalize(), text)

def switch_case_to_camel_c_case(text):
    return re.sub(r"^([a-z0-9])", lambda m: m.group(1).capitalize(), text)

class SwitchCaseCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        for region in self.view.sel():
            text = self.view.substr(region)

            if not text:
                return

            try:
                text = switch_case(text)
                self.view.replace(edit, region, text)
            except UnknownCase:
                sublime.status_message('Unknown case type')
