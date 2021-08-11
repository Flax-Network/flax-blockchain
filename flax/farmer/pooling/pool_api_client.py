from aiohttp import ClientSession, ClientTimeout

from flax.farmer.pooling.og_pool_protocol import SubmitPartial
from flax.server.server import ssl_context_for_root
from flax.ssl.create_ssl import get_mozilla_ca_crt

timeout = ClientTimeout(total=30)


class PoolApiClient:
    base_url: str

    def __init__(self, base_url: str) -> None:
        self.base_url = base_url
        self.ssl_context = ssl_context_for_root(get_mozilla_ca_crt())

    async def get_pool_info(self):
        async with ClientSession(timeout=timeout) as client:
            async with client.get(f"{self.base_url}/pool_info", ssl=self.ssl_context) as res:
                return await res.json()

    async def submit_partial(self, submit_partial: SubmitPartial):
        async with ClientSession(timeout=timeout) as client:
            async with client.post(
                    f"{self.base_url}/partial",
                    json=submit_partial.to_json_dict(),
                    ssl=self.ssl_context
            ) as res:
                return await res.json()
