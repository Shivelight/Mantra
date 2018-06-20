import aiohttp


class ClientResponse(aiohttp.client_reqrep.ClientResponse):

    @property
    def status_code(self):
        return self.status


def ClientSession(**kwargs):
    kwargs['response_class'] = ClientResponse
    return aiohttp.ClientSession(**kwargs)
