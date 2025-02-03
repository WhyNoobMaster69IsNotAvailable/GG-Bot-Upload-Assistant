import sentry_sdk


def run():
    sentry_sdk.init(
        environment="production",
        server_name="GG Bot Upload Assistant",
        dsn="https://4093e406eb754b20a2a7f6d15e6b34c0@ggbot.bot.nu/1",
        traces_sample_rate=1.0,
        profiles_sample_rate=1.0,
        attach_stacktrace=True,
        shutdown_timeout=20,
    )

    raise Exception("Raised Exception on purpose to send it to Bugsink")


if __name__ == "__main__":
    run()
