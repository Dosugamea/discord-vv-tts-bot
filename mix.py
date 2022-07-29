import audioop
import discord


class MixAudioSource(discord.AudioSource):
    def __init__(self) -> None:
        super().__init__()
        self.sources = []

    def read(self) -> bytes:
        data = bytes(3840)
        for source in self.sources:
            if not (d := source.read()):
                source.cleanup()
                self.sources.remove(source)
            else:
                data = audioop.add(data, d, 2)
        return data
