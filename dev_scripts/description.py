from jinja2 import FileSystemLoader, Environment


class DescriptionManager:
    def __init__(self):
        data = {
            "custom_description_components": "[code]This release is sourced from Amazon Prime[/code]",
            "torrent_info": {
                "torrent_title": "Sangamam 1999 1080p AMZN WEB-DL DD+ 2.0 H.264-DTR",
                "screen_size": "1080p",
                "audio_codec": "DD+",
                "bit_depth": "8",
                "pymediainfo_video_codec": "H.264",
            },
            "release": {
                "title": "Sangamam 1999 1080p AMZN WEB-DL DD+ 2.0 H.264-DTR",
                "video": {
                    "resolution": "1080p",
                    "codec": "H.264",
                    "bitrate": "10000 kb/s",
                },
                "audio": {
                    "bitrate": "640 kb/s",
                    "codec": "H.264",
                    "channels": "5.1",
                },
            },
            "bbcode": {
                "center_start": "[center]",
                "center_end": "[/center]",
                "code_start": "[code]",
                "code_end": "[/code]",
            },
            "internal": {
                "uploader_signature": "Uploaded with [color=red]❤[/color] using GG-BOT Upload Assistant",
                "screenshot_header": "---------------------- [size=22]Screenshots[/size] ----------------------",
            },
            "screenshots": "[url=https://ptpimg.me/dpuq6e.png][img=350]https://ptpimg.me/dpuq6e.png[/img][/url] [url=https://ptpimg.me/kaz5nr.png][img=350]https://ptpimg.me/kaz5nr.png[/img][/url] [url=https://ptpimg.me/8fb12a.png][img=350]https://ptpimg.me/8fb12a.png[/img][/url] [url=https://ptpimg.me/9it24k.png][img=350]https://ptpimg.me/9it24k.png[/img][/url] [url=https://ptpimg.me/9o5751.png][img=350]https://ptpimg.me/9o5751.png[/img][/url] [url=https://ptpimg.me/07xk34.png][img=350]https://ptpimg.me/07xk34.png[/img][/url]",
        }

        templateLoader = FileSystemLoader(
            searchpath="/Users/aanand/IdeaProjects/gg-bot-upload-assistant/description_templates"
        )
        templateEnv = Environment(loader=templateLoader)

        TEMPLATE_FILE = "test.jinja2"
        template = templateEnv.get_template(TEMPLATE_FILE)

        outputText = template.render(data=data)
        print(outputText)


if __name__ == "__main__":
    manager = DescriptionManager()
