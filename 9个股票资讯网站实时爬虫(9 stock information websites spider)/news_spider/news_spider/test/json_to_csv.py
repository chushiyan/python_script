import json
import csv


class CSVPipeline(object):
    def __init__(self):
        self.resource = open('newsItem.json', 'r', encoding='utf-8')
        self.file = open("newsItem.csv", 'w', encoding='utf-8', newline="")
        self.writer = csv.writer(self.file, delimiter='#', quotechar='"')
        self.writer.writerow([
            'id',
            'source',
            'timestamp',
            'pubDate',
            'title',
            'content'
        ]
        )

        data = json.load(self.resource)

        for key, item in data.items():
            print(key)
            self.clear_item(item)


        for key, item in data.items():
            print(key)
            self.process_item(key,item)
        self.closed_spider()

    def clear_item(self, item):
        for key, value in item.items():
            if key == "Author":
                continue
            if type(value) == str:
                value = value.replace('\r\n', '').replace('\n', '').replace('\r', '').replace('\t', '').strip()
            if type(value) == list and len(value) > 0:
                for i in range(len(value)):
                    value[i] = value[i].replace('\r\n', '').replace('\n', '').replace('\r', '').replace('\t',
                                                                                                        '').strip()
            item[key] = value

    def process_item(self, key, item):

        self.writer.writerow([
            key,
            str(item['source']),
            item['timestamp'],
            str(item.get('pubDate', '')),
            str(item.get('title', '')),
            str(item.get('content', ''))
        ]
        )

        return item

    def closed_spider(self):
        self.file.close()


if __name__ == '__main__':
    csvPipeline = CSVPipeline()
