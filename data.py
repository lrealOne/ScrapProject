from scpKbm import data;

class GpuInfo:
    def __init__(self, model, price, url):
        self.model = model
        self.price = price
        self.url = url

    def get_data(self):
        return {
            'Model': self.model,
            'Price': self.price,
            'URL': self.url
        }

    @classmethod
    def add(cls, item):
        return cls(
            model=item.get("Model"),
            price=item.get("Price"),
            url=item.get("URL")
        )

gpu_scrape = [GpuInfo.add(item) for item in data]

for gpu in gpu_scrape:
    print(gpu.get_data())
