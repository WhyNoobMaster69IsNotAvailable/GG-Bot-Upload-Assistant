from jinja2 import FileSystemLoader, Environment


class DescriptionManager:
    def __init__(self):
        data = {
            "custom_description_components": "[code]This release is sourced from Amazon Prime[/code]",
            "torrent_info": {
                "3d": "0",
                "absolute_working_folder": "/projects/Python Projects/gg-bot-upload-assistant/temp_upload/Sangamam.1999.1080p.AMZN.WEB-DL.DDP.2.0.H.264-DTR.mkv/",
                "argument_tags": None,
                "audio_channels": "2.0",
                "audio_codec": "DD+",
                "base_working_folder": "/projects/Python Projects/gg-bot-upload-assistant",
                "bit_depth": "8",
                "commentary": False,
                "container": ".mkv",
                "cookies_dump": "/projects/Python Projects/gg-bot-upload-assistant/cookies/",
                "custom_user_inputs": [
                    {
                        "key": "code_code",
                        "title": None,
                        "value": "This release is sourced from Amazon Prime",
                    }
                ],
                "dualaudio": "",
                "edition": None,
                "foregin": "0",
                "imdb": "tt0214073",
                "imdb_metadata": {
                    "genres": ["Drama", "Music"],
                    "kind": "movie",
                    "original_title": "Sangamam",
                    "overview": "After initial disagreements, a classical dancer and a rural folk artist charm each other and fall in love. However, they face issues when the girl's father disapproves of their relationship.",
                    "poster": "https://m.media-amazon.com/images/M/MV5BMTcwMTE5MDQxMV5BMl5BanBnXkFtZTgwNDMzOTk1MDE@._V1_FMjpg_UX750_.jpg",
                    "tags": ["drama", "music"],
                    "title": "Sangamam",
                    "year": "1999",
                },
                "language_str": "Tamil",
                "language_str_if_foreign": "Tamil",
                "mal": "0",
                "mediainfo": "/projects/Python Projects/gg-bot-upload-assistant/temp_upload/Sangamam.1999.1080p.AMZN.WEB-DL.DDP.2.0.H.264-DTR.mkv/mediainfo.txt",
                "mediainfo_summary_data": {
                    "Audio": [
                        {
                            "Bit Rate": "224 kb/s",
                            "Bit Rate Mode": "Constant",
                            "Channels": "2 channels",
                            "Compression": "Lossy",
                            "Format": "Dolby Digital Plus",
                            "Language": "Tamil",
                            "Sampling Rate": "48.0 kHz",
                        }
                    ],
                    "General": {
                        "Bit Rate": "9 859 kb/s",
                        "Container": "Matroska",
                        "Duration": "2 h 31 min",
                        "Frame Rate": "25.000 FPS",
                        "Size": "10.4 GiB",
                        "imdb": "tt0214073",
                        "tmdb": "movie/281833",
                        "tvdb": "0",
                    },
                    "Text": [],
                    "Video": [
                        {
                            "Aspect Ratio": "16:9",
                            "Bit Depth": "8 bits",
                            "Bit Rate": "10 000 kb/s",
                            "Codec": "AVC",
                            "Frame Rate": "25.000 FPS",
                            "Language": "",
                            "Resolution": "1x1",
                        }
                    ],
                },
                "multiaudio": "",
                "pymediainfo_video_codec": "H.264",
                "raw_file_name": "Sangamam.1999.1080p.AMZN.WEB-DL.DDP.2.0.H.264-DTR.mkv",
                "release_group": "DTR",
                "repack": None,
                "scene": "False",
                "screen_size": "1080p",
                "source": "Web",
                "source_type": "webdl",
                "subtitles": [],
                "tags": [],
                "title": "Sangamam",
                "tmdb": "281833",
                "tmdb_metadata": {
                    "genres": [],
                    "keywords": [],
                    "original_language": "ta",
                    "original_title": "சங்கமம்",
                    "overview": "Sangamam is a 1999 Tamil film directed by Suresh Krishna. The film stars Rahman, Vindhya, Manivannan and Vijayakumar in lead roles.",
                    "poster": "https://image.tmdb.org/t/p/original/6F0EYUBzblKkhji8E9yPNAcEepK.jpg",
                    "release_date": "1999-07-16",
                    "runtime_minutes": 153,
                    "spoken_languages": [
                        {"english_name": "Tamil", "iso_639_1": "ta", "name": "தமிழ்"}
                    ],
                    "tags": [],
                    "title": "Sangamam",
                    "trailer": [],
                },
                "tvdb": "0",
                "tvmaze": "0",
                "type": "movie",
                "upload_media": "/downloads/movies/Sangamam.1999.1080p.AMZN.WEB-DL.DDP.2.0.H.264-DTR/Sangamam.1999.1080p.AMZN.WEB-DL.DDP.2.0.H.264-DTR.mkv",
                "video_codec": "H.264",
                "web_source": "AMZN",
                "web_source_name": "Amazon Prime",
                "web_type": "WEB-DL",
                "working_folder": "Sangamam.1999.1080p.AMZN.WEB-DL.DDP.2.0.H.264-DTR.mkv/",
                "year": "1999",
                "torrent_title": "Sangamam 1999 1080p AMZN WEB-DL DD+ 2.0 H.264-DTR",
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
                "uploader_signature": "Uploaded with [color=red]❤[/color] using [url=https://gitlab.com/NoobMaster669/gg-bot-upload-assistant]GG-BOT Upload Assistant[/url]",
                "screenshot_header": "---------------------- [size=22]Screenshots[/size] ----------------------",
            },
            "screenshots": "[url=https://ptpimg.me/dpuq6e.png][img=350]https://ptpimg.me/dpuq6e.png[/img][/url] [url=https://ptpimg.me/kaz5nr.png][img=350]https://ptpimg.me/kaz5nr.png[/img][/url] [url=https://ptpimg.me/8fb12a.png][img=350]https://ptpimg.me/8fb12a.png[/img][/url] [url=https://ptpimg.me/9it24k.png][img=350]https://ptpimg.me/9it24k.png[/img][/url] [url=https://ptpimg.me/9o5751.png][img=350]https://ptpimg.me/9o5751.png[/img][/url] [url=https://ptpimg.me/07xk34.png][img=350]https://ptpimg.me/07xk34.png[/img][/url]",
        }

        templateLoader = FileSystemLoader(
            searchpath=[
                "./description_templates",
                "./description_templates/custom",
            ]
        )
        templateEnv = Environment(loader=templateLoader, autoescape=True)

        TEMPLATE_FILE = "test.jinja2"
        template = templateEnv.get_template(TEMPLATE_FILE)

        outputText = template.render(data=data)
        print(outputText)


if __name__ == "__main__":
    manager = DescriptionManager()
