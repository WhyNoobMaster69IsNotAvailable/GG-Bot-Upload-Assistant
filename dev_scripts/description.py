from jinja2 import FileSystemLoader, Environment


class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def get_age(self):
        return self.age

    def get_name(self):
        return self.name


class DescriptionManager:
    def __init__(self):
        data = {
            "custom_description_components": "[code]This release is sourced from Amazon Prime[/code]",
            "internal": {
                "center_start": "[center]",
                "center_end": "[/center]",
                "uploader_signature": "Uploaded with [color=red]❤[/color] using GG-BOT Upload Assistant",
                "screenshot_header": "---------------------- [size=22]Screenshots[/size] ----------------------",
            },
            "screenshots": "[url=https://ptpimg.me/dpuq6e.png][img=350]https://ptpimg.me/dpuq6e.png[/img][/url] [url=https://ptpimg.me/kaz5nr.png][img=350]https://ptpimg.me/kaz5nr.png[/img][/url] [url=https://ptpimg.me/8fb12a.png][img=350]https://ptpimg.me/8fb12a.png[/img][/url] [url=https://ptpimg.me/9it24k.png][img=350]https://ptpimg.me/9it24k.png[/img][/url] [url=https://ptpimg.me/9o5751.png][img=350]https://ptpimg.me/9o5751.png[/img][/url] [url=https://ptpimg.me/07xk34.png][img=350]https://ptpimg.me/07xk34.png[/img][/url]",
        }

        templateLoader = FileSystemLoader(searchpath="./description_templates")
        templateEnv = Environment(loader=templateLoader)

        TEMPLATE_FILE = "default.jinja2"
        template = templateEnv.get_template(TEMPLATE_FILE)

        outputText = template.render(data=data)
        print(outputText)


if __name__ == "__main__":
    manager = DescriptionManager()
