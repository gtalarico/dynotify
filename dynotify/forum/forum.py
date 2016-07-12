import requests
import logging
import bs4
import json

logger = logging.getLogger()

class ForumPost(object):

    def __init__(self):
        self.title = None
        self.poster = None
        self.post_url = None

class Forum(object):
    max_pages = 3
    default_headers = {
                    # 'Accept': 'application/json',
                    # 'Accept': 'application/json, text/javascript, */*; q=0.01',
                    # 'Accept-Encoding': 'gzip, deflate, sdch, br',
                    # 'Accept-Language': 'en-US,en;q=0.8,pt-BR;q=0.6,pt;q=0.4,es;q=0.2',
                    'Referer': 'https://forum.dynamobim.com/',
                    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
                    # 'X-Requested-With': 'XMLHttpRequest'
                    }


class DynamoForum(Forum):

    headers = dict(Forum.default_headers)
    url = 'https://forum.dynamobim.com/latest?no_definitions=true&page={page_id}'
    post_url = 'https://forum.dynamobim.com/t/{slug}'

    class DynamoPost(object):

        def __init__(self, **topic):
            self.title = topic.get('title')
            self.tags = topic.get('tags', [])
            self.category_id = topic.get('category_id')
            self.views = topic.get('views')
            self.posts_count = topic.get('posts_count')
            self.last_posted_at = topic.get('last_posted_at')
            self.created_at = topic.get('created_at')
            self.has_accepted_answer = topic.get('has_accepted_answer')
            self.slug = topic.get('slug')
            self.post_url = DynamoForum.post_url.format(slug=self.slug)
            # self.last_poster_username = topic.get('last_poster_username', None)

            posters = topic.get('posters')
            for poster in posters:
                if poster.get('description') == 'Original Poster':
                    self.poster_id = poster.get('user_id')
                if poster.get('description') == 'Most Recent Poster':
                    self.last_poster = poster.get('user_id')

        def __repr__(self):
            return '<FORUM POST: {}>'.format(self.title)

        def print_post(self):
            for k,v in self.__dict__.items():
                print('{}: {}'.format(k, str(v)))

    def __init__(self):
        headers = DynamoForum.headers
        headers['Host'] = 'forum.dynamobim.com'
        headers['Accept'] = 'application/json'

        self.s = requests.Session()
        self.s.headers.update(headers)
        self.forum_posts = []
        self.pages = {}

    def get_pages(self):
        for page_id in range(1, DynamoForum.max_pages + 1):
            url = DynamoForum.url.format(page_id=page_id)
            try:
                print('Making request: ' + url )
                r = self.s.get(url, verify=False)
            except requests.exceptions.Timeout:
                logger.error('Could not get content from forum')
                return
            logger.info('STATUS: {}'.format(r.status_code))
            try:
                json_response = r.json()
            except:
                print('error')
            else:
                with open('sample_json_file', 'w') as fp:
                    json.dump(json_response, fp, indent=2)
                self.pages[page_id] = json_response
                topics = json_response['topic_list']['topics']
                for topic in topics:
                    post = self.DynamoPost(**topic)
                    self.forum_posts.append(post)


dynamoforum = DynamoForum()
dynamoforum.get_pages()
print(dynamoforum.forum_posts)
for post in dynamoforum.forum_posts:
    print('='*40)
    post.print_post()
# print(len(dynamoforum.forum_posts))
# print(dynamoforum.pages[1])
# print(pages.keys())
# print(pages['topic_list']['more_topics_url'])
# print(pages['topic_list']['topics'][0].keys())

# print(pages['topic_list']['topics'][0]['title'])
# print(pages['topic_list']['topics'][0]['views'])
# print(pages['topic_list']['topics'][0]['reply_count'])
# print(pages['topic_list']['topics'][0]['category_id'])
# print(pages['topic_list']['topics'][0]['tags'])
# print(pages['topic_list']['topics'][0]['topics'])
# print(pages['topic_list']['per_page'])
# import json
# d = json.loads(pages)
# dynamoforum.process_pages()
