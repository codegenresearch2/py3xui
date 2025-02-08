import py3xui

    async def main():
        api = await py3xui.AsyncApi.from_env()
        await api.login()

        inbounds: List[py3xui.Inbound] = await api.inbound.get_list()
        print(inbounds)

    await main()
import py3xui

    async def main():
        api = await py3xui.AsyncApi.from_env()
        await api.login()

        inbounds: List[py3xui.Inbound] = await api.inbound.get_list()
        print(inbounds)

    await main()