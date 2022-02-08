import config
import utils.send_message.tg as tg
import utils.send_message.vk as vk


class SendMessage:
    async def __vk(msg: str) -> None:
        return await vk.send_message(msg)


    async def __tg(msg: str) -> None:
        return await tg.send_message(msg)


    @staticmethod
    async def services(msg: str) -> None:
        if config.VK['use']:
            await SendMessage.__vk(msg)
        if config.TG['use']:
            await SendMessage.__tg(msg)
