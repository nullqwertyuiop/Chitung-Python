from pathlib import Path

from graia.ariadne.app import Ariadne
from graia.ariadne.event.message import GroupMessage, MessageEvent
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import Image
from graia.ariadne.message.parser.twilight import Twilight, FullMatch, UnionMatch, MatchResult, SpacePolicy
from graia.saya import Saya, Channel
from graia.saya.builtins.broadcast import ListenerSchema

saya = Saya.current()
channel = Channel.current()

channel.name("ChitungHelp")
channel.author("角川烈、白门守望者（原作者）、nullqwertyuiop（移植）")
channel.description("七筒")


@channel.use(
    ListenerSchema(
        listening_events=[GroupMessage],
        inline_dispatchers=[
            Twilight(
                [
                    UnionMatch("/funct", "/discl") @ "which",
                ]
            )
        ]
    )
)
async def chitung_vanilla_image_handler(
        app: Ariadne,
        event: MessageEvent,
        which: MatchResult
):
    await app.sendGroupMessage(event.sender.group, MessageChain.create([
        Image(path=Path(Path(__file__).parent / "assets" / "help" / f"{which.result.asDisplay()[1:]}.png"))
    ]))
