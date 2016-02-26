from notv.models import *
from crawlers import bilibili, vm

from django.core.management.base import BaseCommand

ALL_SOUCES = {
    'bilibili' : bilibili,
    'vm' : vm
}

class Command(BaseCommand):
    help = 'Update Ups and Videos'

    def add_arguments(self, parser):
        parser.add_argument('-r', default = False, required = False, action = 'store_true', dest = 'read')
        parser.add_argument('sources', nargs='*')

    def handle(self, *args, **options):
        read = options['read']
        if 'sources' in options:
            sources = [ALL_SOUCES[r] for r in options['sources']]
        else:
            sources = [bilibili, vm]


        for r in sources:
            print('updating ' + r.name)
            newUps = r.updateUps()
            if len(newUps) != 0:
                print('Find New UPs')
                for up in newUps:
                    print(up)

            videos = r.getUpdates(read)
            if videos != 0:
                print('Find New Videos')
                for v in videos:
                    print(str(v) + ' from ' + str(v.up))
